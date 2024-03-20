import requests
import os

def translate_text(input_text, source_lang, target_lang):
    api_url = "https://mymemory.translated.net/api/get"

    params = {
        'q': input_text,
        'langpair': f'{source_lang}|{target_lang}'
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        translation_data = response.json()
        translated_text = translation_data['responseData']['translatedText']
        return translated_text
    else:
        print(f"Error: {response.status_code}")
        return None

def translate_file(input_file, output_file, source_lang, target_lang):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        return

    translated_text = translate_text(input_text, source_lang, target_lang)

    if translated_text:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_text)
        print(f"Translation for {input_file} saved to {output_file}")
    else:
        print(f"Translation for {input_file} failed.")

def main():
    input_files = ["nl_text_1.txt", "nl_text_2.txt", "nl_text_3.txt"]
    source_lang = "nl"  # Dutch
    target_lang = "de"  # German

    for input_file in input_files:
        # Update output file names
        output_file = input_file.replace("nl_", "de_")
        
        # Translate and save the file
        translate_file(input_file, output_file, source_lang, target_lang)

        # Delete the old Dutch file
        try:
            os.remove(input_file)
            print(f"Deleted old file: {input_file}")
        except FileNotFoundError:
            print(f"Error: File {input_file} not found.")
        except Exception as e:
            print(f"Error while deleting {input_file}: {str(e)}")

if __name__ == "__main__":
    main()
