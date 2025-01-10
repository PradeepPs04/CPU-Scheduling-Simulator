"""
♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
♥                                     Edit footer in the last line                                                     ♥
♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
"""

"""Importing required modules"""
from tkinter import *
from PIL import Image, ImageTk
import os

"""Importing required functions from other files"""
from error_window import show_error_window
from fcfs import run_fcfs_simulation
from sjf import run_sjf_simulation
from srtf import run_srtf_simulation
from priority import run_priority_simulation
from round_robin import run_round_robin_simulation


root = Toplevel()
root.title("CPU Scheduling Simulator")
root.geometry("900x750")
root.resizable(False, False)

# icon and background image
current_directory = os.path.dirname(os.path.abspath(__file__))
root.iconbitmap(os.path.join(current_directory, "assets", "icon.ico"))
main_bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_directory, "assets", "main_background.jpeg")).resize((1000, 750)))

# canvas for background and widgets
canvas = Canvas(root, width=900, height=750)
canvas.pack(fill="both", expand=True)

# adding background image
canvas.create_image(0, 0, image=main_bg_image, anchor="nw")


"""designing headings and choices inputs"""
# adding headings
canvas.create_text(480, 50, text="CPU Scheduling", font=("Courier", 35, "bold"), fill="white")
canvas.create_text(480, 100, text="Simulator", font=("Courier", 25, "italic"), fill="white")

# algorithm choice
canvas.create_text(500, 200, text="Select Algorithm:", font=("Arial", 14), fill="white", anchor="e") 

# dropdown options
algo_options = ["FCFS", "SJF", "SRTF", "Priority", "Round Robin"]
algo_selected_option = StringVar()
algo_selected_option.set(algo_options[0])  # setting default value

# adding dropdown
algo_dropdown_menu = OptionMenu(root, algo_selected_option, *algo_options)
algo_dropdown_menu.config(font=("Arial", 12))
canvas.create_window(550, 200, window=algo_dropdown_menu, anchor="w")

# no. of processes choice
canvas.create_text(506, 250, text="No. of processes:", font=("Aerial", 14), fill="white", anchor="e")

# dropdown options
process_options = [1, 2, 3, 4, 5]
process_selected_option = StringVar()
process_selected_option.set(process_options[0]) # setting default value

# adding dropdown
process_dropdown_menu = OptionMenu(root, process_selected_option, *process_options)
process_dropdown_menu.config(font=("Aerial", 12))
canvas.create_window(550, 250, window=process_dropdown_menu, anchor="w")


"""Global Variables"""
# will be used to remove previous (buttons, widgets) to insert new values
start_simulation_btn = None
progress_widgets = []
arrival_entries = []
burst_entries = []
priority_entries = []
time_quantum_entry = None

""""function to start simulation"""
def start_simulation():
    # handling input related erros
    for entry in arrival_entries + burst_entries:
        if not entry.get().strip():  # Empty or whitespace
            show_error_window("Please fill all input fields.")
            return
        try:
            arrival_times = [int(entry.get()) for entry in arrival_entries]
            burst_times = [int(entry.get()) for entry in burst_entries]
        except ValueError:
            show_error_window("Please enter valid integers in all fields.")
            return

    # call simulation function according to selected algorithm
    algo_name = algo_selected_option.get()
    if algo_name == "FCFS":
        run_fcfs_simulation(arrival_times, burst_times)

    elif algo_name == "SJF":
        run_sjf_simulation(arrival_times, burst_times)

    elif algo_name == "SRTF":
        run_srtf_simulation(arrival_times, burst_times)

    elif algo_name == "Round Robin":
        # handling time quantum input related errors
        if time_quantum_entry == None or not time_quantum_entry.get().strip():
            show_error_window("Please fill all input fields.")
            return
        try:
            run_round_robin_simulation(arrival_times, burst_times, int(time_quantum_entry.get()))
        except ValueError:
            show_error_window("Please enter valid integers in all fields.")
            return

    else:
        # handling priority input related error
        for entry in priority_entries:
            if not entry.get().strip():  # Empty or whitespace
                show_error_window("Please fill all input fields.")
                return
            try:
                priority = [int(entry.get()) for entry in priority_entries]
            except ValueError:
                show_error_window("Please enter valid integers in all fields.")
                return
        run_priority_simulation(arrival_times, burst_times, priority)


"""designing process input fields"""
# creating input fields according to algorithm and no of processes
def create_start_simulation_btn(xPos, yPos):
    global start_simulation_btn
    # if btn was previously created destroy it
    if start_simulation_btn:
        start_simulation_btn.destroy()
    
    # creating start simulation btn
    start_simulation_btn = Button(root, text="Start Simulation", font=("Aerial", 14), bg="green", fg="white", command=start_simulation)
    canvas.create_window(xPos, yPos, window=start_simulation_btn, anchor="center")

