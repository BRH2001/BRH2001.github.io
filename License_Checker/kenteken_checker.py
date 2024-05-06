import tkinter as tk
from rdw.rdw import Rdw

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
        car = Rdw()
        result = car.get_vehicle_data(license_plate)
        if result:
            global vehicle_data
            vehicle_data = result[0]
            display_filter_options()
        else:
            result_text.config(text="gefaald om data op te halen.") 
    else:
        result_text.config(text="voer kentekennummer in:")

def display_filter_options():
    filter_label.config(text="kies filter:", fg='white', bg='black')
    filter_label.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="w")

    # Define filter options
    filter_options = ["alles zien", "basis informatie", "aanvullende data", "Datums"]

    # Create buttons for each filter option
    for i, option in enumerate(filter_options):
        padx_left = (5 if i != 0 else 120, 5)
        padx_right = (5, 120 if i != 3 else 5)
        filter_button = tk.Button(root, text=option, command=lambda op=option: apply_filter(op))
        filter_button.grid(row=3, column=i, padx=padx_left, pady=5, sticky="ew")

def apply_filter(option):
    if option == "alles zien":
        display_vehicle_data(vehicle_data)
    else:
        if option in filter_mapping:
            display_filtered_data(option)
        else:
            result_text.config(text=f"geen data beschikbaar voor {option}.")

def display_filtered_data(option):
    filter_text = ""
    relevant_data = filter_mapping[option]
    for label, key in relevant_data.items():
        if key in vehicle_data:
            # Remove the time part from date fields
            value = vehicle_data[key]
            if "datum" in key:
                value = format_date(value)
            else:
                value = format_value(key, value)
            filter_text += f"{label}: {value}\n"
    result_text.config(text=filter_text)

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

def display_vehicle_data(data):
    filtered_data = {
        key: format_value(key, value) if key in value_format_mapping else value
        for key, value in data.items()
        if key not in ["typegoedkeuringsnummer", "volgnummer_wijziging_eu_typegoedkeuring", "code_toelichting_tellerstandoordeel"]
        and not key.startswith("api_")
    }
    # Format license plate number with hyphens
    if 'kenteken' in filtered_data:
        filtered_data['kenteken'] = format_license_plate(filtered_data['kenteken'])

    filter_text = ""
    for key, value in filtered_data.items():
        filter_text += f"{key}: {value}\n"
    result_text.config(text=filter_text)

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
root.title("kenteken checker")
root.configure(bg='black')  # Set background color to black

# License plate input field
license_plate_label = tk.Label(root, text="voer kentekennummer in:", fg='white', bg='black')
license_plate_label.grid(row=0, column=0, padx=10, pady=5)

license_plate_entry = tk.Entry(root)
license_plate_entry.grid(row=0, column=1, padx=10, pady=5)

# Button to fetch vehicle data
fetch_button = tk.Button(root, text="zie voertuig data:", command=fetch_vehicle_data, bg='black', fg='white')
fetch_button.grid(row=1, column=0, columnspan=2, pady=5)

# Text widget to display results
result_text = tk.Label(root, text="", justify="left", fg='white', bg='black')
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Label for filter options
filter_label = tk.Label(root, text="", fg='white', bg='black')

# Global variable to store fetched vehicle data
vehicle_data = None

# Dictionary to map filter options to relevant keys in vehicle_data
filter_mapping = {
    "basis informatie": {
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
        "Wielbasis": "wielbasis",
        "Technische maximum massa voertuig": "technische_max_massa_voertuig",
        "Variant": "variant",
        "Uitvoering": "uitvoering",
        "Vermogen massarijklaar": "vermogen_massarijklaar",
        "Aantal wielen": "aantal_wielen"
    },
    "Datums": {
        "Vervaldatum apk": "vervaldatum_apk_dt",
        "Datum tenaamstelling": "datum_tenaamstelling_dt",
        "Datum eerste toelating": "datum_eerste_toelating_dt",
        "Datum eerste tenaamstelling in Nederland": "datum_eerste_tenaamstelling_in_nederland_dt"
    },
    "aanvullende data": {
        "Bruto BPM": "bruto_bpm",
        "Plaats chassisnummer": "plaats_chassisnummer",
        "Europese voertuigcategorie": "europese_voertuigcategorie",
        "Wacht op keuren": "wacht_op_keuren",
        "WAM verzekerd": "wam_verzekerd",
        "Export indicator": "export_indicator",
        "Openstaande terugroepactie indicator": "openstaande_terugroepactie_indicator",
        "Taxi indicator": "taxi_indicator",
        "Maximum massa samenstelling": "maximum_massa_samenstelling",
        "Aantal rolstoelplaatsen": "aantal_rolstoelplaatsen",
        "Jaar laatste registratie tellerstand": "jaar_laatste_registratie_tellerstand",
        "Tellerstandoordeel": "tellerstandoordeel",
        "Tenaamstellen mogelijk": "tenaamstellen_mogelijk",
        "Zuinigheidsclassificatie": "zuinigheidsclassificatie"
    }
}

# Run the Tkinter event loop
root.mainloop()
