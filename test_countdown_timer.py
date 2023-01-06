import unittest
import os
os.system('Xvfb :1 -screen 0 1600x1200x16  &')    # create virtual display with size 1600x1200 and 16 bit color. Color can be changed to 24 or 8
os.environ['DISPLAY']=':1.0'    # tell X clients to use our virtual DISPLAY :1.0.
import tkinter as tk
from unittest.mock import Mock
from unittest.mock import MagicMock
from tkinter import messagebox

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

        # create mock buttons for testing
        self.next_button = MagicMock()
        self.next_previous = MagicMock()

        self.start_button = MagicMock()
        self.pause_button = MagicMock()
        self.reset_button = MagicMock()


        # create mock timer label for testing
        self.timer_label = MagicMock()
        self.timerPerName_label = MagicMock()
        self.timerPerNameAvgInSeconds = MagicMock()
        self.name_label = MagicMock()

        # assign the mock buttons to the object under test
        self.countdown_timer.next_button = self.next_button
        self.countdown_timer.next_previous = self.next_previous

        self.countdown_timer.start_button = self.start_button
        self.countdown_timer.pause_button = self.pause_button
        self.countdown_timer.reset_button = self.reset_button

        # assign the mock timer labels to the object under test
        self.countdown_timer.timer_label = self.timer_label
        self.countdown_timer.timerPerName_label = self.timerPerName_label
        self.countdown_timer.timerPerNameAvgInSeconds = self.timerPerNameAvgInSeconds
        self.countdown_timer.name_label = self.name_label
    
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

    def test_previous(self):
        self.countdown_timer.verifiedNames = ["person1","person2","person3","person4"]
        self.countdown_timer.timeIsOver = False
        self.countdown_timer.numberOfNamesLeft = 2
        self.countdown_timer.currentIndex = 2
        self.countdown_timer.previous()
        self.assertEqual(self.countdown_timer.currentIndex, 1)
        self.assertEqual(self.countdown_timer.verifiedNames[self.countdown_timer.currentIndex], "person2" )
        self.countdown_timer.previous()
        self.assertEqual(self.countdown_timer.currentIndex, 0)
        self.assertEqual(self.countdown_timer.verifiedNames[self.countdown_timer.currentIndex], "person1" )
    
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

    def test_calculate_new_interval(self):
        self.countdown_timer.countdown_seconds = 120
        self.countdown_timer.numberOfNamesLeft = 2
        self.countdown_timer.calculateNewIntervalAndUpdateTimerInSeconds()
        self.assertEqual(self.countdown_timer.interval, 60)
        self.assertEqual(self.countdown_timer.intervalTimerInSeconds, 60)

        self.countdown_timer.countdown_seconds = 120
        self.countdown_timer.numberOfNamesLeft = 0
        with self.assertRaises(ZeroDivisionError):
            self.countdown_timer.calculateNewIntervalAndUpdateTimerInSeconds()

        self.countdown_timer.countdown_seconds = -120
        self.countdown_timer.numberOfNamesLeft = 2
        with self.assertRaises(ValueError):
            self.countdown_timer.calculateNewIntervalAndUpdateTimerInSeconds()
    
    def test_disable_next_and_previous_buttons(self):
        self.countdown_timer.disableNextAndPreviousButtons()
        self.next_button.config.assert_called_with(state="disabled")
        self.next_previous.config.assert_called_with(state="disabled")

    def test_enable_next_and_previous_buttons(self):
        self.countdown_timer.enableNextAndPreviousButtons()
        self.next_button.config.assert_called_with(state="normal")
        self.next_previous.config.assert_called_with(state="normal")

    def test_pause(self):
        self.countdown_timer.pause()
        self.assertEqual(self.countdown_timer.countdown_running, False)
        self.start_button.config.assert_called_with(state="normal")
        self.pause_button.config.assert_called_with(state="disabled")

    def test_reset(self):
        self.countdown_timer.disableNextAndPreviousButtons = MagicMock()
        self.countdown_timer.reset()
        self.assertEqual(self.countdown_timer.timeIsOver, False)
        self.assertEqual(self.countdown_timer.countdown_seconds, 0)
        self.assertEqual(self.countdown_timer.countdown_running, False)
        self.timer_label.config.assert_called_with(text="00:00:00")
        self.timerPerName_label.config.assert_called_with(text="00:00:00")
        self.timerPerNameAvgInSeconds.config.assert_called_with(text="00:00:00")
        self.name_label.configure.assert_called_with(text="")
        self.assertEqual(self.countdown_timer.intervalTimerInSeconds, 0)
        self.start_button.config.assert_called_with(state="normal")
        self.pause_button.config.assert_called_with(state="disabled")
        self.reset_button.config.assert_called_with(state="disabled")
        self.countdown_timer.disableNextAndPreviousButtons.assert_called_once()
        self.timer_label.configure.assert_called_with(fg="white")
        self.timerPerName_label.configure.assert_called_with(fg="white")
        self.timerPerNameAvgInSeconds.configure.assert_called_with(fg="cyan")

    def test_update_timer_label(self):
        # Test when timeIsCloseToFinish is True
        self.countdown_timer.timeIsCloseToFinish = True
        self.countdown_timer.countdown_seconds = 1
        self.countdown_timer.update_timer_label()
        self.timer_label.configure.assert_called_with(fg="red")

        self.timer_label.reset_mock()
        self.countdown_timer.countdown_seconds = 2
        self.countdown_timer.update_timer_label()
        self.timer_label.configure.assert_called_with(fg="yellow")

        # Test when timeIsOver is True
        self.timer_label.reset_mock()
        self.timerPerName_label.reset_mock()
        self.timerPerNameAvgInSeconds.reset_mock()
        self.name_label.reset_mock()
        self.countdown_timer.timeIsCloseToFinish = False
        self.countdown_timer.timeIsOver = True
        self.countdown_timer.update_timer_label()
        self.timer_label.configure.assert_called_with(fg="red")
        self.timerPerName_label.config.assert_called_with(text="time is over")
        self.timerPerNameAvgInSeconds.config.assert_called_with(text="")
        self.name_label.config.assert_called_with(text="")
        self.timerPerName_label.configure.assert_called_with(fg="red")
        # Test when timeIsCloseToFinish and timeIsOver are False
        self.timer_label.reset_mock()
        self.timerPerName_label.reset_mock()
        self.timerPerNameAvgInSeconds.reset_mock()
        self.name_label.reset_mock()
        self.countdown_timer.timeIsCloseToFinish = False
        self.countdown_timer.timeIsOver = False
        self.countdown_timer.update_timer_label()
        self.timer_label.configure.assert_called_with(fg="white")
        self.timerPerName_label.config.assert_not_called()
        self.timerPerNameAvgInSeconds.config.assert_not_called()
        self.name_label.config.assert_not_called()
        self.timerPerName_label.configure.assert_not_called()

    def test_start(self):
        # Create mock objects
        self.countdown_timer.checkboxEvaluation = MagicMock(return_value=["Alice", "Bob"])
        self.countdown_timer.validateHoursInput = MagicMock(return_value=1)
        self.countdown_timer.validateMinutesInput = MagicMock(return_value=0)
        self.countdown_timer.update_timer = MagicMock()
        self.countdown_timer.enableNextAndPreviousButtons = MagicMock()
        # Set the countdown_seconds to a non-zero value
        self.countdown_timer.countdown_seconds = 3600
        self.countdown_timer.start()

        # Verify that the start button is disabled
        self.countdown_timer.start_button.config.assert_called_with(state="disabled")
        # Verify that the pause and reset buttons are enabled
        self.countdown_timer.pause_button.config.assert_called_with(state="normal")
        self.countdown_timer.reset_button.config.assert_called_with(state="normal")
        # Verify that the next and previous buttons are enabled
        self.countdown_timer.enableNextAndPreviousButtons.assert_called_once()
        # Verify that the countdown_running flag is set to True
        self.assertTrue(self.countdown_timer.countdown_running)
        # Verify that update_timer is called
        self.countdown_timer.update_timer.assert_called_once()
        # Verify that the number of names left is set correctly
        self.assertEqual(self.countdown_timer.numberOfNamesLeft, 0)
        # Verify that the interval is calculated correctly
        self.assertEqual(self.countdown_timer.interval, 1800)
        self.assertEqual(self.countdown_timer.intervalTimerInSeconds, 1800)
        # Verify that the name label is updated
        self.countdown_timer.name_label.configure.assert_called_with(text="Alice")

    def test_start_when_countdown_seconds_is_zero(self):
        self.countdown_timer.enableNextAndPreviousButtons = MagicMock()
        self.countdown_timer.checkboxEvaluation = MagicMock()
        self.names = ["name1", "name2", "name3"]
        self.countdown_timer.checkboxEvaluation = MagicMock(return_value=self.names)
        # Test when countdown_seconds is zero
        self.countdown_timer.countdown_seconds = 0
        
        #self.countdown_timer.verifiedNames = ["name1", "name2", "name3"]
        self.countdown_timer.hours_entry.set("1")
        self.countdown_timer.minutes_entry.set("0")
        self.countdown_timer.start()
        self.countdown_timer.pause_button.config.assert_called_with(state="normal")
        self.countdown_timer.reset_button.config.assert_called_with(state="normal")
        self.countdown_timer.enableNextAndPreviousButtons.assert_called_once()
        self.countdown_timer.start_button.config.assert_called_with(state="disabled")
        self.assertEqual(self.countdown_timer.countdown_seconds, 3600)
        self.assertEqual(self.countdown_timer.timeSetInSeconds, 3600)
        self.assertEqual(self.countdown_timer.numberOfNamesLeft, 3)
        # maybe code has to be adapted here
        self.assertEqual(self.countdown_timer.interval, 1200)
        self.assertEqual(self.countdown_timer.intervalTimerInSeconds, 1200)
        self.assertEqual(self.countdown_timer.currentIndex, 0)
        self.countdown_timer.name_label.configure.assert_called_with(text="name1")

        # Verify that the start button is disabled
        self.countdown_timer.start_button.config.assert_called
if __name__ == '__main__':
    unittest.main()
