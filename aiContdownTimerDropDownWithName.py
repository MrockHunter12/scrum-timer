
import tkinter as tk
import time
import math

class CountdownTimer:
    def __init__(self, parent):
        self.timeIsOver = False
        self.timeIsCloseToFinish = False
        self.main_window = parent
        self.verifiedNames=[]

        # Create the timer frame
        self.timer_frame = tk.Frame(self.main_window, bg="#333", bd=5)
        self.timer_frame.pack(fill="x", padx=10, pady=5)

        # Create the timer label
        self.timer_label = tk.Label(self.timer_frame, text="00:00:00", font=("Arial", 30), bg="#333", fg="#fff")
        self.timer_label.pack(fill="x", padx=10, pady=5)

        # Create the name label
        self.name_label = tk.Label(self.main_window, text="", font=("Arial", 14), bg="#333", fg="#fff")
        self.name_label.pack(fill="x", padx=10, pady=5)

        # Create the name label
        self.timerPerName_label = tk.Label(self.main_window, text="00:00:00", font=("Arial", 14), bg="#333", fg="#fff")
        self.timerPerName_label.pack(fill="x", padx=10, pady=5)

        # Create the input frame
        self.input_frame = tk.Frame(self.main_window, bg="#333", bd=5)
        self.input_frame.pack(fill="x", padx=10, pady=5)

        # Create the input labels
        tk.Label(self.input_frame, text="Hours:", font=("Arial", 14), bg="#333", fg="#fff").pack(side="left")

        # Create the hours drop-down menu
        self.hours_entry = tk.StringVar(self.input_frame)
        self.hours_entry.set("0") # default value
        self.hours_menu = tk.OptionMenu(self.input_frame, self.hours_entry, "0", "1", "2", "3", "4", "5")
        self.hours_menu.pack(side="left")

        tk.Label(self.input_frame, text="Minutes:", font=("Arial", 14), bg="#333", fg="#fff").pack(side="left")

        # Create the minutes drop-down menu
        self.minutes_entry = tk.StringVar(self.input_frame)
        self.minutes_entry.set("15") # default value
        self.minutes_menu = tk.OptionMenu(self.input_frame, self.minutes_entry, "1", "2", "3" ,"4", "5", "15", "30", "45")
        self.minutes_menu.pack(side="left")

        # Modify the style of the OptionMenu widgets to a dark mode theme
        self.hours_menu["menu"].configure(foreground="#fff", background="#333")
        self.minutes_menu["menu"].configure(foreground="#fff", background="#333")

        # Create the control frame
        self.control_frame = tk.Frame(self.main_window, bg="#333", bd=5)
        self.control_frame.pack(fill="x", padx=10, pady=5)

        # Create the start button
        self.start_button = tk.Button(self.control_frame, text="Start", width=10, command=self.start, font=("Arial", 7), bg="#4caf50", fg="#fff")
        self.start_button.pack(side="left", padx=10)
        
        # Create the pause button
        self.pause_button = tk.Button(self.control_frame, text="Pause", width=10, command=self.pause, state="disabled", font=("Arial", 7), bg="#2196f3", fg="#fff")
        self.pause_button.pack(side="left", padx=10)

        # Create the reset button
        self.reset_button = tk.Button(self.control_frame, text="Reset", width=10, command=self.reset, state="disabled", font=("Arial", 7), bg="#f44336", fg="#fff")
        self.reset_button.pack(side="left", padx=10)

        self.createCheckBoxes()

        # Create the countdown variables
        self.remaining_seconds = 0
        self.countdown_seconds = 0
        self.timeSetInSeconds  = 0
        self.counter = 0
        self.countdown_running = False

    def createCheckBoxes(self):
        self.checkboxes = []
        self.checkBoxVariables = []
        self.load_names("C:\\Users\SESA478801\\Documents\\names.txt")
        for name in self.names:
            var = tk.IntVar() 
            checkbox = tk.Checkbutton(self.main_window, text=name, variable=var, font=("Arial", 10), bg="#333",fg="#808080")
            checkbox.pack()
            self.checkboxes.append(checkbox)
            var.set(1)  # set the initial value of the IntVar variable to 1
            self.checkBoxVariables.append(var)

    def load_names(self, filepath):
        """Load names from a text file and store them in a list"""
        with open(filepath, "r") as f:
            self.names = [line.strip() for line in f]



    def start(self):
        self.verifiedNames = []
        for i, checkBoxVariable in enumerate(self.checkBoxVariables):
            if checkBoxVariable.get():  # check if the checkbox is active
                name = self.checkboxes[i].cget("text")
                self.verifiedNames.append(name)  # store
        self.name_iter = iter(self.verifiedNames)  # create iterator for names list
        # If the timer was previously paused, use the remaining time as the countdown time
        if  self.countdown_seconds > 0:
            self.countdown_seconds =  self.countdown_seconds
        else:
            # Get the input time
            hours_str = self.hours_entry.get()
            minutes_str = self.minutes_entry.get()

            # Validate the input
            if minutes_str.isdigit():
                minutes = int(minutes_str)
            else:
                minutes = 0
            if hours_str.isdigit() :
                hours = int(hours_str)
            else:
                hours = 0
            # Convert the input time to seconds
            self.countdown_seconds = hours * 3600 + minutes * 60
            self.timeSetInSeconds = self.countdown_seconds
            # Calculate the time interval for each name
            self.interval = int(math.floor((hours * 3600 + minutes * 60) / len(self.verifiedNames)))
            self.intervalTimerInSeconds = self.interval
            #self.update_name()

        # Enable the pause and reset buttons
        self.pause_button.config(state="normal")
        self.reset_button.config(state="normal")

        # Disable the start button
        self.start_button.config(state="disabled")

        # Set the countdown running flag to True
        self.countdown_running = True

        # Calculate the time interval for each name
        #self.interval = (hours * 3600 + minutes * 60) / len(self.verifiedNames)

        # Update the timer label
        self.update_timer()


    def pause(self):
        self.countdown_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def reset(self):
        self.timeIsOver = False
        # Reset the countdown variables
        self.countdown_seconds = 0
        self.countdown_running = False

        # Clear the input entries
        self.hours_entry.set("0")
        self.minutes_entry.set("0")
        #self.name_iter = iter(self.verifiedNames)

        # Update the timer label
        self.timer_label.config(text="00:00:00")
        self.timerPerName_label.config(text="00:00:00")
        self.name_label.configure(text="")
        self.countdown_seconds = 0
        self.intervalTimerInSeconds = 0

        # Enable the start button and disable the pause and reset buttons
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.reset_button.config(state="disabled")

    def update_timer(self):
        
        if self.countdown_running :
            self.update_timer_label()
            if self.countdown_seconds <= self.timeSetInSeconds * 0.1 and not self.timeIsOver:
               self.timeIsCloseToFinish = True
            else:
               self.timeIsCloseToFinish = False
            # Decrement the countdown seconds
            if self.countdown_seconds > 0 and not self.timeIsOver:
                if (self.countdown_seconds % self.interval == 0) :
                    self.update_name()
                self.countdown_seconds -= 1
                self.intervalTimerInSeconds -= 1
            else:
                self.timeIsCloseToFinish = False
                self.timeIsOver = True
                self.countdown_seconds += 1
            # Convert the countdown seconds to hours, minutes, and seconds
            hours, remainder = divmod(self.countdown_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Update the timer label
            self.timer_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

            # Convert the countdown seconds to hours, minutes, and seconds
            hours, remainder = divmod(self.intervalTimerInSeconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Update the timer label
            self.timerPerName_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

            # Schedule the update_timer() function to run again after 1 second
            self.main_window.after(1000, self.update_timer)
            self.update_timer_label()
        else:
            # Countdown has finished, disable the pause and reset buttons
            self.pause_button.config(state="disabled")
            self.reset_button.config(state="disabled")

    def update_timer_label(self):
        if self.timeIsCloseToFinish:
            if self.countdown_seconds % 2 == 0:
                self.timer_label.configure(fg="#FFFF00")
            else:
                self.timer_label.configure(fg="#FF0000")
        elif self.timeIsOver:
            self.timer_label.configure(fg="#FF0000")
            self.timerPerName_label.config(text="time is over")
            self.name_label.config(text="")
            self.timerPerName_label.configure(fg="#FF0000")
        else:
            self.timer_label.configure(fg="#fff")

    def update_name(self):
        # Update the name label every interval
        if not self.timeIsOver:
            try:
                # Get the next name from the iterator
                name = next(self.name_iter)
            except StopIteration:
                # If the iterator is exhausted, start again from the beginning
                self.name_iter = iter(self.verifiedNames)
                name = next(self.name_iter)

            # Update the name label
            self.name_label.configure(text=name)

            # Call this method again after the interval
            #self.main_window.after(int(self.interval * 1000), self.update_name)
            self.intervalTimerInSeconds = int(self.interval)

if __name__ == "__main__":
    
    main_window = tk.Tk()

    main_window.title("M262 Motion Timer")
    main_window.minsize(200, 70)
    main_window.maxsize(300, 520)
    main_window.attributes("-topmost", True)
    main_window.configure(bg="#333")

    # make a frame for the title bar
    #title_bar = Frame(main_window, bg="#333", relief='raised', bd=1)


    main_window.resizable(True, True)
    app = CountdownTimer(main_window)
    app.load_names("C:\\Users\SESA478801\\Documents\\names.txt")
    main_window.mainloop()

