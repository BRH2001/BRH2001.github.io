from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
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
            btn.bind(on_release=lambda btn: self.input_field.insert_text(btn.text))
            self.add_widget(btn)


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10)
        self.add_widget(layout)

        title_label = Label(text='Language Learner', font_size='24sp')
        layout.add_widget(title_label)

        word_quiz_button = Button(text='Word Quiz', size_hint=(None, None), size=(150, 50))
        word_quiz_button.bind(on_press=self.go_to_word_quiz)
        layout.add_widget(word_quiz_button)

        sentence_translate_button = Button(text='Sentence Translate', size_hint=(None, None), size=(150, 50))
        sentence_translate_button.bind(on_press=self.go_to_sentence_translate)
        layout.add_widget(sentence_translate_button)

    def go_to_word_quiz(self, instance):
        self.manager.current = 'word_quiz'

    def go_to_sentence_translate(self, instance):
        self.manager.current = 'sentence_translate'


class WordQuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.word_pairs = [
            {'en': 'hello', 'es': 'hola'},
            {'en': 'goodbye', 'es': 'adiós'}
        ]
        self.current_pair = None
        self.translation_input = TextInput(hint_text='Type the Spanish translation', multiline=False)
        self.translation_label = Label(text='', halign='center', font_size='20sp')
        self.spanish_characters_menu = SpanishCharactersMenu(self.translation_input)

        layout = BoxLayout(orientation='vertical', spacing=10)
        self.add_widget(layout)

        self.generate_question(layout)

    def generate_question(self, layout):
        if self.word_pairs:
            self.current_pair = self.word_pairs.pop(0)
            question_label = Label(text=f"What is the Spanish translation of '{self.current_pair['en']}'?", font_size='20sp')
            submit_button = Button(text='Submit', size_hint=(None, None), size=(100, 50))
            submit_button.bind(on_press=self.check_answer)

            layout.clear_widgets()
            layout.add_widget(question_label)
            layout.add_widget(self.translation_input)
            layout.add_widget(submit_button)
            layout.add_widget(self.create_characters_button())

    def create_characters_button(self):
        characters_button = Button(text='Spanish Characters', size_hint=(None, None), size=(150, 50))
        characters_button.bind(on_release=self.spanish_characters_menu.open)
        return characters_button

    def check_answer(self, instance):
        user_answer = self.translation_input.text.strip().lower()
        correct_answer = self.current_pair['es'].strip().lower()

        if user_answer == correct_answer:
            self.translation_label.text = 'Correct!'
        else:
            self.translation_label.text = f'Incorrect. Correct answer is "{self.current_pair["es"]}"'

        self.parent.add_widget(self.translation_label)
        self.generate_question(self.parent)

    def reset_quiz(self):
        self.word_pairs = [
            {'en': 'hello', 'es': 'hola'},
            {'en': 'goodbye', 'es': 'adiós'}
        ]
        self.translation_input.text = ''
        self.translation_label.text = ''
        self.generate_question(self.parent)


class SentenceTranslateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sentences = [
            {'es': '¿Cómo estás?', 'en_options': ['How are you?', 'What is this?', 'Where are you?'], 'en_correct': 'How are you?'}
        ]
        self.current_sentence = None
        self.translation_output = Label(text='', halign='center', font_size='20sp')

        layout = BoxLayout(orientation='vertical', spacing=10)
        self.add_widget(layout)

        self.generate_question(layout)

    def generate_question(self, layout):
        if self.sentences:
            self.current_sentence = self.sentences.pop(0)
            question_label = Label(text=f"Translate the sentence into English:", font_size='20sp')
            options_layout = BoxLayout(orientation='vertical', spacing=5)

            for option in self.current_sentence['en_options']:
                btn = Button(text=option, size_hint=(None, None), size=(200, 50))
                btn.bind(on_press=self.check_answer)
                options_layout.add_widget(btn)

            layout.clear_widgets()
            layout.add_widget(question_label)
            layout.add_widget(options_layout)

    def check_answer(self, instance):
        user_answer = instance.text.strip()
        correct_answer = self.current_sentence['en_correct'].strip()

        if user_answer == correct_answer:
            self.translation_output.text = 'Correct!'
        else:
            self.translation_output.text = f'Incorrect. Correct answer is "{self.current_sentence["en_correct"]}"'

        self.parent.add_widget(self.translation_output)
        self.generate_question(self.parent)

    def reset_quiz(self):
        self.sentences = [
            {'es': '¿Cómo estás?', 'en_options': ['How are you?', 'What is this?', 'Where are you?'], 'en_correct': 'How are you?'}
        ]
        self.translation_output.text = ''
        self.generate_question(self.parent)


class LanguageLearningApp(App):
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
    LanguageLearningApp().run()
