import tkinter as tk
import requests

def preprocess_license_plate(license_plate):
    # Remove any whitespace and convert to uppercase
    license_plate = license_plate.replace(" ", "").upper()
    # Remove hyphens if present
    license_plate = license_plate.replace("-", "")
    return license_plate

def fetch_vehicle_data():
    license_plate = license_plate_entry.get()
    if license_plate:
        license_plate = preprocess_license_plate(license_plate)
        try:
            url = f"https://opendata.rdw.nl/api/odata/v4/m9d7-ebf2?$filter=kenteken eq '{license_plate}'"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if data and 'value' in data and data['value']:
                global vehicle_data
                vehicle_data = data['value'][0]
                result_text.config(state=tk.NORMAL)
                result_text.delete(1.0, tk.END)
                result_text.config(state=tk.DISABLED)
                display_filter_options()  # Reset filter options
                apply_filter("Alles zien")  # Automatically show all data initially
            else:
                result_text.config(text="Geen data gevonden voor dit kenteken.")
        except requests.exceptions.RequestException as e:
            result_text.config(text=f"Fout bij het ophalen van data: {e}")
    else:
        result_text.config(text="Voer kentekennummer in:")

def display_filter_options():
    filter_label.config(text="Kies filter:", fg='white', bg='black')
    filter_label.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="w")

    # Define filter options
    filter_options = ["Alles zien", "Basis informatie", "Aanvullende data", "Datums"]

    # Create buttons for each filter option
    for i, option in enumerate(filter_options):
        padx_left = (5 if i != 0 else 120, 5)
        padx_right = (5, 120 if i != 3 else 5)
        filter_button = tk.Button(root, text=option, command=lambda op=option: apply_filter(op), bg='black', fg='white')
        filter_button.grid(row=3, column=i, padx=padx_left, pady=5, sticky="ew")

def apply_filter(option):
    if option == "Alles zien":
        display_vehicle_data(vehicle_data)
    else:
        if option in filter_mapping:
            display_filtered_data(option)
        else:
            result_text.config(text=f"Geen data beschikbaar voor {option}.")

def display_filtered_data(option):
    filter_text = ""
    relevant_data = filter_mapping[option]
    filtered_data = {label: vehicle_data.get(key, "N/A") for label, key in relevant_data.items()}
    
    # Split data into two columns
    half = len(filtered_data) // 2
    left_data = list(filtered_data.items())[:half]
    right_data = list(filtered_data.items())[half:]
    
    left_text = "\n".join(f"{label}: {format_value(label, value)}" for label, value in left_data)
    right_text = "\n".join(f"{label}: {format_value(label, value)}" for label, value in right_data)

    filter_text = f"{left_text}\n\n{right_text}"
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, filter_text)
    result_text.config(state=tk.DISABLED)

def display_vehicle_data(data):
    filtered_data = {
        key: format_value(key, value) if key in value_format_mapping else value
        for key, value in data.items()
        if key not in ["__id", "typegoedkeuringsnummer", "volgnummer_wijziging_eu_typegoedkeuring", "code_toelichting_tellerstandoordeel"]
        and not key.startswith("api_")
    }
    # Format license plate number with hyphens
    if 'kenteken' in filtered_data:
        filtered_data['kenteken'] = format_license_plate(filtered_data['kenteken'])

    # Split data into two columns
    half = len(filtered_data) // 2
    left_data = list(filtered_data.items())[:half]
    right_data = list(filtered_data.items())[half:]
    
    left_text = "\n".join(f"{key}: {value}" for key, value in left_data)
    right_text = "\n".join(f"{key}: {value}" for key, value in right_data)

    filter_text = f"{left_text}\n\n{right_text}"
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, filter_text)
    result_text.config(state=tk.DISABLED)

def format_date(date_str):
    if date_str and "T" in date_str:
        date_str = date_str.split("T")[0]
    if date_str and len(date_str) >= 8:
        # Add hyphens between the numbers if they are not already present
        if "-" not in date_str:
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        else:
            return date_str
    else:
        return date_str

def format_license_plate(license_plate):
    # Ensure the license plate is in the correct format
    license_plate = license_plate.upper().replace("-", "").replace(" ", "")
    return "-".join([license_plate[:2], license_plate[2:4], license_plate[4:]])

value_format_mapping = {
    "lengte": lambda value: f"{value} cm",
    "breedte": lambda value: f"{value} cm",
    "wielbasis": lambda value: f"{value} cm",
    "massa_ledig_voertuig": lambda value: f"{value} kg",
    "toegestane_maximum_massa_voertuig": lambda value: f"{value} kg",
    "massa_rijklaar": lambda value: f"{value} kg",
    "maximum_massa_trekken_ongeremd": lambda value: f"{value} kg",
    "maximum_trekken_massa_geremd": lambda value: f"{value} kg",
    "technische_max_massa_voertuig": lambda value: f"{value} kg",
    "maximum_massa_samenstelling": lambda value: f"{value} kg",
    "cilinderinhoud": lambda value: f"{value} liter",
    "bruto_bpm": lambda value: f"€{value}"
}

