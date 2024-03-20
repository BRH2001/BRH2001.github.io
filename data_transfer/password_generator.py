from random import randint
import random
import string


class Passwordgen:

    def __init__(self):

        self.lowercase_letters = string.ascii_lowercase
        self.uppercase_letters = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = string.punctuation

        self.length = 32  # Fixed length of 32 characters
        self.num_passwords = 50

    def run_gen(self):
        with open("passwords.txt", "w") as file:
            for _ in range(self.num_passwords):
                self._generate_password()
                file.write(self.password + "\n")

        print(f"{self.num_passwords} secure passwords generated and saved to 'passwords.txt'.\n")
        self._pick_three_passwords()

    def _generate_password(self):
        # Ensure the length is at least 32 characters
        if self.length < 32:
            return "Password length should be at least 32 characters."

        # Make a password with randomly generated characters
        self.password = ''
        for _ in range(self.length):
            lowercase_letter = random.choice(self.lowercase_letters)
            uppercase_letter = random.choice(self.uppercase_letters)
            digit = random.choice(self.digits)
            symbol = random.choice(self.symbols)

            all_characters = [lowercase_letter, uppercase_letter, digit, symbol]
            x = random.choices(all_characters, k=1)
            self.password += x[0]

        self._check_all_characters()

    def _check_all_characters(self):
        """Check if every type of character is used in the generated password"""
        self.lowercase = False
        self.uppercase = False
        self.digit = False
        self.symbol = False

        # Check each individual character to see if it is present in the password string
        for y in self.password:
            if y in self.lowercase_letters and not self.lowercase:
                self.lowercase = True
            if y in self.uppercase_letters and not self.uppercase:
                self.uppercase = True
            if y in self.digits and not self.digit:
                self.digit = True
            if y in self.symbols and not self.symbol:
                self.symbol = True
            if self.lowercase and self.uppercase and self.digit and self.symbol:
                break

        # If one of the character types isn't present, remove the last character and replace it with the missing one
        if not self.lowercase:
            self.password.pop()
            self.password += random.choice(self.lowercase_letters)
        if not self.uppercase:
            self.password.pop()
            self.password += random.choice(self.uppercase_letters)
        if not self.digit:
            self.password.pop()
            self.password += random.choice(self.digits)
        if not self.symbol:
            self.password.pop()
            self.password += random.choice(self.symbols)

    @staticmethod
    def _pick_three_passwords():
        # Makes a list with 3 random numbers between 1 and 50
        random_list = []
        while len(random_list) != 3:
            x = randint(1, 50)
            random_list.append(x)
            # Making sure the program doesn't accidentally have a duplicate number
            random_list = list(dict.fromkeys(random_list))

        # Read the lines in the file, make it into a list and then use the random numbers to only print out 3 of them
        with open("passwords.txt", "r") as file:
            lines = file.readlines()
        with open("passwords.txt", "w") as file:
            for number, line in enumerate(lines):
                if number in random_list:
                    file.write(line)
            file.close()

        print("Randomly chose 3 of the 50 generated passwords to use for the text files")


if __name__ == "__main__":
    pg = Passwordgen()
    pg.run_gen()

