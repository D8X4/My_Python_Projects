import sys
import json
import time
import subprocess
from dataclasses import dataclass, asdict, fields
from pathlib import Path

import cv2
from evdev import UInput, AbsInfo, ecodes as e
from PySide6.QtCore import QObject, QThread, Signal, Slot, Qt
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QPlainTextEdit, QDoubleSpinBox, QDialog,
)

BASE = Path(__file__).parent
ASSETS = BASE / "assets"
SHOT_PATH = ASSETS / "shot.png"
CONFIG_PATH = BASE / "config.json"

PIZZA_CHOICE = {
    "pepperoni": (820, 503),
    "cheese":    (1122, 501),
    "sausage":   (710, 695),
    "soda":      (1202, 709),
}

TEMPLATE_FILES = {
    "e_interract": "e_interract.png",
    "pepperoni":   "pepperoni_interract_gray.png",
    "cheese":      "cheese_interract_gray.png",
    "sausage":     "sausage_interract_gray.png",
    "soda":        "soda_interract_gray.png",
}

SCALES = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05]
MENU_BUTTON = (216, 721)
MAX_SCREEN_W = 1920


@dataclass
class Settings:
    """Shared between the GUI (writes) and the worker (reads). Saved to config.json."""
    min_score: float = 0.6
    min_e_score: float = 0.4
    line_y: int = 440   # bot only looks ABOVE this line
    x1: int = 820       # left edge of the region
    x2: int = 1130      # right edge of the region
    hover_delay: float = 0.4
    hold_time: float = 0.1
    menu_open_delay: float = 0.6
    order_open_delay: float = 0.7

    @classmethod
    def load(cls):
        s = cls()
        try:
            data = json.loads(CONFIG_PATH.read_text())
            for f in fields(cls):
                if f.name in data:
                    setattr(s, f.name, type(getattr(s, f.name))(data[f.name]))
        except (FileNotFoundError, ValueError, TypeError):
            pass
        return s

    def save(self):
        try:
            CONFIG_PATH.write_text(json.dumps(asdict(self), indent=2))
        except OSError:
            pass


def capture_screen():
    """Full screenshot via Spectacle, cropped to the first 1920px. None on failure."""
    subprocess.run(["spectacle", "-b", "-n", "-f", "-o", str(SHOT_PATH)])
    screen = cv2.imread(str(SHOT_PATH))
    if screen is None:
        return None
    if screen.shape[1] > MAX_SCREEN_W:
        screen = screen[:, :MAX_SCREEN_W]
    return screen