def format_value(key, value):
    if key in value_format_mapping:
        return value_format_mapping[key](value)
    return value

# Create the main Tkinter window
root = tk.Tk()
root.title("Kenteken Checker")
root.configure(bg='black')  # Set background color to black

# License plate input field
license_plate_label = tk.Label(root, text="Voer kentekennummer in:", fg='white', bg='black')
license_plate_label.grid(row=0, column=0, padx=10, pady=5)

license_plate_entry = tk.Entry(root)
license_plate_entry.grid(row=0, column=1, padx=10, pady=5)

# Button to fetch vehicle data
fetch_button = tk.Button(root, text="Zie voertuig data:", command=fetch_vehicle_data, bg='black', fg='white')
fetch_button.grid(row=1, column=0, columnspan=2, pady=5)

# Text widget to display results
result_text = tk.Text(root, wrap=tk.WORD, height=20, width=80, fg='white', bg='black', state=tk.DISABLED)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Label for filter options
filter_label = tk.Label(root, text="", fg='white', bg='black')

# Global variable to store fetched vehicle data
vehicle_data = None

# Dictionary to map filter options to relevant keys in vehicle_data
filter_mapping = {
    "Basis informatie": {
        "Kenteken": "kenteken",
        "Voertuigsoort": "voertuigsoort",
        "Merk": "merk",
        "Handelsbenaming": "handelsbenaming",
        "Inrichting": "inrichting",
        "Eerste kleur": "eerste_kleur",
        "Tweede kleur": "tweede_kleur",
        "Aantal deuren": "aantal_deuren",
        "Aantal zitplaatsen": "aantal_zitplaatsen",
        "Aantal cilinders": "aantal_cilinders",
        "Cilinderinhoud": "cilinderinhoud",
        "Massa ledig voertuig": "massa_ledig_voertuig",
        "Toegestane maximum massa voertuig": "toegestane_maximum_massa_voertuig",
        "Massa rijklaar": "massa_rijklaar",
        "Maximum massa trekken ongeremd": "maximum_massa_trekken_ongeremd",
        "Maximum trekken massa geremd": "maximum_trekken_massa_geremd",
        "Lengte": "lengte",
        "Breedte": "breedte",
        "Wielbasis": "wielbasis"
    },
    "Aanvullende data": {
        "Datum eerste toelating": "datum_eerste_toelating",
        "Datum eerste afgifte nederland": "datum_eerste_afgifte_nederland",
        "Bruto bpm": "bruto_bpm",
        "Inrichting": "inrichting",
        "Aantal deuren": "aantal_deuren",
        "Aantal wielen": "aantal_wielen",
        "Aantal zitplaatsen": "aantal_zitplaatsen",
        "Catalogusprijs": "catalogusprijs",
        "Datum eerste afgifte nederland": "datum_eerste_afgifte_nederland",
        "Vermogen massarijklaar": "vermogen_massarijklaar",
        "Toegestane maximum massa voertuig": "toegestane_maximum_massa_voertuig",
        "BPM bedrag": "bpm_bedrag",
        "Eerste kleur": "eerste_kleur",
        "Tweede kleur": "tweede_kleur",
        "Aantal cilinders": "aantal_cilinders",
        "Cilinderinhoud": "cilinderinhoud",
        "Massa ledig voertuig": "massa_ledig_voertuig",
        "Massa rijklaar": "massa_rijklaar",
        "Maximum massa trekken ongeremd": "maximum_massa_trekken_ongeremd",
        "Maximum trekken massa geremd": "maximum_trekken_massa_geremd",
        "Technische max massa voertuig": "technische_max_massa_voertuig",
        "Type": "type",
        "Wielbasis": "wielbasis"
    },
    "Datums": {
        "Datum eerste toelating": "datum_eerste_toelating",
        "Datum eerste afgifte nederland": "datum_eerste_afgifte_nederland",
        "Vervaldatum apk": "vervaldatum_apk",
        "Datum tenaamstelling": "datum_tenaamstelling",
        "Eerste kleur": "eerste_kleur",
        "Tweede kleur": "tweede_kleur",
        "BPM bedrag": "bpm_bedrag",
        "Bruto bpm": "bruto_bpm",
        "Massa rijklaar": "massa_rijklaar",
        "Massa ledig voertuig": "massa_ledig_voertuig",
        "Maximum massa trekken ongeremd": "maximum_massa_trekken_ongeremd",
        "Maximum trekken massa geremd": "maximum_trekken_massa_geremd",
        "Technische max massa voertuig": "technische_max_massa_voertuig",
        "Type": "type",
        "Wielbasis": "wielbasis"
    }
}

# Start the Tkinter main loop
root.mainloop()
