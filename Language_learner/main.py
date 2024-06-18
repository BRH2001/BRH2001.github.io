from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown

class SpanishCharactersMenu(DropDown):
    def __init__(self, input_field, **kwargs):
        super().__init__(**kwargs)
        self.input_field = input_field
        self.create_buttons()

    def create_buttons(self):
        spanish_characters = ['á', 'é', 'í', 'ó', 'ú', 'ñ', '¡', '¿']
        for char in spanish_characters:
            btn = Button(text=char, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn, char=char: self.insert_character(char))
            self.add_widget(btn)

    def insert_character(self, char):
        self.input_field.insert_text(char)
        self.dismiss()

class WordQuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.word_pairs = [
            {'en': 'hello', 'es': 'hola'},
            {'en': 'goodbye', 'es': 'adiós'},
            {'en': 'thank you', 'es': 'gracias'},
            {'en': 'water', 'es': 'agua'},
            {'en': 'food', 'es': 'comida'}
        ]
        self.correct_count = 0
        self.incorrect_count = 0
        self.current_pair = None
        self.translation_input = TextInput(hint_text='Type the Spanish translation', multiline=False)
        self.translation_label = Label(text='', halign='center', font_size='20sp', size_hint_y=None, height=40)
        self.user_answer_label = Label(text='', halign='center', font_size='16sp', size_hint_y=None, height=40)
        self.spanish_characters_menu = SpanishCharactersMenu(self.translation_input)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.add_widget(layout)
        self.layout = layout

        self.generate_question()

    def generate_question(self):
        self.layout.clear_widgets()
        if self.word_pairs:
            self.current_pair = self.word_pairs.pop(0)
            question_label = Label(text=f"What is the Spanish translation of '{self.current_pair['en']}'?", font_size='20sp', size_hint_y=None, height=40)
            submit_button = Button(text='Submit', size_hint_y=None, height=50)
            submit_button.bind(on_press=self.check_answer)

            self.layout.add_widget(question_label)
            self.layout.add_widget(self.translation_input)
            self.layout.add_widget(submit_button)
            self.layout.add_widget(self.create_characters_button())
            self.layout.add_widget(self.user_answer_label)
            self.layout.add_widget(self.translation_label)

            # Add Back to Main Menu button
            back_to_menu_button = Button(text='Back to Main Menu', size_hint_y=None, height=50)
            back_to_menu_button.bind(on_press=self.go_to_main_menu)
            self.layout.add_widget(back_to_menu_button)
        else:
            self.show_summary(final=True)

    def create_characters_button(self):
        characters_button = Button(text='Spanish Characters', size_hint_y=None, height=50)
        characters_button.bind(on_release=self.spanish_characters_menu.open)
        return characters_button

    def check_answer(self, instance):
        user_answer = self.translation_input.text.strip().lower()
        correct_answer = self.current_pair['es'].strip().lower()

        self.user_answer_label.text = f'Your Answer: {user_answer}'

        if user_answer == correct_answer:
            self.translation_label.text = 'Correct!'
            self.correct_count += 1
        else:
            self.translation_label.text = f'Incorrect. Correct answer is "{self.current_pair["es"]}"'
            self.incorrect_count += 1

        if self.word_pairs:
            Clock.schedule_once(self.reset_quiz, 2)  # Delay reset to show feedback
        else:
            self.show_summary(final=True)

    def reset_quiz(self, dt):
        self.translation_input.text = ''
        self.user_answer_label.text = ''
        self.generate_question()

    def show_summary(self, final=False):
        self.layout.clear_widgets()
        summary_text = f'Quiz Finished!\nCorrect Answers: {self.correct_count}\nIncorrect Answers: {self.incorrect_count}'
        if final:
            last_answer_feedback = f'\nLast Question Feedback: {self.translation_label.text}'
            summary_text += last_answer_feedback

        summary_label = Label(
            text=summary_text,
            font_size='20sp', halign='center', size_hint_y=None, height=100
        )
        back_button = Button(text='Back to Main Menu', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_to_main_menu)

        self.layout.add_widget(summary_label)
        self.layout.add_widget(back_button)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'


class SentenceTranslateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sentences = [
            {'es': '¿Cómo estás?', 'en_options': ['How are you?', 'What is this?', 'Where are you?'], 'en_correct': 'How are you?'},
            {'es': 'Me gusta la música.', 'en_options': ['I like music.', 'The music is loud.', 'Do you like music?'], 'en_correct': 'I like music.'},
            {'es': 'Voy al supermercado.', 'en_options': ['I am going to the supermarket.', 'I went to the market.', 'He goes to the supermarket.'], 'en_correct': 'I am going to the supermarket.'}
        ]
        self.correct_count = 0
        self.incorrect_count = 0
        self.current_sentence = None
        self.translation_output = Label(text='', halign='center', font_size='20sp', size_hint_y=None, height=40)
        self.user_answer_label = Label(text='', halign='center', font_size='16sp', size_hint_y=None, height=40)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.add_widget(layout)
        self.layout = layout

        self.generate_question()

    def generate_question(self):
        self.layout.clear_widgets()
        if self.sentences:
            self.current_sentence = self.sentences.pop(0)
            question_label = Label(text=f"Translate the sentence into English:\n'{self.current_sentence['es']}'", font_size='20sp', size_hint_y=None, height=333)
            options_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)

            for option in self.current_sentence['en_options']:
                btn = Button(text=option, size_hint_y=None, height=50)
                btn.bind(on_press=self.check_answer)
                options_layout.add_widget(btn)

            self.layout.add_widget(question_label)
            self.layout.add_widget(options_layout)
            self.layout.add_widget(self.user_answer_label)
            self.layout.add_widget(self.translation_output)

            # Add Back to Main Menu button
            back_to_menu_button = Button(text='Back to Main Menu', size_hint_y=None, height=50)
            back_to_menu_button.bind(on_press=self.go_to_main_menu)
            self.layout.add_widget(back_to_menu_button)

    def check_answer(self, instance):
        user_answer = instance.text.strip()
        correct_answer = self.current_sentence['en_correct'].strip()

        self.user_answer_label.text = f'Your Answer: {user_answer}'

        if user_answer == correct_answer:
            self.translation_output.text = 'Correct!'
            self.correct_count += 1
        else:
            self.translation_output.text = f'Incorrect. Correct answer is "{self.current_sentence["en_correct"]}"'
            self.incorrect_count += 1

        if self.sentences:
            Clock.schedule_once(self.reset_quiz, 2)  # Delay reset to show feedback
        else:
            self.show_summary(final=True)

    def reset_quiz(self, dt):
        self.translation_output.text = ''
        self.user_answer_label.text = ''
        self.generate_question()

    def show_summary(self, final=False):
        self.layout.clear_widgets()
        summary_text = f'Quiz Finished!\nCorrect Answers: {self.correct_count}\nIncorrect Answers: {self.incorrect_count}'
        if final:
            last_answer_feedback = f'\nLast Question Feedback: {self.translation_output.text}'
            summary_text += last_answer_feedback

        summary_label = Label(
            text=summary_text,
            font_size='20sp', halign='center', size_hint_y=None, height=100
        )
        back_button = Button(text='Back to Main Menu', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_to_main_menu)

        self.layout.add_widget(summary_label)
        self.layout.add_widget(back_button)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=285)
        self.add_widget(layout)

        # Create buttons
        word_quiz_button = Button(text='Word Quiz', size_hint_y=None, height=50)
        sentence_translate_button = Button(text='Sentence Translation', size_hint_y=None, height=50)

        # Bind button actions
        word_quiz_button.bind(on_press=self.go_to_word_quiz)
        sentence_translate_button.bind(on_press=self.go_to_sentence_translate)

        # Add buttons to layout
        layout.add_widget(word_quiz_button)
        layout.add_widget(sentence_translate_button)

    def go_to_word_quiz(self, instance):
        self.manager.current = 'word_quiz'

    def go_to_sentence_translate(self, instance):
        self.manager.current = 'sentence_translate'


class Español_fácilApp(App):
    def build(self):
        screen_manager = ScreenManager()

        main_menu_screen = MainMenuScreen(name='main_menu')
        word_quiz_screen = WordQuizScreen(name='word_quiz')
        sentence_translate_screen = SentenceTranslateScreen(name='sentence_translate')
        screen_manager.add_widget(main_menu_screen)
        screen_manager.add_widget(word_quiz_screen)
        screen_manager.add_widget(sentence_translate_screen)

        return screen_manager


if __name__ == '__main__':
    Español_fácilApp().run()