def bgr_to_qimage(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = rgb.shape
    return QImage(rgb.data, w, h, 3 * w, QImage.Format.Format_RGB888).copy()


# ======================= bot worker =======================
class BotWorker(QObject):
    log = Signal(str)
    status = Signal(str)
    finished = Signal()

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self._running = False
        self.ui: UInput | None = None
        self.templates = {}  # name -> list of pre-scaled templates

    def stop(self):
        self._running = False

    def sleep(self, seconds):
        """Sleep in small chunks so Stop reacts quickly."""
        end = time.time() + seconds
        while self._running and time.time() < end:
            time.sleep(0.05)

    def _dev(self) -> UInput:
        if self.ui is None:
            raise RuntimeError("input device not created yet")
        return self.ui

    def load_templates(self):
        for name, filename in TEMPLATE_FILES.items():
            img = cv2.imread(str(ASSETS / filename), cv2.IMREAD_GRAYSCALE)
            if img is None:
                self.log.emit(f"ERROR: couldn't load template '{name}' ({filename})")
                return False
            self.templates[name] = [
                cv2.resize(img, (int(img.shape[1] * s), int(img.shape[0] * s)))
                for s in SCALES
            ]
        return True

    def create_input_device(self):
        caps = {
            e.EV_KEY: [e.BTN_LEFT, e.KEY_E],
            e.EV_ABS: [
                (e.ABS_X, AbsInfo(0, 0, 3839, 0, 0, 0)),
                (e.ABS_Y, AbsInfo(0, 0, 1079, 0, 0, 0)),
            ],
        }
        self.ui = UInput(caps, name="virtual-mouse")
        self.sleep(1)

    def mouse_click(self, x, y):
        ui = self._dev()
        s = self.settings
        # approach from a nearby point so the game sees the cursor move onto the button
        ui.write(e.EV_ABS, e.ABS_X, x - 6)
        ui.write(e.EV_ABS, e.ABS_Y, y - 6)
        ui.syn()
        self.sleep(0.05)
        ui.write(e.EV_ABS, e.ABS_X, x)
        ui.write(e.EV_ABS, e.ABS_Y, y)
        ui.syn()
        self.sleep(s.hover_delay)

        ui.write(e.EV_KEY, e.BTN_LEFT, 1)
        ui.syn()
        self.sleep(s.hold_time)
        ui.write(e.EV_KEY, e.BTN_LEFT, 0)
        ui.syn()

    def key_press(self, key):
        ui = self._dev()
        ui.write(e.EV_KEY, key, 1)
        ui.syn()
        self.sleep(0.1)
        ui.write(e.EV_KEY, key, 0)
        ui.syn()

    def grab_region(self):
        """Screenshot -> grayscale region above the line, between x1 and x2."""
        screen = capture_screen()
        if screen is None:
            return None
        s = self.settings
        region = screen[:s.line_y, s.x1:s.x2]
        if region.size == 0:
            self.log.emit("ERROR: region is empty, re-set the line/region")
            return None
        return cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    def score(self, image, name):
        best = 0.0
        for tmpl in self.templates[name]:
            if tmpl.shape[1] > image.shape[1] or tmpl.shape[0] > image.shape[0]:
                continue
            result = cv2.matchTemplate(image, tmpl, cv2.TM_CCOEFF_NORMED)
            best = max(best, cv2.minMaxLoc(result)[1])
        return best

    @Slot()
    def run(self):
        self._running = True
        try:
            self.status.emit("Loading")
            if not self.load_templates():
                return
            try:
                self.create_input_device()
            except (PermissionError, OSError) as err:
                self.log.emit(f"ERROR: couldn't create virtual input device: {err}")
                return
            self.status.emit("Running")
            self.loop()
        except Exception as err:
            self.log.emit(f"ERROR: {type(err).__name__}: {err}")
        finally:
            if self.ui is not None:
                self.ui.close()
                self.ui = None
            self.status.emit("Stopped")
            self.finished.emit()

    def loop(self):
        while self._running:
            region = self.grab_region()
            if region is None:
                self.log.emit("Failed to load screenshot")
                self.sleep(1)
                continue

            e_score = self.score(region, "e_interract")
            if e_score < self.settings.min_e_score:
                self.log.emit(f"Waiting for e_interract... (score: {e_score:.3f})")
                self.sleep(0.3)
                continue

            self.log.emit(f"e_interract found! (score: {e_score:.3f})")
            self.key_press(e.KEY_E)
            self.sleep(self.settings.menu_open_delay)
            self.mouse_click(*MENU_BUTTON)
            self.sleep(self.settings.order_open_delay)
            if not self._running:
                break

            region = self.grab_region()
            if region is None:
                self.log.emit("Failed to load order screenshot")
                self.sleep(0.5)
                continue

            scores = {}
            for name in PIZZA_CHOICE:
                scores[name] = self.score(region, name)
                self.log.emit(f"{name}: {scores[name]:.3f}")

            winner = max(scores, key=scores.get)
            if scores[winner] >= self.settings.min_score:
                self.log.emit(f"Order matched: {winner} ({scores[winner]:.3f}) - Clicking!")
                self.mouse_click(*PIZZA_CHOICE[winner])
                self.sleep(1.0)
            else:
                self.log.emit(f"No order matched (best was {winner} at {scores[winner]:.3f})")

            self.sleep(0.3)


# ======================= picker / viewer =======================
class Canvas(QWidget):
    """Shows a screenshot. Modes: 'line' (click), 'region' (drag), 'view' (read-only)."""
    picked = Signal(int, int)  # line: (y, 0)   region: (x1, x2)

    def __init__(self, qimage, mode, settings):
        super().__init__()
        self.pix = QPixmap.fromImage(qimage)
        self.mode = mode
        self.settings = settings
        self.hover = None        # image coords of the cursor
        self.drag_start = None   # image x where the drag began
        self.setMouseTracking(True)
        self.setMinimumSize(640, 360)

    def _geometry(self):
        iw, ih = self.pix.width(), self.pix.height()
        scale = min(self.width() / iw, self.height() / ih)
        ox = (self.width() - iw * scale) / 2
        oy = (self.height() - ih * scale) / 2
        return scale, ox, oy

    def _to_image(self, pos):
        scale, ox, oy = self._geometry()
        x = int((pos.x() - ox) / scale)
        y = int((pos.y() - oy) / scale)
        x = max(0, min(self.pix.width() - 1, x))
        y = max(0, min(self.pix.height() - 1, y))
        return x, y

    def paintEvent(self, event):
        p = QPainter(self)
        scale, ox, oy = self._geometry()
        iw, ih = self.pix.width(), self.pix.height()
        p.drawPixmap(int(ox), int(oy), int(iw * scale), int(ih * scale), self.pix)

        green = QColor(0, 255, 0)
        red = QColor(255, 60, 60)
        s = self.settings

        # current saved values (green)
        p.fillRect(int(ox + s.x1 * scale), int(oy), int((s.x2 - s.x1) * scale),
                   int(ih * scale), QColor(0, 255, 0, 40))
        p.setPen(QPen(green, 2))
        ly = int(oy + s.line_y * scale)
        p.drawLine(int(ox), ly, int(ox + iw * scale), ly)

        # live preview (red)
        if self.hover is not None:
            hx, hy = self.hover
            if self.mode == "line":
                p.setPen(QPen(red, 2))
                y = int(oy + hy * scale)
                p.drawLine(int(ox), y, int(ox + iw * scale), y)
            elif self.mode == "region" and self.drag_start is not None:
                a, b = sorted((self.drag_start, hx))
                p.fillRect(int(ox + a * scale), int(oy), int((b - a) * scale),
                           int(ih * scale), QColor(255, 60, 60, 70))

        if self.mode == "view":
            # actual search area the bot sees
            area_x, area_y = int(ox + s.x1 * scale), int(oy)
            area_w, area_h = int((s.x2 - s.x1) * scale), int(s.line_y * scale)
            p.fillRect(area_x, area_y, area_w, area_h, QColor(0, 150, 255, 60))
            p.setPen(QPen(QColor(0, 150, 255), 2))
            p.drawRect(area_x, area_y, area_w, area_h)

            # click points
            p.setPen(QPen(QColor(255, 200, 0), 2))
            points = dict(PIZZA_CHOICE)
            points["menu"] = MENU_BUTTON
            for name, (cx, cy) in points.items():
                wx, wy = int(ox + cx * scale), int(oy + cy * scale)
                p.drawEllipse(wx - 8, wy - 8, 16, 16)
                p.drawLine(wx - 12, wy, wx + 12, wy)
                p.drawLine(wx, wy - 12, wx, wy + 12)
                p.drawText(wx + 12, wy - 10, name)
        p.end()

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton or self.mode == "view":
            return
        x, y = self._to_image(event.position().toPoint())
        if self.mode == "line":
            self.picked.emit(y, 0)
        else:
            self.drag_start = x
            self.hover = (x, y)

    def mouseMoveEvent(self, event):
        self.hover = self._to_image(event.position().toPoint())
        self.update()

    def mouseReleaseEvent(self, event):
        if self.mode == "region" and self.drag_start is not None:
            a, b = sorted((self.drag_start, self.hover[0]))
            self.drag_start = None
            if b - a >= 5:
                self.picked.emit(a, b)
            self.update()


class PickerDialog(QDialog):
    def __init__(self, qimage, mode, settings, parent=None):
        super().__init__(parent)
        texts = {
            "line": "Click to set the line. The bot only looks ABOVE it. (Esc to cancel)",
            "region": "Drag left/right over the order area. (Esc to cancel)",
            "view": "Blue = area the bot searches. Green = saved line/edges. "
                    "Yellow = click points. (Esc to close)",
        }
        titles = {"line": "Set line", "region": "Set region", "view": "Regions"}
        self.setWindowTitle(titles[mode])
        self.values = None

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(texts[mode]))
        self.canvas = Canvas(qimage, mode, settings)
        self.canvas.picked.connect(self.on_picked)
        layout.addWidget(self.canvas, 1)
        self.resize(1300, 800)

    def on_picked(self, a, b):
        self.values = (a, b)
        self.accept()


