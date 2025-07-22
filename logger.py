import os
import csv
from datetime import datetime

LOG_DIR = "data"

def init_log(username):
    os.makedirs(LOG_DIR, exist_ok=True)
    filepath = os.path.join(LOG_DIR, f"{username}.csv")
    if not os.path.exists(filepath):
        with open(filepath, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Exercise", "Score", "Feedback"])

def log_progress(username, exercise, score, feedback):
    filepath = os.path.join(LOG_DIR, f"{username}.csv")
    with open(filepath, "a", newline='') as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, exercise, round(score, 2), feedback])
