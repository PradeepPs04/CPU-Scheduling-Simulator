from tkinter import ttk

def configure_styles():
    style = ttk.Style()

    # set theme
    style.theme_use("default")

    # style for text labels
    style.configure("Custom.TLabel", background="lightgray", font=("Arial", 12))

    # style for Start Button
    style.configure(
        "Start.TButton",
        background="green",
        foreground="white",
        font=("Arial", 12, "bold"),
        borderwidth=2,
        relief="raised",
        padding=5
    )
    style.map(
        "Start.TButton",
        background=[("active", "darkgreen")],
        foreground=[("active", "white")]
    )

    # style for Exit Button
    style.configure(
        "Exit.TButton",
        background="red",
        foreground="white",
        font=("Arial", 12, "bold"),
        borderwidth=2,
        relief="raised",
        padding=5
    )
    style.map(
        "Exit.TButton",
        background=[("active", "darkred")],
        foreground=[("active", "white")]
    )

    # style for Progress bar
    style.configure(
        "Custom.Horizontal.TProgressbar",
        troughcolor="white",  
        background="orange", 
        thickness=17         
    )