# ======================= main window =======================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pizza Bot")
        self.settings = Settings.load()
        self.thread = None
        self.worker = None

        layout = QVBoxLayout(self)

        self.status = QLabel("Status: idle")
        self.button = QPushButton("Start")

        # pickers
        self.line_btn = QPushButton("Set Line")
        self.region_btn = QPushButton("Set Region")
        self.show_btn = QPushButton("Show Regions")
        self.line_btn.clicked.connect(lambda: self.pick("line"))
        self.region_btn.clicked.connect(lambda: self.pick("region"))
        self.show_btn.clicked.connect(lambda: self.pick("view"))
        pick_row = QHBoxLayout()
        pick_row.addWidget(self.line_btn)
        pick_row.addWidget(self.region_btn)
        pick_row.addWidget(self.show_btn)

        self.info = QLabel()
        self.refresh_info()

        # score thresholds
        self.min_score_box = self.make_spinbox(self.settings.min_score, 0.0, 1.0)
        self.min_e_box = self.make_spinbox(self.settings.min_e_score, 0.0, 1.0)
        self.min_score_box.valueChanged.connect(
            lambda v: setattr(self.settings, "min_score", v))
        self.min_e_box.valueChanged.connect(
            lambda v: setattr(self.settings, "min_e_score", v))
        row = QHBoxLayout()
        row.addWidget(QLabel("Order min score"))
        row.addWidget(self.min_score_box)
        row.addWidget(QLabel("E min score"))
        row.addWidget(self.min_e_box)

        # delays
        delay_grid = QGridLayout()
        delay_fields = [
            ("Hover", "hover_delay"), ("Hold", "hold_time"),
            ("Menu open", "menu_open_delay"), ("Order open", "order_open_delay"),
        ]
        for i, (label, attr) in enumerate(delay_fields):
            box = self.make_spinbox(getattr(self.settings, attr), 0.0, 3.0)
            box.valueChanged.connect(lambda v, a=attr: setattr(self.settings, a, v))
            delay_grid.addWidget(QLabel(label), i // 2, (i % 2) * 2)
            delay_grid.addWidget(box, i // 2, (i % 2) * 2 + 1)

        self.logbox = QPlainTextEdit()
        self.logbox.setReadOnly(True)
        self.logbox.setMaximumBlockCount(500)

        layout.addWidget(self.status)
        layout.addWidget(self.button)
        layout.addLayout(pick_row)
        layout.addWidget(self.info)
        layout.addLayout(row)
        layout.addLayout(delay_grid)
        layout.addWidget(self.logbox)

        self.button.clicked.connect(self.toggle)

    @staticmethod
    def make_spinbox(value, lo, hi):
        box = QDoubleSpinBox()
        box.setRange(lo, hi)
        box.setSingleStep(0.05)
        box.setDecimals(2)
        box.setValue(value)
        return box

    def refresh_info(self):
        s = self.settings
        self.info.setText(f"Line Y: {s.line_y}    Region X: {s.x1} to {s.x2}")

    def pick(self, mode):
        # hide this window so it isn't in the screenshot
        self.hide()
        QApplication.processEvents()
        QThread.msleep(600)
        img = capture_screen()
        self.show()
        if img is None:
            self.logbox.appendPlainText("ERROR: couldn't take screenshot for picker")
            return

        dlg = PickerDialog(bgr_to_qimage(img), mode, self.settings, self)
        if mode == "view":
            dlg.exec()
            return
        if dlg.exec() and dlg.values:
            a, b = dlg.values
            if mode == "line":
                self.settings.line_y = a
            else:
                self.settings.x1, self.settings.x2 = a, b
            self.settings.save()
            self.refresh_info()
            self.logbox.appendPlainText(f"Updated {mode}: {self.info.text()}")

    def set_picking_enabled(self, enabled):
        self.line_btn.setEnabled(enabled)
        self.region_btn.setEnabled(enabled)
        self.show_btn.setEnabled(enabled)

    def toggle(self):
        if self.thread is None:
            self.start_bot()
        else:
            self.worker.stop()
            self.button.setEnabled(False)

    def start_bot(self):
        self.thread = QThread()
        self.worker = BotWorker(self.settings)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.log.connect(self.logbox.appendPlainText)
        self.worker.status.connect(lambda s: self.status.setText(f"Status: {s}"))
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.on_stopped)

        self.thread.start()
        self.button.setText("Stop")
        self.set_picking_enabled(False)

    def on_stopped(self):
        self.thread = None
        self.worker = None
        self.button.setText("Start")
        self.button.setEnabled(True)
        self.set_picking_enabled(True)

    def closeEvent(self, event):
        if self.worker is not None:
            self.worker.stop()
            self.thread.quit()
            self.thread.wait(3000)
        self.settings.save()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
