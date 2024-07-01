import math
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

# Input
def get_week_number():
    while True:
        week_number = int(input("Voer een weeknummer in tussen 0 en 54: "))
        if 0 <= week_number <= 54:
            return week_number
        print("Ongeldig weeknummer. Probeer het opnieuw.")

def get_active_chickens():
    while True:
        active_chickens = int(input(f"Voer het aantal actieve kippen in (tussen {MIN_CHICKENS} en {MAX_CHICKENS}): "))
        if MIN_CHICKENS <= active_chickens <= MAX_CHICKENS:
            return active_chickens
        print("Ongeldig aantal kippen. Probeer het opnieuw.")

week_number = get_week_number()
active_chickens = get_active_chickens()

# Calculations
total_eggs = active_chickens * EGGS_PER_CHICKEN_PER_WEEK
full_boxes = total_eggs // BOX_CAPACITY
leftover_eggs = total_eggs % BOX_CAPACITY
max_revenue = (full_boxes * (PRICE_PER_BOX + DEPOSIT_PER_BOX)) + (leftover_eggs * PRICE_PER_EGG)
total_hours = math.ceil(total_eggs / PROCESSING_RATE_PER_HOUR)
salary = total_hours * HOURLY_WAGE
personal_eggs_value = BONUS_EGGS * PRICE_PER_EGG
total_earnings = salary + personal_eggs_value

# Receipt
receipt = f"""
==========================
      Kassabon Week {week_number}
==========================
Totaal geproduceerde eieren: {total_eggs}
Volle doosjes: {full_boxes} x €{PRICE_PER_BOX} = €{full_boxes * PRICE_PER_BOX:.2f}
Statiegeld voor doosjes: {full_boxes} x €{DEPOSIT_PER_BOX} = €{full_boxes * DEPOSIT_PER_BOX:.2f}
Overgebleven eieren: {leftover_eggs} x €{PRICE_PER_EGG} = €{leftover_eggs * PRICE_PER_EGG:.2f} 
--------------------------
Totaal verkoopprijs: €{max_revenue:.2f}
--------------------------
Uurloon: {total_hours} uur x €{HOURLY_WAGE:.2f} = €{salary:.2f}
Bonus eieren: {BONUS_EGGS} x €{PRICE_PER_EGG:.2f} = €{personal_eggs_value:.2f}
--------------------------
Totale verdiensten: €{total_earnings:.2f}
==========================
"""

# Output
print(receipt)

# Save receipt to a file
with open(f"kassabon_week_{week_number}.txt", "w") as file:
    file.write(receipt)
