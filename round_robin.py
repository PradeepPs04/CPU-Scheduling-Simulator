from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import time
import os

"""Importing custom styles"""
from styles import configure_styles
configure_styles()


"""Main function"""
def run_round_robin_simulation(arrival, burst, quantum):
    rr_window = Toplevel()
    rr_window.title("Round Robin Simulator")
    rr_window.geometry("900x750")
    rr_window.resizable(False, False)

    # icon and background image
    current_directory = os.path.dirname(os.path.abspath(__file__))
    rr_window.iconbitmap(os.path.join(current_directory, "assets", "icon.ico"))
    bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_directory, "assets", "algo_background.jpeg")).resize((1000, 750)))

    canvas = Canvas(rr_window, width=900, height=750)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")


    """styling"""
    # heading
    canvas.create_text(450, 40, text="Round Robin Simulator", font=("Courier", 20, "underline"), fill="white")


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

        # processes
        process[i] = Label(rr_window, text=f"P{i}:", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(110, y_position, window=process[i], anchor="w")

        # Progress bar
        progress[i] = Progressbar(rr_window, style="Custom.Horizontal.TProgressbar", orient=HORIZONTAL, length=400, mode="determinate")
        canvas.create_window(150, y_position, window=progress[i], anchor="w")

        # remaining time
        remaining_time_labels[i] = Label(rr_window, text=f"{burst[i]}ms", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(650, y_position, window=remaining_time_labels[i], anchor="w")
    

    # adding time quantum label
    quantum_label = Label(rr_window, text=f"Time Quantum: {quantum} ms", font=("Arial", 12, "bold"), background="skyblue")
    canvas.create_window(150, 590, window=quantum_label)


    ## stats section ##
    stats = ["Average Waiting Time:", "Average Turnaround Time:", "Total Execution Time:", "CPU Idle Time:"]
    stats_labels = {}
    for i, stat in enumerate(stats):
        canvas.create_text(570, 620 + i * 30, text=stat, font=("Arial", 12, "bold"), fill="white", anchor="w")
        stats_labels[stat] = Label(rr_window, text="         ", font=("Arial", 12), style="Custom.TLabel")
        canvas.create_window(800, 620 + i * 30, window=stats_labels[stat], anchor="w")

    # Start Simulation Button
    start_button = Button(rr_window, text="Start Simulation", width=18, style="Start.TButton")
    canvas.create_window(400, 590, window=start_button, anchor="center")


    """round robin simulation function"""
    def start_progress():
        # disable click on start button once schedulig is started
        start_button["state"] = DISABLED

        waiting_time = [0] * len(arrival) # will store waiting time of each process
        turnaround_time = [0] * len(arrival) # will store turnaround time of each process
        current_time = 0
        completed_processes = []
        completed_count = 0
        idle_time = 0

        ready_queue = []

        # adding processes data in single structure (dictionary)
        processes = {}
        for i in range(len(arrival)):
            processes[i] = {
                "arrival": arrival[i],
                "burst": burst[i],
                "remaining": burst[i],
                "total_steps": max(10, int(burst[i] * 5)), # total steps for progress bar
            }

        # add all processes to queue that are arriving at 0
        for id in range (len(arrival)):
            if processes[id]["arrival"] == 0:
                ready_queue.append(id)

        while completed_count != len(arrival):
            # if process available in ready queue
            if ready_queue:
                current_process = ready_queue.pop(0)
                time_slice = min(quantum, processes[current_process]["remaining"])

                # execute the process for time slice
                processes[current_process]["remaining"] -= time_slice
                current_time += time_slice

                # simulate progress bar for the current process
                progress[current_process]["value"] = (1 - (processes[current_process]["remaining"] / burst[current_process])) * 100

                # decrement remaining burst time
                remaining_time = max(0, processes[current_process]["remaining"])
                remaining_time_labels[current_process]["text"] = f"{int(remaining_time)}ms"

                rr_window.update_idletasks()
                time.sleep(0.5)


                # check if current process has finished its execution
                if processes[current_process]["remaining"] == 0:
                    # calculate stats of process
                    turnaround_time[current_process] = current_time - processes[current_process]["arrival"]
                    waiting_time[current_process] = turnaround_time[current_process] - processes[current_process]["burst"]
                    completed_processes.append(current_process)
                    completed_count += 1

                # add new arriving process to ready queue
                for id in range(len(arrival)):
                    if processes[id]["arrival"] > current_time or id == current_process:
                        continue
                    if id not in ready_queue and id not in completed_processes:
                        ready_queue.append(id)

                # if the process has not finished, add it to ready queue again
                if processes[current_process]["remaining"] > 0:
                    ready_queue.append(current_process)

            else:
                # if no process available then CPU must wait
                current_time += 1
                idle_time += 1

                # add new arriving process to ready queue
                for id in range (len(arrival)):
                    if id not in completed_processes and processes[id]["arrival"] <= current_time:
                        ready_queue.append(id)


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
        start_button.config(text="Exit", command=rr_window.destroy, width=18, style="Exit.TButton")
        start_button["state"] = NORMAL # make it clickable again


    start_button["command"] = start_progress # adding function to on click event of button

    rr_window.mainloop()



"""
########################################################################################
#           Remove below comments and run program to test round robin only             #
########################################################################################
""" 
# arrival = [2,5,1,0,4]
# burst = [6,2,8,3,4]
# quantum = 2
# run_round_robin_simulation(arrival, burst, quantum)
