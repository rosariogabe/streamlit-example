import csv
from gtts import gTTS
import os
import pronouncing

class TextToSpeechConverter:
    def __init__(self):
        self.name = None
        self.phonetic_spelling = None
        self.accent_options = {
            "American English": "en",
            "British English": "en-uk",
            "Australian English": "en-au",
            "Indian English": "en-in",
            "Spanish": "es",
            "Mexican Spanish": "es-mx",
            "French": "fr",
            "Canadian French": "fr-ca",
            "German": "de",
            "Italian": "it",
            "Japanese": "ja",
            "Portuguese": "pt",
            "Brazilian Portuguese": "pt-br",
            "Russian": "ru",
            "Chinese (Simplified)": "zh",
            "Chinese (Traditional)": "zh-tw",
            "Korean": "ko",
            "Arabic": "ar",
            # Add more accent options as needed
        }

    def prompt_user_for_name(self):
        self.name = input("What is your name: ")

    def get_phonetic_spelling(self):
        phonetic_spelling = pronouncing.phones_for_word(self.name)

        if phonetic_spelling:
            self.phonetic_spelling = ''.join(char for char in phonetic_spelling[0] if char.isalpha())
        else:
            print(f"we are unable to find the correct phonetic spelling for: {self.name}")
            user_input = input("Please enter the phonetic spelling manually: ")
            self.phonetic_spelling = user_input

    def display_phonetic_spelling(self):
        while True:
            print(f"Phonetic spelling for {self.name}: {self.phonetic_spelling}")
            user_input_approval = input(f'Are you happy with: {self.phonetic_spelling}? Yes/No: ')
            if user_input_approval.lower() == "yes":
                return user_input_approval
            elif user_input_approval.lower() == "no":
                new_phonetic_spelling = input("Please provide the correct phonetic spelling: ")
                self.phonetic_spelling = new_phonetic_spelling
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")

    def display_accent_options(self):
        print("Available accent options:")
        for idx, accent in enumerate(self.accent_options.keys(), start=1):
            print(f"{idx}. {accent}")

    def prompt_user_for_accent(self):
        selection = int(input("Enter the number corresponding to your desired accent: "))
        return list(self.accent_options.values())[selection - 1] if 1 <= selection <= len(self.accent_options) else None

    def convert_to_speech(self, selected_accent):
        tts = gTTS(text=self.name, lang=selected_accent)
        filename = f"{self.name}.mp3"
        tts.save(filename)
        os.system("start " + filename)

    def save_to_csv(self, selected_accent):
        data = [(self.name, self.phonetic_spelling, selected_accent)]
        filename = f"{self.name}_data.csv"

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Phonetic Spelling', 'Selected Accent'])
            writer.writerows(data)

        print(f"Data saved to {filename}.")

if __name__ == "__main__":
    converter = TextToSpeechConverter()

    converter.prompt_user_for_name()
    converter.get_phonetic_spelling()
    approval = converter.display_phonetic_spelling()

    converter.display_accent_options()
    selected_accent = converter.prompt_user_for_accent()



    if selected_accent and approval:
        converter.convert_to_speech(selected_accent)
        converter.save_to_csv(selected_accent)
    else:
        print("Invalid selection. Please choose a valid number.")
