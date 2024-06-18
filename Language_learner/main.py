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
            {'en': 'hello', 'es': 'hola'}, {'en': 'goodbye', 'es': 'adiós'},
            {'en': 'thank you', 'es': 'gracias'}, {'en': 'water', 'es': 'agua'},
            {'en': 'food', 'es': 'comida'}, {'en': 'house', 'es': 'casa'},
            {'en': 'book', 'es': 'libro'}, {'en': 'cat', 'es': 'gato'},
            {'en': 'dog', 'es': 'perro'}, {'en': 'day', 'es': 'día'},
            {'en': 'night', 'es': 'noche'}, {'en': 'sun', 'es': 'sol'},
            {'en': 'moon', 'es': 'luna'}, {'en': 'star', 'es': 'estrella'},
            {'en': 'car', 'es': 'coche'}, {'en': 'school', 'es': 'escuela'},
            {'en': 'teacher', 'es': 'maestro'}, {'en': 'student', 'es': 'estudiante'},
            {'en': 'friend', 'es': 'amigo'}, {'en': 'family', 'es': 'familia'},
            {'en': 'work', 'es': 'trabajo'}, {'en': 'love', 'es': 'amor'},
            {'en': 'life', 'es': 'vida'}, {'en': 'computer', 'es': 'computadora'},
            {'en': 'phone', 'es': 'teléfono'}, {'en': 'city', 'es': 'ciudad'},
            {'en': 'country', 'es': 'país'}, {'en': 'world', 'es': 'mundo'},
            {'en': 'travel', 'es': 'viajar'}, {'en': 'music', 'es': 'música'},
            {'en': 'movie', 'es': 'película'}, {'en': 'game', 'es': 'juego'},
            {'en': 'sport', 'es': 'deporte'}, {'en': 'exercise', 'es': 'ejercicio'},
            {'en': 'health', 'es': 'salud'}, {'en': 'doctor', 'es': 'doctor'},
            {'en': 'hospital', 'es': 'hospital'}, {'en': 'school', 'es': 'escuela'},
            {'en': 'university', 'es': 'universidad'}, {'en': 'language', 'es': 'idioma'},
            {'en': 'culture', 'es': 'cultura'}, {'en': 'food', 'es': 'comida'},
            {'en': 'drink', 'es': 'bebida'}, {'en': 'bread', 'es': 'pan'},
            {'en': 'coffee', 'es': 'café'}, {'en': 'tea', 'es': 'té'},
            {'en': 'water', 'es': 'agua'}, {'en': 'milk', 'es': 'leche'},
            {'en': 'juice', 'es': 'jugo'}, {'en': 'breakfast', 'es': 'desayuno'}
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
            {'es': 'Voy al supermercado.', 'en_options': ['I am going to the supermarket.', 'I went to the market.', 'He goes to the supermarket.'], 'en_correct': 'I am going to the supermarket.'},
            {'es': 'Ella tiene un perro.', 'en_options': ['She has a dog.', 'He has a dog.', 'She has a cat.'], 'en_correct': 'She has a dog.'},
            {'es': 'El libro es interesante.', 'en_options': ['The book is interesting.', 'The book is boring.', 'The book is old.'], 'en_correct': 'The book is interesting.'},
            {'es': 'La casa es grande.', 'en_options': ['The house is big.', 'The house is small.', 'The house is new.'], 'en_correct': 'The house is big.'},
            {'es': 'Tengo dos hermanos.', 'en_options': ['I have two brothers.', 'I have two sisters.', 'I have two friends.'], 'en_correct': 'I have two brothers.'},
            {'es': 'Nos gusta viajar.', 'en_options': ['We like to travel.', 'We like to eat.', 'We like to dance.'], 'en_correct': 'We like to travel.'},
            {'es': 'El cielo es azul.', 'en_options': ['The sky is blue.', 'The sky is cloudy.', 'The sky is red.'], 'en_correct': 'The sky is blue.'},
            {'es': 'Hace calor hoy.', 'en_options': ['It is hot today.', 'It is cold today.', 'It is raining today.'], 'en_correct': 'It is hot today.'},
            {'es': 'Estoy aprendiendo español.', 'en_options': ['I am learning Spanish.', 'I am learning English.', 'I am learning French.'], 'en_correct': 'I am learning Spanish.'},
            {'es': 'Necesito descansar.', 'en_options': ['I need to rest.', 'I need to work.', 'I need to eat.'], 'en_correct': 'I need to rest.'},
            {'es': 'Quiero una bebida.', 'en_options': ['I want a drink.', 'I want food.', 'I want sleep.'], 'en_correct': 'I want a drink.'},
            {'es': 'Mi cumpleaños es en julio.', 'en_options': ['My birthday is in July.', 'My birthday is in June.', 'My birthday is in August.'], 'en_correct': 'My birthday is in July.'},
            {'es': 'La película fue buena.', 'en_options': ['The movie was good.', 'The movie was bad.', 'The movie was okay.'], 'en_correct': 'The movie was good.'},
            {'es': 'Necesito ir al baño.', 'en_options': ['I need to go to the bathroom.', 'I need to go to the kitchen.', 'I need to go to the bedroom.'], 'en_correct': 'I need to go to the bathroom.'},
            {'es': 'El tren llega a tiempo.', 'en_options': ['The train arrives on time.', 'The train is late.', 'The train is early.'], 'en_correct': 'The train arrives on time.'},
            {'es': 'Voy a la playa.', 'en_options': ['I am going to the beach.', 'I am going to the park.', 'I am going to the city.'], 'en_correct': 'I am going to the beach.'},
            {'es': 'El perro está en el jardín.', 'en_options': ['The dog is in the garden.', 'The dog is in the house.', 'The dog is in the street.'], 'en_correct': 'The dog is in the garden.'},
            {'es': 'Ella trabaja en una oficina.', 'en_options': ['She works in an office.', 'She works in a school.', 'She works in a hospital.'], 'en_correct': 'She works in an office.'},
            {'es': 'El café está caliente.', 'en_options': ['The coffee is hot.', 'The coffee is cold.', 'The coffee is sweet.'], 'en_correct': 'The coffee is hot.'},
            {'es': 'Mi coche es rojo.', 'en_options': ['My car is red.', 'My car is blue.', 'My car is green.'], 'en_correct': 'My car is red.'},
            {'es': 'El niño está jugando.', 'en_options': ['The child is playing.', 'The child is sleeping.', 'The child is eating.'], 'en_correct': 'The child is playing.'},
            {'es': 'Tengo que estudiar.', 'en_options': ['I have to study.', 'I have to work.', 'I have to sleep.'], 'en_correct': 'I have to study.'},
            {'es': 'Me gusta leer libros.', 'en_options': ['I like to read books.', 'I like to write books.', 'I like to sell books.'], 'en_correct': 'I like to read books.'},
            {'es': 'La comida está deliciosa.', 'en_options': ['The food is delicious.', 'The food is terrible.', 'The food is cold.'], 'en_correct': 'The food is delicious.'},
            {'es': 'Hace frío en invierno.', 'en_options': ['It is cold in winter.', 'It is hot in winter.', 'It is raining in winter.'], 'en_correct': 'It is cold in winter.'},
            {'es': 'La ciudad es grande.', 'en_options': ['The city is big.', 'The city is small.', 'The city is quiet.'], 'en_correct': 'The city is big.'},
            {'es': 'Estoy feliz hoy.', 'en_options': ['I am happy today.', 'I am sad today.', 'I am tired today.'], 'en_correct': 'I am happy today.'},
            {'es': 'El gato está durmiendo.', 'en_options': ['The cat is sleeping.', 'The cat is eating.', 'The cat is playing.'], 'en_correct': 'The cat is sleeping.'},
            {'es': 'La puerta está cerrada.', 'en_options': ['The door is closed.', 'The door is open.', 'The door is locked.'], 'en_correct': 'The door is closed.'}
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
