import pandas as pd
import os
import re
from datetime import datetime, timedelta

PATTERN = re.compile(r'screenshot(\d+)_(\d{2})_(\d{2})__(\d{2})_(\d{2})\.txt')
# df = pd.DataFrame(columns=['Camera', 'Date', 'X_center', 'Y_center', 'Width', 'Height'])
NUMERIC_COLS = ['Camera', 'X_center', 'Y_center', 'Width', 'Height']

def read_positions(label_dir='../../data_all/labels', output_csv='positions.csv'):
    """
    Reads elephant labels into a csv file if not available, otherwise return it.
    Parameters:
    - label_dir (str): Path to annotation labals.
    - output_csv (str): Path to output csv file.
    """
    df = pd.DataFrame(columns=['Camera', 'Date', 'X_center', 'Y_center', 'Width', 'Height'])
    csv_file = output_csv
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        for col in NUMERIC_COLS:
            df[col] = pd.to_numeric(df[col])
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    
    for filename in os.listdir(label_dir):
        ending = os.path.splitext(filename)[0][-2:]
        if ending not in ['00', '15', '30', '45']:
            continue
        path = os.path.join(label_dir, filename)
        match = PATTERN.match(filename)
        assert match
        camera, day, month, hour, minute = map(int, match.groups())
        # Convert to datetime object
        data = {}
        timestamp = pd.Timestamp(year=2024, month=month, day=day, hour=hour, minute=minute)
        with open(path) as file:
            for item in file:
                _, x_center, y_center, width, height = item.strip().split()
                data['X_center'], data['Y_center'], data['Width'], data['Height'] = x_center, y_center, width, height
                data['Camera'] = camera
                data['Date'] = pd.to_datetime(timestamp)
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'] + pd.Timedelta(hours=1)
    if not os.path.exists(csv_file):
        df.to_csv(csv_file, index=False)
    return df