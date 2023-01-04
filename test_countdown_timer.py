import unittest
import os
os.system('Xvfb :1 -screen 0 1600x1200x16  &')    # create virtual display with size 1600x1200 and 16 bit color. Color can be changed to 24 or 8
os.environ['DISPLAY']=':1.0'    # tell X clients to use our virtual DISPLAY :1.0.
import tkinter as tk
from tkinter import messagebox
from unittest.mock import Mock

from aiContdownTimerDropDownWithName  import CountdownTimer

class TestCountdownTimer(unittest.TestCase):
    def setUp(self):
        # Create a dummy tkinter window to use as the parent for the CountdownTimer object
        self.main_window = tk.Tk()

        self.main_window.title("M262 Motion Timer")
        self.main_window.minsize(200, 70)
        self.main_window.maxsize(300, 520)
        self.main_window.attributes("-topmost", True)
        self.main_window.configure(bg="#333")
        self.main_window.resizable(True, True)

        # Create an instance of the CountdownTimer class
        self.countdown_timer = CountdownTimer(self.main_window)
    
    def tearDown(self):
        # Destroy the window created in the setUp method
        self.main_window.destroy()

    def test_next(self):
        self.countdown_timer.verifiedNames = ["person1","person2","person3","person4"]
        self.countdown_timer.timeIsOver = False
        self.countdown_timer.numberOfNamesLeft = 3
        self.countdown_timer.currentIndex = 1
        self.countdown_timer.next()
        self.assertEqual(self.countdown_timer.currentIndex, 2)
        self.countdown_timer.next()
        self.assertEqual(self.countdown_timer.currentIndex, 3)
    
    def test_load_names(self):
        self.countdown_timer.load_names("names.txt")
        self.assertEqual(self.countdown_timer.names, ["Uros", "Petar", "Felix", "Anica", "Igor"])

    def test_update_timer(self):
        self.label = Mock()

        # Test a countdown of 1 hour, 23 minutes, and 45 seconds
        self.countdown_timer.updateTimer(3600 + 23*60 + 45, self.label)
        self.label.config.assert_called_with(text="01:23:45")
        
        # Test a countdown of 4 hours, 2 minutes, and 30 seconds
        self.countdown_timer.updateTimer(4*3600 + 2*60 + 30, self.label)
        self.label.config.assert_called_with(text="04:02:30")

    def test_checkbox_evaluation(self):
        self.checkbox_variables = [Mock(), Mock(), Mock()]
        self.checkboxes = [Mock(), Mock(), Mock()]
        self.checkboxes[0].cget.return_value = "Alice"
        self.checkboxes[1].cget.return_value = "Bob"
        self.checkboxes[2].cget.return_value = "Charlie"

        # Test with all checkboxes inactive
        self.checkbox_variables[0].get.return_value = False
        self.checkbox_variables[1].get.return_value = False
        self.checkbox_variables[2].get.return_value = False
        names = self.countdown_timer.checkboxEvaluation(self.checkbox_variables, self.checkboxes)
        self.assertEqual(names, [])
        
        # Test with all checkboxes active
        self.checkbox_variables[0].get.return_value = True
        self.checkbox_variables[1].get.return_value = True
        self.checkbox_variables[2].get.return_value = True
        names = self.countdown_timer.checkboxEvaluation(self.checkbox_variables, self.checkboxes)
        self.assertEqual(names, ["Alice", "Bob", "Charlie"])
        
        # Test with only the first and third checkboxes active
        self.checkbox_variables[0].get.return_value = True
        self.checkbox_variables[1].get.return_value = False
        self.checkbox_variables[2].get.return_value = True
        names = self.countdown_timer.checkboxEvaluation(self.checkbox_variables, self.checkboxes)
        self.assertEqual(names, ["Alice", "Charlie"])

    def test_validate_minutes_input(self):
        # Test with a valid input
        minutes_str = "45"
        minutes = self.countdown_timer.validateMinutesInput(minutes_str)
        self.assertEqual(minutes, 45)
        
        # Test with an invalid input
        minutes_str = "abc"
        minutes = self.countdown_timer.validateMinutesInput(minutes_str)
        self.assertEqual(minutes, 0)
    
    def test_validate_hours_input(self):
        # Test with a valid input
        hours_str = "3"
        hours = self.countdown_timer.validateHoursInput(hours_str)
        self.assertEqual(hours, 3)
        
        # Test with an invalid input
        hours_str = "abc"
        hours = self.countdown_timer.validateHoursInput(hours_str)
        self.assertEqual(hours, 0)

if __name__ == '__main__':
    unittest.main()
