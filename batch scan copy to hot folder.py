import sys
import shutil
import tkinter as tk
from tkinter import messagebox
import keyboard
import time
from threading import Thread
import os
import sys
import random
import string

barcode = ""  # Variable to store the barcode
scanning = False  # Flag to indicate if scanning is in progress
scanning_thread = None  # Reference to the scanning thread
source_folders = {
    "Navy Jersey - White #": r"C:\\Users\\Owner\\Desktop\\DTF P RINTER\\1 soccer post\\7elite\\numbers\\white-navy",
    "Red Jersey - White #": r"C:\\Users\\Owner\\Desktop\\DTF P RINTER\\1 soccer post\\7elite\\numbers\\white-red",
    "White Jersey - Red #": r"C:\\Users\\Owner\\Desktop\\DTF P RINTER\\1 soccer post\\7elite\\numbers\\red-white",
    "Red Shorts - White #": r"C:\\Users\\Owner\\Desktop\\DTF P RINTER\\1 soccer post\\7elite\\numbers\\shorts",
    "Navy Shorts - White #": r"C:\\Users\\Owner\\Desktop\\DTF P RINTER\\1 soccer post\\7elite\\numbers\\shorts"

}  # Dictionary to store the source folders

# Listen for barcode scanner input
def on_key_press(e):
    global barcode
    key = e.name

    # Append key value to barcode
    if key == "enter":
        for folder_name, folder_path in source_folders.items():
            copy_file(barcode, folder_name)
        barcode = ""  # Reset barcode for the next scan
    else:
        barcode += key

    # Delay to differentiate consecutive key presses within a scan
    time.sleep(0.1)

# Copy file based on the barcode
def copy_file(barcode, folder_name):
    if folder_name in selected_folders:  # Check if the folder is selected
        x = barcode.rsplit('-', 1)[-1]
        src_folder = source_folders.get(folder_name)
        if src_folder is not None:
            src_path = f"{src_folder}\\Record-{x}.pdf"
            dst_folder = r"C:\Users\Owner\Desktop\DTF P RINTER\hot-folder"
            if os.path.exists(src_path):
                file_extension = ".pdf"
                random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
                dst_file_name = f"Record-{x}_{random_suffix}{file_extension}"
                dst_path = os.path.join(dst_folder, dst_file_name)
                shutil.copy(src_path, dst_path)
                print(f"File copied from {folder_name} successfully!")
                time.sleep(0.1)  # Add a delay of 0.5 seconds
            else:
                print(f"File not found in {folder_name} folder.")
        else:
            print(f"Invalid source folder selected: {folder_name}")
    else:
        print(f"Folder not selected: {folder_name}")

        
# Function to start the barcode scanning
def start_scanning():
    global scanning, scanning_thread
    if not scanning:
        scanning = True
        toggle_buttons_state()  # Disable buttons during scanning
        print("Scanning started...")
        # Create a new thread only if scanning is not already in progress
        scanning_thread = Thread(target=keyboard.on_press, args=(on_key_press,))
        scanning_thread.start()

# Function to toggle the state of buttons
def toggle_buttons_state():
    start_button.config(state=tk.DISABLED if scanning else tk.NORMAL)
    relaunch_button.config(state=tk.DISABLED if scanning else tk.NORMAL)

# Function to relaunch the application
def relaunch_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Create the GUI window
window = tk.Tk()
window.title("Barcode Scanner")
window.geometry("500x500")

# Create the title label for the barcode scanner
title_label = tk.Label(window, text="7 Elite Numbers Batch Mode", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

# Create the "Start Scanning" button
start_button = tk.Button(window, text="Start Scanning", command=start_scanning)
start_button.pack(pady=10)

# Create folder selection checkboxes
selected_folders = []

def select_folder(folder_name):
    if folder_name not in selected_folders:
        selected_folders.append(folder_name)
    else:
        selected_folders.remove(folder_name)

def update_folder_label():
    folder_label.config(text="Selected Folders: " + ", ".join(selected_folders))

folder_checkboxes = []
for folder_name, folder_path in source_folders.items():
    folder_checkbox = tk.Checkbutton(
        window,
        text=folder_name,
        font=("Arial", 12, "bold"),  # Specify the font properties here
        indicatoron=False,  # Remove the checkbox indicator
        width=30,  # Set the width of the buttons
        padx=10,  # Add horizontal padding
        pady=5,  # Add vertical padding
        command=lambda name=folder_name: select_folder(name),
        highlightthickness=3,  # Set the thickness of the border
        highlightbackground="red"  # Set the color of the border
    )
    folder_checkbox.configure(background="white", selectcolor="red")  # Set background color to white
    folder_checkbox.pack(anchor=tk.CENTER, padx=5, pady=3)  # Add spacing with padx and pady
    folder_checkboxes.append(folder_checkbox)

# Create a label to display the selected source folders
folder_label = tk.Label(window, text="Source Folders: ")
folder_label.pack(pady=10)

# Function to show a message box with information
def show_info_message():
    messagebox.showinfo("Information", "Scan barcode to copy the corresponding file")

# Create the "Info" button
info_button = tk.Button(window, text="Info", command=show_info_message)
info_button.pack(side=tk.LEFT, padx=5, pady=10)

# Create the "Relaunch" button
relaunch_button = tk.Button(window, text="Relaunch", command=relaunch_app)
relaunch_button.pack(side=tk.LEFT, padx=5, pady=10)

# Keep the application running
window.mainloop()
