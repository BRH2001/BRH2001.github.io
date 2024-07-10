import math
import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import datetime

# Constants
EGGS_PER_CHICKEN_PER_WEEK = 5
BOX_CAPACITY = 12
PRICE_PER_BOX = 6.00
DEPOSIT_PER_BOX = 1.00
PRICE_PER_EGG = 1.00
PROCESSING_RATE_PER_HOUR = 1000
HOURLY_WAGE = 3.50
BONUS_EGGS = 10
MIN_CHICKENS = 2450
MAX_CHICKENS = 2525

# Functions
def calculate_receipt():
    try:
        week_number = int(week_entry.get())
        active_chickens = int(chickens_entry.get())

        if not (0 <= week_number <= 54):
            raise ValueError("Ongeldig weeknummer.")
        if not (MIN_CHICKENS <= active_chickens <= MAX_CHICKENS):
            raise ValueError("Ongeldig aantal kippen.")

        total_eggs = active_chickens * EGGS_PER_CHICKEN_PER_WEEK
        full_boxes = total_eggs // BOX_CAPACITY
        leftover_eggs = total_eggs % BOX_CAPACITY
        total_sales_price = (full_boxes * (PRICE_PER_BOX + DEPOSIT_PER_BOX)) + (leftover_eggs * PRICE_PER_EGG)
        total_hours = math.ceil(total_eggs / PROCESSING_RATE_PER_HOUR)  # Calculate total_hours
        salary = total_hours * HOURLY_WAGE
        personal_eggs_value = BONUS_EGGS * PRICE_PER_EGG
        total_earnings = salary + personal_eggs_value
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")

        # Simplified receipt for QR code
        qr_receipt = (
            f"============================\n"
            f"        KASSABON\n"
            f"============================\n"
            f"Datum: {current_date}\n"
            f"Week: {week_number}\n"
            f"Totaal eieren: {total_eggs}\n"
            f"Doosjes: {full_boxes}\n"
            f"Losse eieren: {leftover_eggs}\n"
            f"Totaalprijs: €{total_sales_price:.2f}\n"
            f"============================\n"
            f"Bedankt voor uw aankoop!\n"
            f"============================\n"
        )

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(qr_receipt.strip())
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((200, 200))  # Increase size for better readability
        qr_img_tk = ImageTk.PhotoImage(qr_img)

        # Update QR code label
        qr_code_label.configure(image=qr_img_tk)
        qr_code_label.image = qr_img_tk

        # Text for text areas
        omzet_berekening = (
            f"============================\n"
            f"   Omzet Berekening\n"
            f"============================\n"
            f"Datum: {current_date}\n"
            f"Week: {week_number}\n"
            f"Totaal geproduceerde eieren: {total_eggs}\n"
            f"Volle doosjes: {full_boxes} x €{PRICE_PER_BOX:.2f} = €{full_boxes * PRICE_PER_BOX:.2f}\n"
            f"Statiegeld voor doosjes: {full_boxes} x €{DEPOSIT_PER_BOX:.2f} = €{full_boxes * DEPOSIT_PER_BOX:.2f}\n"
            f"Overgebleven eieren: {leftover_eggs} x €{PRICE_PER_EGG:.2f} = €{leftover_eggs * PRICE_PER_EGG:.2f}\n"
            f"Totaal verkoopprijs: €{total_sales_price:.2f}\n"
        )

        loon_berekening = (
            f"============================\n"
            f"   Mijn Loon Berekening\n"
            f"============================\n"
            f"Datum: {current_date}\n"
            f"Week: {week_number}\n"
            f"Uurloon: {total_hours} uur x €{HOURLY_WAGE:.2f} = €{salary:.2f}\n"
            f"Bonus eieren: {BONUS_EGGS} x €{PRICE_PER_EGG:.2f} = €{personal_eggs_value:.2f}\n"
            f"Totale verdiensten: €{total_earnings:.2f}\n"
        )

        # Update the text areas
        omzet_text.delete(1.0, tk.END)
        omzet_text.insert(tk.END, omzet_berekening)

        loon_text.delete(1.0, tk.END)
        loon_text.insert(tk.END, loon_berekening)

        # Save the detailed receipt to a file
        full_receipt = f"{omzet_berekening}\n{loon_berekening}"
        with open(f"kassabon_week_{week_number}.txt", "w", encoding='utf-8') as file:
            file.write(full_receipt.strip())

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Ei productie rekenmachine")

# Set background color
bg_color = "#000000"  # Black background
fg_color = "#FFFFFF"  # White foreground for text
entry_bg_color = "#333333"  # Dark grey background for entry and text areas

root.configure(bg=bg_color)

# Week Number Input
tk.Label(root, text="Week Nummer:", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=10, pady=5, sticky='w')
week_entry = tk.Entry(root, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
week_entry.grid(row=0, column=0, columnspan=2, pady=10)

# Active Chickens Input
tk.Label(root, text="Actieve Kippen: (Tussen 2450-2525)", bg=bg_color, fg=fg_color).grid(row=1, column=0, padx=10, pady=5, sticky='w')
chickens_entry = tk.Entry(root, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
chickens_entry.grid(row=1, column=0, columnspan=2, pady=10)

# Calculate Button
calculate_button = tk.Button(root, text="Bereken Omzet en Loon", command=calculate_receipt, bg=entry_bg_color, fg=fg_color)
calculate_button.grid(row=2, column=0, columnspan=22, pady=10)

# Receipt Output
tk.Label(root, text="Omzet Berekening:", bg=bg_color, fg=fg_color).grid(row=3, column=0, padx=10, pady=5, sticky='w')
tk.Label(root, text="Mijn Loon Berekening:", bg=bg_color, fg=fg_color).grid(row=3, column=1, padx=10, pady=5, sticky='w')

omzet_text = tk.Text(root, width=40, height=15, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
omzet_text.grid(row=4, column=0, padx=10, pady=5)

loon_text = tk.Text(root, width=40, height=15, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
loon_text.grid(row=4, column=1, padx=10, pady=5)

# QR Code
qr_code_label = tk.Label(root, bg=bg_color)
qr_code_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
