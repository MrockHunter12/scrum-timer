import unittest
import os
os.system('Xvfb :1 -screen 0 1600x1200x16  &')    # create virtual display with size 1600x1200 and 16 bit color. Color can be changed to 24 or 8
os.environ['DISPLAY']=':1.0'    # tell X clients to use our virtual DISPLAY :1.0.
import tkinter as tk
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
    
    def tearDown(self):
        # Destroy the window created in the setUp method
        self.main_window.destroy()

    def test_next(self):
        self.countdown_timer.verifiedNames = ["person1","person2","person3","person4"]
        self.countdown_timer.timeIsOver = False
        # Test that the next method increments the index correctly
        self.countdown_timer.numberOfNamesLeft = 3
        self.countdown_timer.currentIndex = 1
        self.countdown_timer.next()
        self.assertEqual(self.countdown_timer.currentIndex, 2)
        self.countdown_timer.next()
        self.assertEqual(self.countdown_timer.currentIndex, 3)
"""
    def test_previous(self):
        # Test that the previous method decrements the index correctly
        self.countdown_timer.index = 2
        self.countdown_timer.previous()
        self.assertEqual(self.countdown_timer.index, 1)
        self.countdown_timer.previous()
        self.assertEqual(self.countdown_timer.index, 0)

    def test_format_time(self):
       # Test that the format_time method formats the time correctly
       self.assertEqual(self.countdown_timer.format_time(3661), "01:01:01")
       self.assertEqual(self.countdown_timer.format_time(3600), "01:00:00")
       self.assertEqual(self.countdown_timer.format_time(60), "00:01:00")
       self.assertEqual(self.countdown_timer.format_time(1), "00:00:01")

     def test_start_timer(self):
        # Test that the start_timer method starts the timer correctly
        self.countdown_timer.start_timer()
        self.assertEqual(self.countdown_timer.is_running, True)

    def test_stop_timer(self):
        # Test that the stop_timer method stops the timer correctly
        self.countdown_timer.stop_timer()
        self.assertEqual(self.countdown_timer.is_running, False)

    def test_reset_timer(self):
        # Test that the reset_timer method resets the timer correctly
        self.countdown_timer.reset_timer()
        self.assertEqual(self.countdown_timer.seconds, 0)
        self.assertEqual(self.countdown_timer.minutes, 0)
        self.assertEqual(self.countdown_timer.hours, 0)

    def test_time_is_over(self):
        # Test that the time_is_over method displays a message box when the timer runs out
        with self.assertRaises(messagebox.showinfo):
            self.countdown_timer.time_is_over() """

if __name__ == '__main__':
    unittest.main()
