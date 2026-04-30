#!/usr/bin/env python3
import pandas as pd
import random
import os

# Expand the tilde (~) so Python can find the home directory
file_path = os.path.expanduser('~/Webscrapes/animelist.csv')

try:
    df = pd.read_csv(file_path)
    
    # Filter for the stuff you haven't watched yet
    to_watch = df[df['status'] == 'Plan to Watch']
    
    if not to_watch.empty:
        choice = random.choice(to_watch['name'].tolist())
        print(choice)
    else:
        print("\nNo 'Plan to Watch' items found in the CSV!")
        
except Exception as e:
    print(f"Error: {e}")
