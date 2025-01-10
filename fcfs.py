"""Importing required modules"""
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import time
import os

"""Importing custom styles"""
from styles import configure_styles
configure_styles()

"""Main function"""
def run_fcfs_simulation(arrival, burst):
    fcfs_window = Toplevel()
    fcfs_window.title("FCFS Simulator")
    fcfs_window.geometry("900x750")
    fcfs_window.resizable(False, False)
    
    # adding icon & background image
    current_directory = os.path.dirname(os.path.abspath(__file__))
    fcfs_window.iconbitmap(os.path.join(current_directory, "assets", "icon.ico"))
    bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_directory, "assets", "algo_background.jpeg")).resize((1000, 750)))

    canvas = Canvas(fcfs_window, width=900, height=750)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    """styling"""
    # heading
    canvas.create_text(450, 40, text="FCFS Simulator", font=("Courier", 20, "underline"), fill="white")

    ## process table ##
    headers = ["Process", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time"]
    table_x_positions = [80, 230, 380, 530, 680]
    for i, header in enumerate(headers):
        canvas.create_text(table_x_positions[i], 80, text=header, font=("Arial", 12, "bold"), fill="white", anchor="w")

    # adding data in process table
    for i in range(len(arrival)):
        y_position = 120 + i * 40
        canvas.create_text(table_x_positions[0] + 20, y_position, text=f"P{i}", font=("Arial", 12), fill="white", anchor="w")
        canvas.create_text(table_x_positions[1] + 40, y_position, text=arrival[i], font=("Arial", 12), fill="white", anchor="w")
        canvas.create_text(table_x_positions[2] + 40, y_position, text=burst[i], font=("Arial", 12), fill="white", anchor="w")

    ## simulation section ##
    headers = ["Status Bar", "Remaining Time"]
    x_positions = [150, 625]
    for i, header in enumerate(headers):
        canvas.create_text(x_positions[i], 325, text=header, font=("Arial", 12, "bold"), fill="white", anchor="w")

    # initializing process data
    process = {}
    progress = {}
    remaining_time_labels = {}

    for i in range(len(arrival)):
        y_position = 365 + i * 40

        # process
        process[i] = Label(fcfs_window, text=f"P{i}:", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(110, y_position, window=process[i], anchor="w")

        # Progress bar
        progress[i] = Progressbar(fcfs_window, style="Custom.Horizontal.TProgressbar", orient=HORIZONTAL, length=400, mode="determinate")
        canvas.create_window(150, y_position, window=progress[i], anchor="w")

        # remaining time
        remaining_time_labels[i] = Label(fcfs_window, text=f"{burst[i]}ms", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(650, y_position, window=remaining_time_labels[i], anchor="w")

    ## stats section ##
    stats = ["Average Waiting Time:", "Average Turnaround Time:", "Total Execution Time:", "CPU Idle Time:"]
    stats_labels = {}
    for i, stat in enumerate(stats):
        canvas.create_text(570, 620 + i * 30, text=stat, font=("Arial", 12, "bold"), fill="white", anchor="w")
        stats_labels[stat] = Label(fcfs_window, text="         ", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(800, 620 + i * 30, window=stats_labels[stat], anchor="w")

    # Start Simulation Button
    start_button = Button(fcfs_window, text="Start Simulation", width=18, style="Start.TButton")
    canvas.create_window(400, 590, window=start_button, anchor="center")

    """fcfs simulation function"""
    def start_progress():
        # disable click on start button once schedulig is started
        start_button["state"] = DISABLED

        ready_queue = []
        waiting_time = [0] * len(arrival) # will store waiting time of each process
        turnaround_time = [0] * len(arrival) # will store turnaround time of each process
        current_time = 0
        completed_processes = []
        idle_time = 0

        # Sort processes by arrival time
        processes = sorted(enumerate(arrival), key=lambda x: x[1])

        """Add newly arrived processes to the ready queue."""
        def update_ready_queue():
            for process_id, arrival_time in processes:
                if process_id not in completed_processes and arrival_time <= current_time and f"P{process_id}" not in ready_queue:
                    ready_queue.append(f"P{process_id}")

        """Starting fcfs algorithm"""
        for process_id, arrival_time in processes:
            if current_time < arrival_time:
                idle_time += (arrival_time - current_time)
                current_time = arrival_time

            # add any new arriving process to ready queue
            update_ready_queue()
            
            # simulate progress bar and remaining time for the current process
            steps = max(10, int(burst[process_id] * 5))
            for step in range(steps):
                progress[process_id]["value"] += 100 / steps  # This will increment progress in each step
                remaining_time = max(0, burst[process_id] - (burst[process_id] * (step + 1) / steps))
                remaining_time_labels[process_id]["text"] = f"{int(remaining_time)}ms"
                fcfs_window.update_idletasks()
                time.sleep(0.08)

            current_time += burst[process_id]
            completed_processes.append(process_id) 
            ready_queue.remove(f"P{process_id}") # remove process from ready queue

            # calculate turnaround & waiting time
            turnaround_time[process_id] = current_time - arrival_time
            waiting_time[process_id] = turnaround_time[process_id] - burst[process_id]

        """add stats to screen"""
        # adding waiting and turnaround of each process to process table
        for i in range(len(arrival)):
            y_position = 120 + i * 40
            canvas.create_text(table_x_positions[3] + 40, y_position, text=waiting_time[i], font=("Arial", 12), fill="white", anchor="w")
            canvas.create_text(table_x_positions[4] + 40, y_position, text=turnaround_time[i], font=("Arial", 12), fill="white", anchor="w")

        # calculate required stats
        avg_waiting_time = sum(waiting_time) / len(waiting_time)
        avg_turnaround_time = sum(turnaround_time) / len(turnaround_time)
        total_execution_time = current_time

        # display calculated stats in screen
        stats_labels["Average Waiting Time:"]["text"] = f"{avg_waiting_time:.2f} ms"
        stats_labels["Average Turnaround Time:"]["text"] = f"{avg_turnaround_time:.2f} ms"
        stats_labels["Total Execution Time:"]["text"] = f"{total_execution_time:.2f} ms"
        stats_labels["CPU Idle Time:"]["text"] = f"{idle_time:.2f} ms"

        """Change start button to exit button when simulation is finished"""
        start_button.config(text="Exit", command=fcfs_window.destroy, width=18, style="Exit.TButton")
        start_button["state"] = NORMAL # make it clickable again


    start_button["command"] = start_progress # adding function to on click event of button

    fcfs_window.mainloop()




"""
########################################################################################
#           Remove below comments and run program to test fcfs only                    #
########################################################################################
""" 
# arrival = [0,0,0,20,0]
# burst = [1,2,3,4,5]
# run_fcfs_simulation(arrival,burst)
