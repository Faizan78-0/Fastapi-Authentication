import time

def send_welcome_email(user_email):
    
    print(f"Sending welcome email to {user_email}...")
    time.sleep(2)  
    print(f"Welcome email sent to {user_email}!")
    

def send_opt_email(email: str, opt: str):
    print(f"Sending OPT {opt} to {email}")