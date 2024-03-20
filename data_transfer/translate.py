import os
import requests
import langid


class Translate:

    def __init__(self):
        """Defines assets used in this class"""
        self.input_files = []

    def _translate_text(self, target_lang):
        """Translate the contents of the file"""
        api_url = "https://mymemory.translated.net/api/get"
        source_lang = langid.classify(self.input_text)[0]

        params = {
            'q': self.input_text,
            'langpair': f'{source_lang}|{target_lang}'
        }

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            translation_data = response.json()
            self.translated_text = translation_data['responseData']['translatedText']
        else:
            print(f"Error: {response.status_code}")
            return None

    def _read_file(self, input_file):
        """Reads the file you want to translate"""
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                self.input_text = file.read()
        except FileNotFoundError:
            print(f"Error: File {input_file} not found.")
            return

    def _save_translated_file(self, input_file, output_file):
        """Saves the translated text to a new file"""
        if self.translated_text:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(self.translated_text)
            print(f"Translation for {input_file} saved to {output_file}")
        else:
            print(f"Translation for {input_file} failed.")

    def _find_text_files(self):
        """Finds all text files and puts then into a list, making sure to exclude encrypted files"""
        files = os.listdir()
        for f in files:
            if "text" in f and "encrypted" not in f:
                self.input_files.append(f)

    def translate(self, target_lang):
        self._find_text_files()
        for i, input_file in enumerate(self.input_files):
            output_file = f"{target_lang}_text_{i + 1}.txt"
            self._read_file(input_file)
            self._translate_text(target_lang)
            self._save_translated_file(input_file, output_file)


if __name__ == "__main__":
    nl_de = Translate()
    nl_de.translate("de")
