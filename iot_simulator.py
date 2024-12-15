import tkinter as tk
from tkinter import messagebox
import random

# Sensor class to simulate soil moisture sensor
class Sensor:
    def __init__(self):
        self.moisture_level = 50  # Initial soil moisture level (0-100)

    def update(self):
        # Simulate soil drying over time
        if self.moisture_level > 0:
            self.moisture_level -= random.randint(1, 5)
        return self.moisture_level

    def water(self):
        # Increase moisture when the pump is on
        self.moisture_level = min(100, self.moisture_level + 10)
        return self.moisture_level

# Actuator class to simulate the water pump
class Actuator:
    def __init__(self, sensor):
        self.sensor = sensor
        self.status = False  # False = Off, True = On

    def toggle(self):
        self.status = not self.status
        if self.status:
            self.sensor.water()

    def auto_mode(self):
        # Automatically turn on the pump when moisture level is too low
        if self.sensor.moisture_level < 30:
            self.toggle()

# GUI for controlling the IoT device
class IoTApp:
    def __init__(self, root):
        self.root = root
        self.sensor = Sensor()
        self.actuator = Actuator(self.sensor)
        self.mode = 'manual'  # Default mode is manual

        # Create UI components in English
        self.moisture_label = tk.Label(root, text="Soil Moisture: 50%", font=('Arial', 14))
        self.moisture_label.pack()

        self.toggle_button = tk.Button(root, text="Toggle Pump (Manual)", command=self.toggle_pump, font=('Arial', 12))
        self.toggle_button.pack()

        self.mode_button = tk.Button(root, text="Switch to Auto Mode", command=self.switch_mode, font=('Arial', 12))
        self.mode_button.pack()

        self.update_sensor()

    def update_sensor(self):
        # Update the sensor value periodically
        moisture = self.sensor.update()
        self.moisture_label.config(text=f"Soil Moisture: {moisture}%")

        if self.mode == 'auto':
            self.actuator.auto_mode()

        self.root.after(10000, self.update_sensor)  # Update every 10 seconds

    def toggle_pump(self):
        # Toggle the pump status manually
        self.actuator.toggle()
        if self.actuator.status:
            self.toggle_button.config(text="Stop Pump (Manual)")
        else:
            self.toggle_button.config(text="Toggle Pump (Manual)")

    def switch_mode(self):
        # Switch between manual and automatic modes
        if self.mode == 'manual':
            self.mode = 'auto'
            self.mode_button.config(text="Switch to Manual Mode")
            messagebox.showinfo("Mode", "Switched to Auto Mode")
        else:
            self.mode = 'manual'
            self.mode_button.config(text="Switch to Auto Mode")
            messagebox.showinfo("Mode", "Switched to Manual Mode")


# Run the Tkinter application
root = tk.Tk()
root.title("Smart Irrigation System")
app = IoTApp(root)
root.mainloop()
