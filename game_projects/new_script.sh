#!/bin/bash
read -p 'file name; ' choice
touch $choice.py
chmod u+x $choice.py
echo "#!/usr/bin/env python3" > $choice.py
echo "script was made"
