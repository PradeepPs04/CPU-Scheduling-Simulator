"""Importing required modules"""
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import time
import os

"""Importing custom styles"""
from styles import configure_styles
configure_styles()

def run_sjf_simulation(arrival, burst):
    sjf_window = Toplevel()
    sjf_window.title("SJF Simulator")
    sjf_window.geometry("900x750")
    sjf_window.resizable(False, False)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    sjf_window.iconbitmap(os.path.join(current_directory, "assets", "icon.ico"))

    # adding background image
    bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_directory, "assets", "algo_background.jpeg")).resize((1000, 750)))
    canvas = Canvas(sjf_window, width=900, height=750)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    ### Top Section: Algorithm and CPU Info ###
    canvas.create_text(450, 40, text="SJF Simulator", font=("Courier", 20, "underline"), fill="white")

    # Process Table: Create Headers
    headers = ["Process", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time"]
    table_x_positions = [80, 230, 380, 530, 680]
    for i, header in enumerate(headers):
        canvas.create_text(table_x_positions[i], 80, text=header, font=("Arial", 12, "bold"), fill="white", anchor="w")

    # Add Process Data
    for i in range(len(arrival)):
        y_position = 120 + i * 40
        canvas.create_text(table_x_positions[0] + 20, y_position, text=f"P{i}", font=("Arial", 12), fill="white", anchor="w")
        canvas.create_text(table_x_positions[1] + 40, y_position, text=arrival[i], font=("Arial", 12), fill="white", anchor="w")
        canvas.create_text(table_x_positions[2] + 40, y_position, text=burst[i], font=("Arial", 12), fill="white", anchor="w")

    ### Middle Section: Headers ###
    headers = ["Status Bar", "Remaining Time"]
    x_positions = [150, 625]
    for i, header in enumerate(headers):
        canvas.create_text(x_positions[i], 325, text=header, font=("Arial", 12, "bold"), fill="white", anchor="w")

    # Initialize process data
    process = {}
    progress = {}
    remaining_time_labels = {}

    for i in range(len(arrival)):
        y_position = 365 + i * 40

        # Processes
        process[i] = Label(sjf_window, text=f"P{i}:", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(110, y_position, window=process[i], anchor="w")

        # Progress bar
        progress[i] = Progressbar(sjf_window, style="Custom.Horizontal.TProgressbar", orient=HORIZONTAL, length=400, mode="determinate")
        canvas.create_window(150, y_position, window=progress[i], anchor="w")

        # Remaining Burst Time
        remaining_time_labels[i] = Label(sjf_window, text=f"{burst[i]}ms", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(650, y_position, window=remaining_time_labels[i], anchor="w")

    ### Bottom Section: Stats and Ready Queue ###
    stats = ["Average Waiting Time:", "Average Turnaround Time:", "Total Execution Time:", "CPU Idle Time:"]
    stats_labels = {}
    for i, stat in enumerate(stats):
        canvas.create_text(570, 620 + i * 30, text=stat, font=("Arial", 12, "bold"), fill="white", anchor="w")
        stats_labels[stat] = Label(sjf_window, text="0", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(800, 620 + i * 30, window=stats_labels[stat], anchor="w")

    # Start Simulation Button
    start_button = Button(sjf_window, text="Start Simulation", width=18, style="Start.TButton")
    canvas.create_window(400, 590, window=start_button, anchor="center")

    def start_progress():
        start_button["state"] = DISABLED

        waiting_time = [0] * len(arrival)
        turnaround_time = [0] * len(arrival)
        current_time = 0
        completed_processes = []
        completed_count = 0
        idle_time = 0
        
        # Sort processes by arrival time
        processes = {}
        for i in range (len(arrival)):
            processes[i] = {
                "arrival": arrival[i],
                "burst": burst[i]
            }
        
        # gives smallest process from available processes
        def get_process():
            mini = -1
            for id in processes:
                # if process is completed or haven't came yet
                if id in completed_processes or processes[id]["arrival"] > current_time:
                    continue
                if mini == -1 or processes[id]["burst"] < processes[mini]["burst"]:
                    mini = id
            return mini

        while completed_count != len(processes):
            # get available process having smallest burst time
            mini_id = get_process()

            # if no process are available then cpu must wait
            if mini_id == -1:
                current_time += 1
                idle_time += 1
                continue

            # Simulate progress bar and remaiing time for the current process
            steps = max(10, int(burst[mini_id] * 5))
            for step in range(steps):
                progress[mini_id]["value"] += 100 / steps  # This will increment progress in each step
                remaining_time = max(0, burst[mini_id] - (burst[mini_id] * (step + 1) / steps))
                remaining_time_labels[mini_id]["text"] = f"{int(remaining_time)}ms"
                sjf_window.update_idletasks()
                time.sleep(0.08)

            current_time += processes[mini_id]["burst"]

            processes[mini_id]["completed"] = current_time
            turnaround_time[mini_id] = current_time - processes[mini_id]["arrival"]
            waiting_time[mini_id] = turnaround_time[mini_id] - processes[mini_id]["burst"]
            completed_processes.append(mini_id)

            completed_count += 1

        for i in range(len(arrival)):
            y_position = 120 + i * 40
            canvas.create_text(table_x_positions[3] + 40, y_position, text=waiting_time[i], font=("Arial", 12), fill="white", anchor="w")
            canvas.create_text(table_x_positions[4] + 40, y_position, text=turnaround_time[i], font=("Arial", 12), fill="white", anchor="w")

        avg_waiting_time = sum(waiting_time) / len(waiting_time)
        avg_turnaround_time = sum(turnaround_time) / len(turnaround_time)
        total_execution_time = current_time

        stats_labels["Average Waiting Time:"]["text"] = f"{avg_waiting_time:.2f} ms"
        stats_labels["Average Turnaround Time:"]["text"] = f"{avg_turnaround_time:.2f} ms"
        stats_labels["Total Execution Time:"]["text"] = f"{total_execution_time:.2f} ms"
        stats_labels["CPU Idle Time:"]["text"] = f"{idle_time:.2f} ms"

        start_button.config(text="Exit", command=sjf_window.destroy, width=18, style="Exit.TButton")
        start_button["state"] = NORMAL

    start_button["command"] = start_progress
    sjf_window.mainloop()



"""Testing sjf.py""" 
# arrival = [2,5,1,0,4]
# burst = [6,2,8,3,4]
# run_sjf_simulation(arrival,burst)