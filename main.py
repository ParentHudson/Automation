import tkinter as tk
from tkinter import messagebox
import time
import random
import csv
import webbrowser

task_websites = {"School": "https://idpz.utorauth.utoronto.ca/idp/profile/SAML2/Redirect/SSO?execution=e1s1",
                "Projects": "https://drive.google.com/drive/my-drive",
                "Music": "https://open.spotify.com/playlist/5pzDn4ZAEs5DWwzioJ7cGu?si=97d76cbbd4c54060&pt=b55a48c59f7332470348770ee1b85b50"}
task_type = None
#change this to whatever is the type in the file and then use the dict to open that website

def get_task():
    try:
        with open("tasks.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            tasks = [row["task"] for row in reader if row["task"]]
        return random.choice(tasks) if tasks else "No tasks found."
    except Exception as e:
        return f"Error loading tasks: {e}"

def log_session(task, duration):
    with open("session_log.csv", "a") as log:
        log.write(f"{task},{duration},{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def run_timer(minutes):
    total_seconds = minutes * 60
    for i in range(total_seconds, 0, -1):
        mins, secs = divmod(i, 60)
        timer_label.config(text=f"{mins:02}:{secs:02}")
        window.update()
        time.sleep(1)
    messagebox.showinfo("Done!")

def start_session():
    try:
        duration = int(time_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input")
        return

    task = get_task()
    task_label.config(text=f"Task: {task}")
    log_session(task, duration)
    webbrowser.open("https://q.utoronto.ca")
    run_timer(duration)

#UI
window = tk.Tk()
window.title("🎓 Smart Study Session")
window.attributes("-topmost", True)

tk.Label(window, text="Enter time available (minutes):").pack(pady=5)
time_entry = tk.Entry(window)
time_entry.pack(pady=5)

tk.Button(window, text="Start Session", command=start_session).pack(pady=10)

task_label = tk.Label(window, text= "Task: None")
task_label.pack(pady=5)

timer_label = tk.Label(window, text="00:00", font=("Helvetica", 10))
timer_label.pack(pady=10)

window.mainloop()
