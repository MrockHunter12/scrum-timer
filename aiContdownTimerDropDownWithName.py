
import tkinter as tk
import time
import math
import os
from tkinter import messagebox
import configparser

class CountdownTimer:
    def __init__(self, parent):
        self.timeIsOver = False
        self.timeIsCloseToFinish = False
        self.main_window = parent
        self.verifiedNames=[]
        self.filePathToTimerstIni=os.path.join(os.getcwd(), 'timers.ini')
        self.darkGrayCoroCode= "#333"
        self.lightGreenColorCode = "#4caf50"
        self.blueColorCode = "#2196f3"
        self.redColorCode = "#f44336"

        # Create the timer frame
        self.timer_frame = tk.Frame(self.main_window, bg=self.darkGrayCoroCode, bd=5)
        self.timer_frame.pack(fill="x", padx=10, pady=5)

        # Create the timer label
        self.timer_label = tk.Label(self.timer_frame, text="00:00:00", font=("Arial", 30), bg=self.darkGrayCoroCode, fg="white")
        self.timer_label.pack(fill="x", padx=10, pady=5)

        # Create the next button
        self.next_button = tk.Button(self.timer_frame, text="Next", width=10, command=self.next, font=("Arial", 7), bg=self.lightGreenColorCode, fg="white")
        self.next_button.pack(side="right",padx=0,pady=0)

        # Create the previous button
        self.next_previous = tk.Button(self.timer_frame, text="Previous", width=10, command=self.previous, font=("Arial", 7), bg=self.lightGreenColorCode, fg="white")
        self.next_previous.pack(side="left", padx=0,pady=0)

        # Create the name label
        self.name_label = tk.Label(self.timer_frame, text="", font=("Arial", 14), bg=self.darkGrayCoroCode, fg="white")
        self.name_label.pack(fill="x", padx=10, pady=5)

        # Create the name timer label
        self.timerPerName_label = tk.Label(self.timer_frame, text="00:00:00", font=("Arial", 14), bg=self.darkGrayCoroCode, fg="white")
        self.timerPerName_label.pack(fill="x", padx=10, pady=5)

        # Create the timer interval per avergae
        self.timerPerNameAvgInSeconds = tk.Label(self.timer_frame, text="00:00:00", font=("Arial", 12), bg=self.darkGrayCoroCode, fg="cyan")
        self.timerPerNameAvgInSeconds.pack(fill="x", padx=10, pady=5)

        # Create the input frame
        self.input_frame = tk.Frame(self.main_window, bg=self.darkGrayCoroCode, bd=5)
        self.input_frame.pack(fill="x", padx=10, pady=5,anchor=tk.CENTER)

        # Create the input labels
        tk.Label(self.input_frame, text="Hours:", font=("Arial", 14), bg=self.darkGrayCoroCode, fg="white").pack()

        # Create the hours text input
        self.hours_entry = tk.StringVar(self.input_frame)
        self.hours_entry.set("0") # default value
        self.hours_text = tk.Entry(self.input_frame, textvariable=self.hours_entry, width=5,bg=self.darkGrayCoroCode,fg='white')
        self.hours_text.pack(anchor=tk.CENTER)

        tk.Label(self.input_frame, text="Minutes:", font=("Arial", 14), bg=self.darkGrayCoroCode, fg="white").pack()

        # Create the minutes text input
        self.minutes_entry = tk.StringVar(self.input_frame)
        self.minutes_entry.set("0") # default value
        self.minutes_text = tk.Entry(self.input_frame, textvariable=self.minutes_entry,width=5,bg=self.darkGrayCoroCode,fg='white')
        self.minutes_text.pack(padx=10,anchor=tk.CENTER)

         # Create the input frame
        self.dropFrame = tk.Frame(self.main_window, bg=self.darkGrayCoroCode, bd=5)
        self.dropFrame.pack(fill="x", padx=10, pady=5)

        self.load_timers(self.filePathToTimerstIni)
        # Create a variable to store the selected preconfigured time
        self.selected_time = tk.StringVar(self.input_frame)
        self.selected_time.set(self.preconfigured_times[0][0])

        # Create the dropdown menu
        self.time_options = tk.OptionMenu(self.dropFrame, self.selected_time, *[time[0] for time in self.preconfigured_times])
        self.time_options.pack(side="bottom",padx=10, pady=5)

        self.time_options.config(bg=self.darkGrayCoroCode)
        self.time_options["menu"].config(bg=self.darkGrayCoroCode)

        self.time_options.config(fg='white')
        self.time_options["menu"].config(fg='white')

        # Set a default value for the dropdown menu
        self.selected_time.set(self.preconfigured_times[0][0])

        # Bind the function to the dropdown menu
        self.selected_time.trace('w', self.update_time)

        # Create the control frame
        self.control_frame = tk.Frame(self.main_window, bg=self.darkGrayCoroCode, bd=5)
        self.control_frame.pack(fill="x", padx=10, pady=5)

        # Create the start button
        self.start_button = tk.Button(self.control_frame, text="Start", width=10, command=self.start, font=("Arial", 7), bg=self.lightGreenColorCode, fg="white")
        self.start_button.pack(fill="x", padx=10)
        
        # Create the pause button
        self.pause_button = tk.Button(self.control_frame, text="Pause", width=10, command=self.pause, state="disabled", font=("Arial", 7), bg=self.blueColorCode, fg="white")
        self.pause_button.pack(fill="x", padx=10)

        # Create the reset button
        self.reset_button = tk.Button(self.control_frame, text="Reset", width=10, command=self.reset, state="disabled", font=("Arial", 7), bg=self.redColorCode, fg="white")
        self.reset_button.pack(fill="x", padx=10)

        self.createCheckBoxes()

        self.select_all_var = tk.IntVar()
        self.select_all_checkbox = tk.Checkbutton(self.main_window, text="Select/Unselect All", variable=self.select_all_var, font=("Arial", 10), bg=self.darkGrayCoroCode,fg="gray", command=self.select_all)
        self.select_all_checkbox.pack()

        # Create the countdown variables
        self.remaining_seconds = 0
        self.countdown_seconds = 0
        self.timeSetInSeconds  = 0
        self.numberOfNamesLeft = 0
        self.counter = 0
        self.intervalTimerInSeconds = 0
        self.interval = 0
        self.countdown_running = False
        self.firstExecution = True

    def update_time(self, *args):
        selected = self.selected_time.get()
        # Iterate through the preconfigured times
        for time in self.preconfigured_times:
            if time[0] == selected:
                # Update the hours and minutes input fields
                self.hours_entry.set(time[1])
                self.minutes_entry.set(time[2])

    def select_all(self):
        is_checked = self.select_all_var.get()
        for var in self.checkBoxVariables:
            var.set(is_checked)


    def createCheckBoxes(self):
        self.checkboxes = []
        self.checkBoxVariables = []
        filePathToNamesTextFile=os.path.join(os.getcwd(), 'names.txt')
        try:
            self.load_names(filePathToNamesTextFile)
            for name in self.names:
                var = tk.IntVar() 
                checkbox = tk.Checkbutton(self.main_window, text=name, variable=var, font=("Arial", 10), bg=self.darkGrayCoroCode,fg="gray")
                checkbox.pack(fill="x")
                self.checkboxes.append(checkbox)
                var.set(1)  # set the initial value of the IntVar variable to 1
                self.checkBoxVariables.append(var)
        except Exception as e:
            self.show_warning("the file 'names.txt' in root folder containg the participant names was not found, timer will continue without")

    def load_names(self, filepath):
        """Load names from a text file and store them in a list"""
        with open(filepath, "r") as f:
            self.names = [line.strip() for line in f]

    def load_timers(self, filepath):
        config = configparser.ConfigParser()
        config.read(filepath)
        """Load timers from ini file and store them in a list"""
        self.preconfigured_times = []
        # Iterate through the sections in the ini file
        for section in config.sections():
            # Get the name, hours, and minutes from the section
            name = section
            hours = config[section]['hours']
            minutes = config[section]['minutes']
            # Add the preconfigured time to the list
            self.preconfigured_times.append((name, hours, minutes))

    def updateSubTimers(self):
        self.updateTimer(self.interval, self.timerPerNameAvgInSeconds)
        self.updateTimer(self.intervalTimerInSeconds, self.timerPerName_label)

    def updateTimer(self, timeVariableInSeconds, label):
        # Convert the countdown seconds to hours, minutes, and seconds
        hours, remainder = divmod(timeVariableInSeconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def next(self):
        if self.numberOfNamesLeft> 1:
            self.updateCurrentNameAndTrackNumberOfNamesLeft()
            if  self.numberOfNamesLeft != 0:
                self.calculateNewIntervalAndUpdateTimerInSeconds()
                self.updateSubTimers()
    
    
    def previous(self):
        if self.currentIndex > 0:
            self.currentIndex = self.currentIndex -1
            self.numberOfNamesLeft = self.numberOfNamesLeft +1
            self.calculateNewIntervalAndUpdateTimerInSeconds()
            name = self.verifiedNames[self.currentIndex]
            self.name_label.configure(text=name)
            self.intervalTimerInSeconds = int(self.interval)
            self.updateSubTimers()
    
    def calculateNewIntervalAndUpdateTimerInSeconds(self):
        self.interval = int(math.floor(self.countdown_seconds/ self.numberOfNamesLeft))
        if self.interval < 0:
            raise ValueError("Calculated interval is negative")
        self.intervalTimerInSeconds = self.interval

    def checkboxEvaluation(self, checkboxVariables, checkboxes):
        names = []
        for i, checkBoxVariable in enumerate(checkboxVariables):
            if checkBoxVariable.get():  # check if the checkbox is active
                name = checkboxes[i].cget("text")
                names.append(name)  # store
        return names
    
    def validateMinutesInput(self, minutes_str):
        if minutes_str.isdigit():
            minutes = int(minutes_str)
        else:
            minutes = 0
        return minutes

    def validateHoursInput(self, hours_str):
        if hours_str.isdigit():
            hours = int(hours_str)
        else:
            hours = 0
        return hours

    def disableNextAndPreviousButtons(self):
        self.next_button.config(state="disabled")
        self.next_previous.config(state="disabled")

    def enableNextAndPreviousButtons(self):
        self.next_button.config(state="normal")
        self.next_previous.config(state="normal")
            
            
    def start(self):
        self.main_window.geometry("270x200")
        self.firstExecution = True
        self.verifiedNames = []
        self.verifiedNames = self.checkboxEvaluation(self.checkBoxVariables, self.checkboxes)
        self.currentIndex = 0
        # If the timer was previously paused, use the remaining time as the countdown time
        if  self.countdown_seconds > 0:
            self.countdown_seconds =  self.countdown_seconds
        else:
            # Get the input time
            hours = self.validateHoursInput(self.hours_entry.get())
            minutes = self.validateMinutesInput(self.minutes_entry.get())
            # Convert the input time to seconds
            self.countdown_seconds = hours * 3600 + minutes * 60
            self.timeSetInSeconds = self.countdown_seconds
            # Calculate the time interval for each name
            self.numberOfNamesLeft = len(self.verifiedNames)
            if len(self.verifiedNames)!= 0:
                self.interval = int(math.floor((hours * 3600 + minutes * 60) / len(self.verifiedNames)))
                self.intervalTimerInSeconds = self.interval

                name = self.verifiedNames[self.currentIndex]
                self.name_label.configure(text=name)
                self.intervalTimerInSeconds = int(self.interval)

        # Enable the pause and reset buttons
        self.pause_button.config(state="normal")
        self.reset_button.config(state="normal")

        self.enableNextAndPreviousButtons()

        # Disable the start button
        self.start_button.config(state="disabled")

        # Set the countdown running flag to True
        self.countdown_running = True

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

        # Update the timer label
        self.timer_label.config(text="00:00:00")
        self.timerPerName_label.config(text="00:00:00")
        self.timerPerNameAvgInSeconds.config(text="00:00:00")
        self.name_label.configure(text="")
        self.countdown_seconds = 0
        self.intervalTimerInSeconds = 0

        # Enable the start button and disable the pause and reset buttons
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.disableNextAndPreviousButtons()
        self.timer_label.configure(fg="white")
        self.timerPerName_label.configure(fg="white")
        self.timerPerNameAvgInSeconds.configure(fg="cyan")

    def update_timer(self):
        if self.countdown_running and not self.firstExecution:
            if self.countdown_seconds <= self.timeSetInSeconds * 0.1 and not self.timeIsOver:
               self.timeIsCloseToFinish = True
            else:
               self.timeIsCloseToFinish = False
            # Decrement the countdown seconds
            if self.countdown_seconds > 0 and not self.timeIsOver:
                if len(self.verifiedNames)!= 0 and self.interval!=0:
                    if self.intervalTimerInSeconds <=0 :
                      self.updateCurrentNameAndTrackNumberOfNamesLeft()
                    self.intervalTimerInSeconds = self.intervalTimerInSeconds - 1
                    self.updateSubTimers()
                self.countdown_seconds -= 1
                
            else:
                self.timeIsCloseToFinish = False
                self.timeIsOver = True
                self.disableNextAndPreviousButtons()
                self.countdown_seconds += 1
            # Convert the countdown seconds to hours, minutes, and seconds
            self.updateTimer(self.countdown_seconds, self.timer_label)

            # Schedule the update_timer() function to run again after 1 second
            self.update_timer_label()
            self.main_window.after(1000, self.update_timer)
        elif self.countdown_running and self.firstExecution:
            self.firstExecution = False
            self.main_window.after(1000, self.update_timer)
        else:
            # Countdown has finished, disable the pause and reset buttons
            self.pause_button.config(state="disabled")
            self.reset_button.config(state="disabled")

    def update_timer_label(self):
        if self.timeIsCloseToFinish:
            if self.countdown_seconds % 2 == 0:
                self.timer_label.configure(fg="yellow")
            else:
                self.timer_label.configure(fg="red")
        elif self.timeIsOver:
            self.timer_label.configure(fg="red")
            self.timerPerName_label.config(text="time is over")
            self.timerPerNameAvgInSeconds.config(text="")
            self.name_label.config(text="")
            self.timerPerName_label.configure(fg="red")
        else:
            self.timer_label.configure(fg="white")


    def updateCurrentNameAndTrackNumberOfNamesLeft(self):
        # Update the name label every interval
        if not self.timeIsOver:
            try:
                # Get the next name from the iterator
                self.numberOfNamesLeft -=1 
                if self.currentIndex < len(self.verifiedNames)-1:
                    self.currentIndex += 1
                    name = self.verifiedNames[self.currentIndex]
                    self.name_label.configure(text=name)
            except:
                # If the iterator is exhausted, stay
                name = self.verifiedNames[self.currentIndex]
            # Call this method again after the interval
            self.intervalTimerInSeconds = int(self.interval)

    def show_warning(self, message):
        messagebox.showwarning('warning',message)

if __name__ == "__main__":
    darkGrayCoroCode= "#333"
    main_window = tk.Tk()

    main_window.title("M262 Motion Timer")
    main_window.minsize(200, 70)
    main_window.maxsize(300, 730)
    main_window.attributes("-topmost", True)
    main_window.configure(bg=darkGrayCoroCode)
    main_window.resizable(True, True)
    app = CountdownTimer(main_window)
    main_window.mainloop()

