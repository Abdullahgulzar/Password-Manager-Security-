
import random
import string

# Function to convert password to ASCII values
def ascii_code(password):
    return sum(ord(char) for char in password)

# Function to generate random seed
def generate_seed(length):
    return random.randint(10 * (length - 1), (10 * length) - 1)

# Encrypt password using XOR operation
def honey_encrypt(master_password):
    password_ascii = ascii_code(master_password)
    seed = generate_seed(len(str(password_ascii)))
    cipher = password_ascii ^ seed
    return seed, cipher

# Decrypt password to verify
def honey_decrypt(seed, cipher):
    return cipher ^ seed

# Fake Password Manager - Honeypot
def redirect_to_honeypot(attempted_password):
    fake_passwords = [
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        for _ in range(5)
    ]
    print("Redirected to Honeypot. Decoy Passwords:", fake_passwords)
    return fake_passwords

# Log attacker details
def log_attack(email, attempted_password):
    print(f"Attack detected for email: {email}")
    print(f"Attempted Password: {attempted_password}")

# Simulated Database (in-memory)
users_db = {}  # Format: {'email': {'name': '', 'id': '', 'semester': '', 'cgpa': '', 'mobile': '', 'seed': seed, 'cipher': cipher, 'failed_attempts': 0, 'locked': False, 'mfa_required': False, 'security_question': '', 'security_answer': ''}}

def register_user():
    email = input("Enter your email: ")
    if email in users_db:
        print("Email already registered. Please login.")
        return

    name = input("Enter your name: ")
    user_id = input("Enter your ID: ")
    semester = input("Enter your semester: ")
    cgpa = input("Enter your CGPA: ")
    mobile = input("Enter your mobile number: ")
    password = input("Enter your password: ")
    seed, cipher = honey_encrypt(password)
    security_question = input("Set your security question (e.g., What is your pet's name?): ")
    security_answer = input("Set your security answer: ").lower()
    users_db[email] = {
        'name': name,
        'id': user_id,
        'semester': semester,
        'cgpa': cgpa,
        'mobile': mobile,
        'seed': seed,
        'cipher': cipher,
        'failed_attempts': 0,
        'locked': False,
        'mfa_required': False,
        'security_question': security_question,
        'security_answer': security_answer
    }
    print(f"User {email} registered successfully.")


def unlock_account(email):
    users_db[email]['locked'] = False
    users_db[email]['failed_attempts'] = 0
    print(f"Account {email} unlocked.")


def forgot_password():
    email = input("Enter your registered email: ")
    user = users_db.get(email)
    
    if user:
        print(f"Security Question: {user['security_question']}")
        answer = input("Answer: ").lower()
        if answer == user['security_answer']:
            new_password = input("Enter your new password: ")
            seed, cipher = honey_encrypt(new_password)
            users_db[email]['seed'] = seed
            users_db[email]['cipher'] = cipher
            print("Password reset successful. You can now log in with your new password.")
        else:
            print("Incorrect answer. Password reset failed.")
    else:
        print("Email not found. Please register first.")


def login_user():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = users_db.get(email)
    if user:
        if user['locked']:
            print("Your account is locked. Please try again later.")
            return "Account locked."

        decrypted_password = honey_decrypt(user['seed'], user['cipher'])
        
        if decrypted_password == ascii_code(password):
            print("Login Successful! Welcome.")
            print(f"\nRegistered User Details:\nName: {user['name']}\nID: {user['id']}\nSemester: {user['semester']}\nCGPA: {user['cgpa']}\nMobile Number: {user['mobile']}")
            user['failed_attempts'] = 0  # Reset failed attempts
            return "Login successful!"
        else:
            user['failed_attempts'] += 1
            log_attack(email, password)
            if user['failed_attempts'] >= 5:
                user['locked'] = True
                print("Account locked. Please try again later.")
                return "Account locked."
            else:
                fake_passwords = redirect_to_honeypot(password)
                return  # Removed "Invalid login. Fake passwords generated."
    else:
        return "User not found. Please register first."

# Main program flow
if __name__ == "__main__":
    while True:
        print("\nPassword Vault System")
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        choice = input("Choose an option (1/2/3/4): ")
        
        if choice == "1":
            register_user()
        elif choice == "2":
            print(login_user())
        elif choice == "3":
            forgot_password()
        elif choice == "4":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

