import requests
import keyboard
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time

# Define the webhook URLs
webhook_url_1 = "https://webhook-url-2.com"
webhook_url_2 = "https://webhook-url-2.com"

barcode = ""  # Variable to store the barcode
scanning = False  # Flag to indicate if scanning is in progress
scanning_thread = None  # Reference to the scanning thread

# Flag to indicate if barcode confirmation is in progress
confirming_barcode = False

# Listen for barcode scanner input
def on_key_press(e):
    global barcode, confirming_barcode
    key = e.name

    # Append key value to barcode
    if key == "enter":
        if not confirming_barcode:
            confirming_barcode = True
            # Show alert to confirm barcode
            confirmed = messagebox.askyesno("Confirm Barcode", f"Is '{barcode}' the correct barcode?")
            if confirmed:
                send_to_webhook(barcode)
            else:
                print("Barcode not confirmed. Scan canceled.")
            barcode = ""  # Reset barcode for the next scan
            confirming_barcode = False
    else:
        barcode += key

    # Delay to differentiate consecutive key presses within a scan
    time.sleep(0.1)

# Send barcode data to the webhook
def send_to_webhook(barcode):
    payload = {"barcode": barcode}
    try:
        response = requests.post(webhook_url_1 if webhook_choice.get() == 1 else webhook_url_2, json=payload)
        response.raise_for_status()
        print("Barcode sent to webhook successfully!")
    except requests.exceptions.RequestException as e:
        print("Error sending barcode to webhook:", str(e))

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
    start_button_1.config(state=tk.DISABLED if scanning else tk.NORMAL)

# Function to show a message box with information
def show_info_message():
    messagebox.showinfo("Information", "Send Barcode Data to Webhook Endpoints. Scan Away")

# Create the GUI window
window = tk.Tk()
window.title("Barcode Scanner")
window.geometry("500x500")

# Create the "Start Scanning" buttons
start_button_1 = tk.Button(window, text="Start Scanning", command=start_scanning)
start_button_1.pack(pady=10)


# Function to confirm the barcode
def confirm_barcode():
    send_to_webhook(barcode)
    confirm_label.config(text="")
    confirm_buttons_frame.pack_forget()
    barcode = ""  # Reset barcode for the next scan
    confirming_barcode = False

# Function to cancel the scan
def cancel_scan():
    print("Barcode not confirmed. Scan canceled.")
    confirm_label.config(text="")
    confirm_buttons_frame.pack_forget()
    barcode = ""  # Reset barcode for the next scan
    confirming_barcode = False

# Create the "Info" button
info_button = tk.Button(window, text="Info", command=show_info_message)
info_button.pack(side=tk.BOTTOM, pady=10)

# Create a radio button group for webhook selection
webhook_choice = tk.IntVar(value=1)
radio_button_1 = tk.Radiobutton(window, text="Webhook 1", variable=webhook_choice, value=1)
radio_button_1.pack(anchor=tk.W)

radio_button_2 = tk.Radiobutton(window, text="Webhook 2", variable=webhook_choice, value=2)
radio_button_2.pack(anchor=tk.W)

# Keep the application running
window.mainloop()