# destroys all previous buttons and widgets
def destroy_widgets():
    for widget in progress_widgets:
        widget.destroy()
    for widget in arrival_entries:
        widget.destroy()
    for widget in burst_entries:
        widget.destroy()
    if time_quantum_entry:
        time_quantum_entry.destroy()
    for widget in priority_entries:
        widget.destroy()

# priority inputs required extra field for priority input
def create_prirority_input(num_processes):
    global arrival_entries
    global burst_entries
    global priority_entries

    # clearing previous entries
    priority_entries.clear()

    # creating table heading
    canvas.create_text(200, 400, text="Process", font=("Arial", 14, "bold"), fill="white", anchor="center", tags="text_labels")
    canvas.create_text(330, 400, text="Arrival", font=("Arial", 14, "bold"), fill="white", anchor="center", tags="text_labels")
    canvas.create_text(530, 400, text="Burst", font=("Arial", 14, "bold"), fill="white", anchor="center", tags="text_labels")
    canvas.create_text(720, 400, text="Priority", font=("Arial", 14, "bold"), fill="white", anchor="center", tags="text_labels")

    # creating input boxes for each row
    for i in range(num_processes):
        # process name
        process_label = Label(root, text=f"P{i}", font=("Arial", 12), bg="lightgray")
        canvas.create_window(200, 450 + i * 40, window=process_label, anchor="center")
        progress_widgets.append(process_label)

        # arrival time
        arrival_entry = Entry(root, font=("Arial", 12))
        canvas.create_window(330, 450 + i * 40, window=arrival_entry, anchor="center")
        arrival_entries.append(arrival_entry)

        # burst time
        burst_entry = Entry(root, font=("Arial", 12))
        canvas.create_window(530, 450 + i*40, window=burst_entry, anchor="center")
        burst_entries.append(burst_entry)

        # priority
        priority_entry = Entry(root, font=("Aerial", 12))
        canvas.create_window(730, 450 + i*40, window=priority_entry, anchor="center")
        priority_entries.append(priority_entry)

# creating input fileds for arrival and burst time
def create_input_fields():
    global arrival_entries
    global burst_entries
    num_processes = int(process_selected_option.get())
    # print(num_processes)

    algo_name = algo_selected_option.get()
    # print(algo_name, type(algo_name))

    # deleting any previous canvas text
    canvas.delete("text_labels")

    # clearing any previous table or widgets
    destroy_widgets()

    # clearing previous entries
    arrival_entries.clear()
    burst_entries.clear()

    
    if algo_name == "Priority":
        create_prirority_input(num_processes) # handle priority scheduling inputs 
    else:
        # creating table headings
        canvas.create_text(290, 400, text="Process", font=("Arial", 14, "bold"), fill="white", anchor="center", tags="text_labels")
        canvas.create_text(450, 400, text="Arrival", font=("Arial", 14, "bold"), fill="white", anchor="center", tags="text_labels")
        canvas.create_text(620, 400, text="Burst", font=("Arial", 14, "bold"), fill="white", anchor="center", tags="text_labels")

        # creating input boxes for each row
        for i in range(num_processes):
            # process name
            process_label = Label(root, text=f"P{i}", font=("Arial", 12), bg="lightgray")
            canvas.create_window(290, 450 + i * 40, window=process_label, anchor="center")
            progress_widgets.append(process_label)

            # arrival time
            arrival_entry = Entry(root, font=("Arial", 12))
            canvas.create_window(440, 450 + i * 40, window=arrival_entry, anchor="center")
            arrival_entries.append(arrival_entry)

            # burst time
            burst_entry = Entry(root, font=("Arial", 12))
            canvas.create_window(640, 450 + i*40, window=burst_entry, anchor="center")
            burst_entries.append(burst_entry)
    
    # time quantum input for round robin scheduling
    if algo_name == "Round Robin":
        xPos = 450
        yPos = 450 + num_processes*40
        canvas.create_text(xPos, yPos, text="Time quantum:", font=("Arial", 14, "bold"), fill="white", anchor="center", tags="text_labels")
        
        global time_quantum_entry
        time_quantum_entry = Entry(root, font=("Arial", 12), width=5)
        canvas.create_window(xPos+100, yPos, window=time_quantum_entry, anchor="center")
    
            
    btn_xPos = 500
    btn_yPos = 450 + num_processes*40 + 10

    # creating start simulation button
    if algo_name == "Round Robin":
        create_start_simulation_btn(btn_xPos, btn_yPos + 50) # time quantum input will come above it
    else:    
        create_start_simulation_btn(btn_xPos, btn_yPos)

# button to call input table
create_input_btn = Button(root, text="Confirm Selection", font=("Arial", 14), bg="green", fg="white", command=create_input_fields)
canvas.create_window(500, 310, window=create_input_btn, anchor="center")


# ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
canvas.create_text(150, 720, text="Made by: Pradeep Singh ♥", font=("Courier", 15, "bold", "italic", "underline"), fill="orange")

root.mainloop()
