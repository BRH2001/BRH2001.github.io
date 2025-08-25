import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
import sqlite3
import pdb
from datetime import datetime

class CertiportTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Certiport Python Certification Trainer Pro")
        self.root.geometry("1000x800")
        self.current_user = None  # Initialize current_user first
        self.setup_database()
        self.setup_style()
        self.create_main_menu()
        
    def setup_database(self):
        self.conn = sqlite3.connect('certiport_trainer.db')
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                progress TEXT,
                last_login TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                topic TEXT,
                score INTEGER,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        self.conn.commit()
    
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.configure('Title.TLabel', font=('Helvetica', 18, 'bold'), 
                       background='#f5f5f5', foreground='#2c3e50')
        style.configure('Question.TLabel', font=('Helvetica', 12), 
                       background='#f5f5f5', wraplength=850)
        style.configure('Correct.TButton', foreground='green')
        style.configure('Incorrect.TButton', foreground='red')
        style.configure('Score.TLabel', font=('Helvetica', 12, 'bold'), 
                       background='#f5f5f5', foreground='#2c3e50')
        style.configure('Header.TFrame', background='#3498db')
        style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'), 
                       background='#3498db', foreground='white')
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_header(self, title):
        header = ttk.Frame(self.root, style='Header.TFrame')
        header.pack(fill=tk.X, pady=(0, 20))
        
        if hasattr(self, 'current_user') and self.current_user:
            user_label = ttk.Label(header, text=f"User: {self.current_user}", 
                                 style='Header.TLabel')
            user_label.pack(side=tk.LEFT, padx=10)
        
        title_label = ttk.Label(header, text=title, style='Header.TLabel')
        title_label.pack(side=tk.LEFT, expand=True)
        
        home_btn = ttk.Button(header, text="Home", command=self.create_main_menu)
        home_btn.pack(side=tk.RIGHT, padx=10)
        
        return header
    
    def create_main_menu(self):
        self.clear_frame()
        self.create_header("Certiport Python Certification Trainer")
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # User authentication section
        auth_frame = ttk.Frame(main_frame)
        auth_frame.pack(pady=10)
        
        if not self.current_user:
            ttk.Label(auth_frame, text="Welcome! Please login or register:").pack()
            
            auth_btn_frame = ttk.Frame(auth_frame)
            auth_btn_frame.pack(pady=5)
            
            ttk.Button(auth_btn_frame, text="Login", 
                      command=self.show_login).pack(side=tk.LEFT, padx=5)
            ttk.Button(auth_btn_frame, text="Register", 
                      command=self.show_register).pack(side=tk.LEFT, padx=5)
        else:
            ttk.Label(auth_frame, 
                     text=f"Welcome back, {self.current_user}!").pack()
            ttk.Button(auth_frame, text="Logout", 
                      command=self.logout).pack(pady=5)
        
        # Main menu options
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(pady=20)
        
        topics = [
            ("Python Fundamentals", self.python_fundamentals),
            ("Control Flow", self.control_flow),
            ("Data Collections", self.data_collections),
            ("Modular Programming", self.modular_programming),
            ("Files & Exceptions", self.files_exceptions),
            ("Object-Oriented Programming", self.oop),
            ("Practice Test", self.practice_test),
            ("Code Playground", self.code_playground),
            ("Progress Dashboard", self.show_progress),
            ("Community Forum", self.open_forum),
            ("Exit", self.root.quit)
        ]
        
        for i, (text, command) in enumerate(topics):
            btn = ttk.Button(menu_frame, text=text, command=command, width=30)
            btn.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        
        # Add some padding between buttons
        menu_frame.grid_columnconfigure(0, weight=1)
        menu_frame.grid_columnconfigure(1, weight=1)
    
    def show_login(self):
        self.clear_frame()
        self.create_header("Login")
        
        login_frame = ttk.Frame(self.root)
        login_frame.pack(pady=20)
        
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        username_entry = ttk.Entry(login_frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(login_frame)
        btn_frame.grid(row=2, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Login", 
                  command=lambda: self.login(username_entry.get(), password_entry.get())).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", 
                  command=self.create_main_menu).pack(side=tk.LEFT, padx=5)
    
    def show_register(self):
        self.clear_frame()
        self.create_header("Register")
        
        register_frame = ttk.Frame(self.root)
        register_frame.pack(pady=20)
        
        ttk.Label(register_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        username_entry = ttk.Entry(register_frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(register_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(register_frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(register_frame, text="Confirm Password:").grid(row=2, column=0, padx=5, pady=5)
        confirm_entry = ttk.Entry(register_frame, show="*")
        confirm_entry.grid(row=2, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(register_frame)
        btn_frame.grid(row=3, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Register", 
                  command=lambda: self.register(
                      username_entry.get(), 
                      password_entry.get(), 
                      confirm_entry.get()
                  )).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", 
                  command=self.create_main_menu).pack(side=tk.LEFT, padx=5)
    
    def login(self, username, password):
        # In a real application, you would hash the password and verify it
        self.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        
        if user:
            self.current_user = username
            self.cursor.execute(
                "UPDATE users SET last_login=? WHERE username=?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Login successful!")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self, username, password, confirm_password):
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        try:
            self.cursor.execute(
                "INSERT INTO users (username, progress, last_login) VALUES (?, ?, ?)",
                (username, "{}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.create_main_menu()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
    
    def logout(self):
        self.current_user = None
        self.create_main_menu()
    
def run_quiz(self, questions, topic=None):
    self.clear_frame()
    self.create_header(f"Quiz: {topic}" if topic else "Practice Test")
    
    self.current_question = 0
    self.score = 0
    self.questions = random.sample(questions, min(len(questions), 10))
    self.current_topic = topic
    
    main_frame = ttk.Frame(self.root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Question and options frame
    quiz_frame = ttk.Frame(main_frame)
    quiz_frame.pack(fill=tk.BOTH, expand=True)
    
    self.question_label = ttk.Label(quiz_frame, style='Question.TLabel')
    self.question_label.pack(pady=10, anchor='w')
    
    self.option_buttons = []
    for i in range(4):
        btn = ttk.Button(quiz_frame, command=lambda i=i: self.check_answer(i+1))
        btn.pack(fill=tk.X, pady=5)
        self.option_buttons.append(btn)
    
    # REMOVE THIS ENTIRE DEBUG FRAME SECTION FROM run_quiz()
    # -----------------------------------------------------
    # Debug and code execution frame
    # debug_frame = ttk.LabelFrame(main_frame, text="Code Debugger")
    # debug_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    # 
    # code_text = scrolledtext.ScrolledText(debug_frame, width=80, height=10)
    # code_text.pack(fill=tk.BOTH, expand=True)
    # 
    # debug_btn_frame = ttk.Frame(debug_frame)
    # debug_btn_frame.pack(fill=tk.X, pady=5)
    # 
    # ttk.Button(debug_btn_frame, text="Run Code", 
    #           command=lambda: self.execute_code(code_text.get("1.0", tk.END))).pack(side=tk.LEFT, padx=5)
    # ttk.Button(debug_btn_frame, text="Debug Code", 
    #           command=lambda: self.debug_code(code_text.get("1.0", tk.END))).pack(side=tk.LEFT, padx=5)
    # -----------------------------------------------------
    
    # Bottom frame with navigation and score
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(fill=tk.X, pady=10)
    
    self.score_label = ttk.Label(bottom_frame, style='Score.TLabel')
    self.score_label.pack(side=tk.LEFT, padx=10)
    
    btn_frame = ttk.Frame(bottom_frame)
    btn_frame.pack(side=tk.RIGHT)
    
    self.next_button = ttk.Button(btn_frame, text="Next", 
                                command=self.next_question, state=tk.DISABLED)
    self.next_button.pack(side=tk.LEFT, padx=5)
    
    ttk.Button(btn_frame, text="Back to Menu", 
              command=self.create_main_menu).pack(side=tk.LEFT, padx=5)
    
    self.show_question()
    
    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.config(text=f"Question {self.current_question + 1}: {question['question']}")
            
            for i, option in enumerate(question["options"]):
                self.option_buttons[i].config(text=option, state=tk.NORMAL, style='TButton')
            
            self.score_label.config(text=f"Score: {self.score}/{len(self.questions)}")
            self.next_button.config(state=tk.DISABLED)
        else:
            self.show_results()
    
    def check_answer(self, selected_option):
        question = self.questions[self.current_question]
        correct_answer = question["answer"]
        
        for i, btn in enumerate(self.option_buttons):
            btn.config(state=tk.DISABLED)
            if i+1 == correct_answer:
                btn.config(style='Correct.TButton')
            elif i+1 == selected_option and selected_option != correct_answer:
                btn.config(style='Incorrect.TButton')
        
        if selected_option == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", question["explanation"])
        else:
            messagebox.showerror("Incorrect", 
                               f"Correct answer was option {correct_answer}\n\n{question['explanation']}")
        
        self.score_label.config(text=f"Score: {self.score}/{len(self.questions)}")
        self.next_button.config(state=tk.NORMAL)
        
        # Save progress if user is logged in
        if self.current_user and self.current_topic:
            self.cursor.execute(
                "INSERT INTO scores (user_id, topic, score, date) VALUES (?, ?, ?, ?)",
                (self.get_user_id(), self.current_topic, self.score, datetime.now().strftime("%Y-%m-%d"))
            )
            self.conn.commit()
    
    def next_question(self):
        self.current_question += 1
        self.show_question()
    
    def show_results(self):
        percentage = (self.score / len(self.questions)) * 100
        result = "Pass! 🎉" if percentage >= 70 else "Needs More Practice 📚"
        
        messagebox.showinfo("Test Complete",
                          f"Final Score: {self.score}/{len(self.questions)} ({percentage:.1f}%)\n\n{result}")
        self.create_main_menu()
    
    def execute_code(self, code):
        try:
            # Create a new window for code output
            output_window = tk.Toplevel(self.root)
            output_window.title("Code Execution Result")
            output_window.geometry("600x400")
            
            output_text = scrolledtext.ScrolledText(output_window, width=80, height=20)
            output_text.pack(fill=tk.BOTH, expand=True)
            
            # Redirect stdout to the output text widget
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            
            try:
                exec(code)
            except Exception as e:
                output_text.insert(tk.END, f"Error: {str(e)}\n")
            finally:
                sys.stdout = old_stdout
            
            output_text.insert(tk.END, mystdout.getvalue())
            output_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred: {str(e)}")
    
    def debug_code(self, code):
        try:
            # Create a new window for debugging
            debug_window = tk.Toplevel(self.root)
            debug_window.title("Code Debugger")
            debug_window.geometry("800x600")
            
            # Create a text widget with the code
            code_text = scrolledtext.ScrolledText(debug_window, width=80, height=20)
            code_text.pack(fill=tk.BOTH, expand=True)
            code_text.insert(tk.END, code)
            code_text.config(state=tk.DISABLED)
            
            # Create a console-like output widget
            console_frame = ttk.Frame(debug_window)
            console_frame.pack(fill=tk.BOTH, expand=True)
            
            console_label = ttk.Label(console_frame, text="Debug Console:")
            console_label.pack(anchor='w')
            
            console_text = scrolledtext.ScrolledText(console_frame, width=80, height=10)
            console_text.pack(fill=tk.BOTH, expand=True)
            
            # Debug controls
            control_frame = ttk.Frame(debug_window)
            control_frame.pack(fill=tk.X, pady=5)
            
            ttk.Button(control_frame, text="Step", 
                      command=lambda: self.debug_step(console_text)).pack(side=tk.LEFT, padx=5)
            ttk.Button(control_frame, text="Continue", 
                      command=lambda: self.debug_continue(console_text)).pack(side=tk.LEFT, padx=5)
            ttk.Button(control_frame, text="Quit", 
                      command=debug_window.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Debug Error", f"An error occurred: {str(e)}")
    
    def debug_step(self, console_widget):
        # Simplified debug step functionality
        console_widget.insert(tk.END, "Debugging step executed...\n")
        console_widget.see(tk.END)
    
    def debug_continue(self, console_widget):
        # Simplified debug continue functionality
        console_widget.insert(tk.END, "Debugging continued...\n")
        console_widget.see(tk.END)
    
    def code_playground(self):
        self.clear_frame()
        self.create_header("Code Playground")
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Code editor
        editor_frame = ttk.LabelFrame(main_frame, text="Python Code Editor")
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        code_editor = scrolledtext.ScrolledText(editor_frame, width=80, height=20)
        code_editor.pack(fill=tk.BOTH, expand=True)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="Run Code", 
                  command=lambda: self.execute_code(code_editor.get("1.0", tk.END))).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Debug Code", 
                  command=lambda: self.debug_code(code_editor.get("1.0", tk.END))).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear", 
                  command=lambda: code_editor.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Back to Menu", 
                  command=self.create_main_menu).pack(side=tk.RIGHT, padx=5)
        
        # Example code snippets
        example_frame = ttk.LabelFrame(main_frame, text="Example Code Snippets")
        example_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        examples = {
            "List Comprehension": "[x**2 for x in range(10) if x % 2 == 0]",
            "Dictionary": "my_dict = {'a': 1, 'b': 2}\nfor key, value in my_dict.items():\n    print(f'{key}: {value}')",
            "Class Example": "class MyClass:\n    def __init__(self, value):\n        self.value = value\n\nobj = MyClass(10)\nprint(obj.value)"
        }
        
        for name, code in examples.items():
            btn = ttk.Button(example_frame, text=name, 
                            command=lambda c=code: code_editor.insert(tk.END, c))
            btn.pack(side=tk.LEFT, padx=5)
    
    def show_progress(self):
        self.clear_frame()
        self.create_header("Your Progress")
        
        if not self.current_user:
            messagebox.showinfo("Info", "Please login to view your progress")
            self.create_main_menu()
            return
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Progress summary
        summary_frame = ttk.LabelFrame(main_frame, text="Progress Summary")
        summary_frame.pack(fill=tk.X, pady=10)
        
        user_id = self.get_user_id()
        self.cursor.execute(
            "SELECT topic, MAX(score), COUNT(*) FROM scores WHERE user_id=? GROUP BY topic",
            (user_id,)
        )
        results = self.cursor.fetchall()
        
        if not results:
            ttk.Label(summary_frame, text="No quiz results yet. Take some quizzes!").pack()
        else:
            for topic, max_score, count in results:
                ttk.Label(summary_frame, 
                         text=f"{topic}: Highest Score {max_score}/10 (Taken {count} times)").pack(anchor='w')
        
        # Recent activity
        activity_frame = ttk.LabelFrame(main_frame, text="Recent Activity")
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.cursor.execute(
            "SELECT topic, score, date FROM scores WHERE user_id=? ORDER BY date DESC LIMIT 5",
            (user_id,)
        )
        recent = self.cursor.fetchall()
        
        if not recent:
            ttk.Label(activity_frame, text="No recent activity").pack()
        else:
            for topic, score, date in recent:
                ttk.Label(activity_frame, 
                         text=f"{date}: {topic} - Score {score}/10").pack(anchor='w')
        
        ttk.Button(main_frame, text="Back to Menu", 
                  command=self.create_main_menu).pack(pady=10)
    
    def open_forum(self):
        webbrowser.open("https://example.com/certiport-forum")
    
    def get_user_id(self):
        if not self.current_user:
            return None
        self.cursor.execute("SELECT id FROM users WHERE username=?", (self.current_user,))
        return self.cursor.fetchone()[0]
    
    # Quiz content methods
    def python_fundamentals(self):
        questions = [
            {
                "question": "Which of the following is NOT a valid Python data type?",
                "options": ["1. int", "2. float", "3. char", "4. str"],
                "answer": 3,
                "explanation": "Python doesn't have a primitive 'char' type like some other languages. Single characters are just strings of length 1."
            },
            {
                "question": "What is the output of: print(3 * 'ab' + 'c')?",
                "options": ["1. 'abababc'", "2. '3abc'", "3. Error", "4. 'abcabcabc'"],
                "answer": 1,
                "explanation": "In Python, multiplying a string by an integer repeats the string. So 3 * 'ab' becomes 'ababab', then adding 'c' gives 'abababc'."
            },
            {
                "question": "What is the output of: print(3 * 'a' + 'b' * 2)?",
                "options": ["1. 'aaabb'", "2. 'aaabbb'", "3. Error", "4. 'aaab'"],
                "answer": 2,
                "explanation": "First, 'a' is repeated 3 times to become 'aaa'. Then 'b' is repeated 2 times to become 'bb'. Finally, 'aaa' + 'bb' gives 'aaabbb'."
            },
            {
                "question": "What is the difference between the * and ** operators in Python?",
                "options": [
                    "1. * multiplies two numbers, ** is a bitwise operator",
                    "2. * repeats a string, ** is used for exponentiation",
                    "3. Both are used for arithmetic operations",
                    "4. * is used for list unpacking, ** for keyword arguments"
                ],
                "answer": 2,
                "explanation": "* is used to repeat a string, while ** is used for exponentiation. For example, 2 ** 3 = 8."
            }
        ]
        self.run_quiz(questions, "Python Fundamentals")
    
    def control_flow(self):
        questions = [
            {
                "question": "What does this code output?\nx = 5\nwhile x > 0:\n    x -= 1\n    if x == 2:\n        break\n    print(x)\nprint('Done')",
                "options": ["1. 4\n3\nDone", "2. 4\n3\n2\n1\n0\nDone", "3. 4\n3\n2\nDone", "4. 4\n3\nDone"],
                "answer": 4,
                "explanation": "The loop starts at x=5. First iteration: x becomes 4 and prints. Second iteration: x becomes 3 and prints. Third iteration: x becomes 2, hits the break, and exits the loop without printing 2. Then 'Done' prints."
            },
            {
                "question": "Which loop is best when you know exactly how many iterations you need?",
                "options": ["1. for loop", "2. while loop", "3. nested loop", "4. recursive function"],
                "answer": 1,
                "explanation": "A for loop is ideal when you know the exact number of iterations needed, especially when used with range()."
            },
            {
                "question": "What does this code output?\ni = 0\nwhile i < 5:\n    print(i)\n    i += 1\nprint('Done')",
                "options": ["1. 0 1 2 3 4", "2. 0 1 2 3 4 5", "3. 0 1 2 3 4", "4. 0 1 2 3 4 5 6"],
                "answer": 1,
                "explanation": "The loop runs from i=0 to i=4, printing each value and incrementing i by 1. The final print statement prints 'Done'."
            },
            {
                "question": "What is the difference between a break and a continue statement in a loop?",
                "options": [
                    "1. break exits the loop, continue skips the current iteration",
                    "2. break and continue do the same thing",
                    "3. break skips the current iteration, continue exits the loop",
                    "4. continue exits the loop, break skips the current iteration"
                ],
                "answer": 1,
                "explanation": "break exits the loop entirely, while continue skips the current iteration and moves to the next one."
            }
        ]
        self.run_quiz(questions, "Control Flow")
    
    def data_collections(self):
        questions = [
            {
                "question": "What is the output of: print([x*2 for x in [1, 2, 3] if x > 1][1])",
                "options": ["1. 2", "2. 4", "3. 6", "4. Error"],
                "answer": 3,
                "explanation": "The list comprehension filters numbers >1 (2,3), multiplies by 2 (4,6), then takes index 1 which is 6."
            },
            {
                "question": "Which collection type is unordered and doesn't allow duplicates?",
                "options": ["1. list", "2. tuple", "3. set", "4. dictionary"],
                "answer": 3,
                "explanation": "Sets are unordered collections of unique elements."
            },
            {
                "question": "What is the output of: print(list(range(5, 0, -1)))",
                "options": ["1. [5, 4, 3, 2, 1]", "2. [5, 4, 3, 2, 1, 0]", "3. [5, 4, 3, 2]", "4. Error"],
                "answer": 1,
                "explanation": "range(5, 0, -1) generates numbers from 5 to 1 (inclusive) in reverse order."
            },
            {
                "question": "What is the difference between a list and a tuple in Python?",
                "options": [
                    "1. Lists are mutable, tuples are immutable",
                    "2. Both are mutable",
                    "3. Lists are immutable, tuples are mutable",
                    "4. Tuples are faster, lists are slower"
                ],
                "answer": 1,
                "explanation": "Lists are mutable, meaning you can change their contents, while tuples are immutable and cannot be changed after creation."
            }
        ]
        self.run_quiz(questions, "Data Collections")
    
    def modular_programming(self):
        questions = [
            {
                "question": "What is the output of this code?\ndef func(a, b=2):\n    return a * b\n\nprint(func(b=3, a=4))",
                "options": ["1. 8", "2. 12", "3. Error", "4. 6"],
                "answer": 2,
                "explanation": "The function multiplies a and b. We pass a=4 and b=3 (overriding the default), so 4*3=12."
            },
            {
                "question": "Which keyword is used to return a value from a function?",
                "options": ["1. return", "2. yield", "3. break", "4. pass"],
                "answer": 1,
                "explanation": "The return statement is used to exit a function and return a value."
            },
            {
                "question": "What is the output of: print((lambda x: x**2)(3))",
                "options": ["1. 6", "2. 9", "3. 27", "4. Error"],
                "answer": 2,
                "explanation": "This is a lambda function that squares its input. Called with 3, it returns 9."
            },
            {
                "question": "What is the difference between a lambda function and a regular function in Python?",
                "options": [
                    "1. Lambda functions are anonymous, regular functions are not",
                    "2. Lambda functions are faster, regular functions are slower",
                    "3. Lambda functions can only be used in specific contexts",
                    "4. Both are the same"
                ],
                "answer": 1,
                "explanation": "Lambda functions are anonymous and can be used in place of small functions, while regular functions have a name and can be reused and documented."
            }
        ]
        self.run_quiz(questions, "Modular Programming")
    
    def files_exceptions(self):
        questions = [
            {
                "question": "What is the correct way to ensure a file is properly closed after use?",
                "options": [
                    "1. file = open('test.txt'); file.close()",
                    "2. with open('test.txt') as file: ...",
                    "3. Both 1 and 2",
                    "4. Python automatically closes files"
                ],
                "answer": 3,
                "explanation": "Both methods properly close files, but the 'with' statement (context manager) is preferred as it handles closing automatically even if an error occurs."
            },
            {
                "question": "Which exception is raised when a file isn't found?",
                "options": ["1. FileError", "2. IOError", "3. FileNotFoundError", "4. NotFoundError"],
                "answer": 3,
                "explanation": "FileNotFoundError is raised when trying to open a non-existent file."
            },
            {
                "question": "What is the difference between try/except and try/finally?",
                "options": [
                    "1. try/except handles exceptions, try/finally handles cleanup",
                    "2. Both handle the same thing",
                    "3. try/finally handles exceptions, try/except handles cleanup",
                    "4. try/except and try/finally do the same thing"
                ],
                "answer": 1,
                "explanation": "try/except handles exceptions and executes a specific block of code if an exception occurs, while try/finally handles cleanup code that must run regardless of whether an exception occurred."
            },
            {
                "question": "What is the difference between the 'with' statement and a try/finally block?",
                "options": [
                    "1. 'with' is simpler and more readable",
                    "2. Both do the same thing",
                    "3. try/finally is more powerful and flexible",
                    "4. 'with' is used only for files, try/finally for other resources"
                ],
                "answer": 1,
                "explanation": "'with' is a more concise and readable way to handle context management, especially for resources like files."
            }
        ]
        self.run_quiz(questions, "Files & Exceptions")
    
    def oop(self):
        questions = [
            {
                "question": "What is the output of this code?\nclass MyClass:\n    def __init__(self, val):\n        self.val = val\n    def __add__(self, other):\n        return MyClass(self.val + other.val)\n\na = MyClass(3)\nb = MyClass(4)\nc = a + b\nprint(c.val)",
                "options": ["1. 3", "2. 4", "3. 7", "4. Error"],
                "answer": 3,
                "explanation": "The __add__ method is overloaded to add the val attributes. 3 + 4 = 7."
            },
            {
                "question": "Which method is called when an object is created?",
                "options": ["1. __new__", "2. __init__", "3. __create__", "4. __str__"],
                "answer": 2,
                "explanation": "__init__ is the initializer method that's called when a new object is created."
            },
            {
                "question": "What is the difference between a class and an instance in Python?",
                "options": [
                    "1. A class is an instance, an instance is a class",
                    "2. A class is a blueprint, an instance is an object",
                    "3. They are the same thing",
                    "4. A class inherits from an instance"
                ],
                "answer": 2,
                "explanation": "A class is a blueprint that defines the structure and behavior of objects, while an instance is a specific object created from that class."
            },
            {
                "question": "What is the difference between singleton and factory pattern in Python?",
                "options": [
                    "1. Singleton ensures a class has only one instance, factory creates instances based on type",
                    "2. Both are the same thing",
                    "3. Factory ensures a class has only one instance, singleton creates instances based on type",
                    "4. Singleton creates instances based on type, factory ensures a class has only one instance"
                ],
                "answer": 1,
                "explanation": "Singleton ensures a class has only one instance, while factory creates instances based on type."
            }
        ]
        self.run_quiz(questions, "Object-Oriented Programming")
    
    def practice_test(self):
        questions = [
            {
                "question": "Which operator is used for exponentiation in Python?",
                "options": ["1. ^", "2. **", "3. //", "4. %"],
                "answer": 2,
                "explanation": "The ** operator is used for exponentiation (e.g., 2**3 = 8)."
            },
            {
                "question": "What does range(3, 10, 2) generate?",
                "options": ["1. [3, 5, 7, 9]", "2. [3, 4, 5, 6, 7, 8, 9]", "3. [2, 4, 6, 8]", "4. [3, 10, 2]"],
                "answer": 1,
                "explanation": "range(start, stop, step) generates numbers from start to stop-1, incrementing by step."
            },
            {
                "question": "How do you get a list of all keys in a dictionary d?",
                "options": ["1. d.keys()", "2. list(d)", "3. d.items()", "4. Both 1 and 2"],
                "answer": 4,
                "explanation": "Both d.keys() and list(d) will give you the keys of the dictionary."
            },
            {
                "question": "What is the output of: (lambda x: x**2)(3)",
                "options": ["1. 6", "2. 9", "3. 27", "4. Error"],
                "answer": 2,
                "explanation": "This is a lambda function that squares its input. Called with 3, it returns 9."
            },
            {
                "question": "Which mode opens a file for both reading and writing?",
                "options": ["1. 'r'", "2. 'w'", "3. 'a+'", "4. 'x'"],
                "answer": 3,
                "explanation": "'a+' opens the file for both reading and appending. 'r+' would also be correct but wasn't an option."
            },
            {
                "question": "What is the relationship between a class and an object?",
                "options": [
                    "1. A class is an instance of an object",
                    "2. An object is an instance of a class",
                    "3. They are the same thing",
                    "4. A class inherits from an object"
                ],
                "answer": 2,
                "explanation": "An object is an instance of a class. Classes define the blueprint for objects."
            }
        ]
        self.run_quiz(questions, "Practice Test")

if __name__ == "__main__":
    root = tk.Tk()
    app = CertiportTrainer(root)
    root.mainloop()