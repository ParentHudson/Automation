import tkinter as tk
from tkinter import messagebox
import time
import random
import csv
import webbrowser
import os

### Next Steps ###
"""
Include apps not just web pages
replace time.sleep
"""

task_websites = {"school": "https://q.utoronto.ca",
                "projects": "https://drive.google.com/drive/my-drive",
                "music": "https://open.spotify.com/playlist/5pzDn4ZAEs5DWwzioJ7cGu?si=97d76cbbd4c54060&pt=b55a48c59f7332470348770ee1b85b50"}

seconds_left = 0

def get_task():
    try:
        with open("tasks.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            tasks = [row for row in reader if row["task"]]
        return random.choice(tasks) if tasks else "No tasks found."
    except Exception as e:
        return f"Error loading tasks: {e}"

def log_session(task, duration):
    with open("session_log.csv", "a") as log:
        log.write(f"{task},{duration},{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def run_timer(seconds):
    global seconds_left
    total_seconds = seconds
    for i in range(total_seconds, 0, -1):
        seconds_left -= 1
        mins, secs = divmod(i, 60)
        timer_label.config(text=f"{mins:02}:{secs:02}")
        window.update()
        time.sleep(1)
        #this needs to be written differently because it if causing errors
    messagebox.showinfo("Done!")

def start_session(seconds):
    global seconds_left
    if seconds_left == 0:
        seconds_left += seconds
        task = get_task()
        task_name = task["task"]
        task_label.config(text=f"Task: {task_name}")
        log_session(task, seconds_left)
        webbrowser.open(task_websites[task["type"].lower()])
        run_timer(seconds)
    else:
        seconds_left += seconds
        run_timer(seconds_left)

    

#UI
window = tk.Tk()
window.title("🎓 Smart Study Session")
window.attributes("-topmost", True)

tk.Button(window, text=" +30 ", command=lambda: start_session(30*60)).pack(pady=0)
tk.Button(window, text=" +1h ", command=lambda: start_session(60*60)).pack(pady=0)

task_label = tk.Label(window, text= "Task: None")
task_label.pack(pady=5)

timer_label = tk.Label(window, text="00:00", font=("Helvetica", 10))
timer_label.pack(pady=10)

window.mainloop()
