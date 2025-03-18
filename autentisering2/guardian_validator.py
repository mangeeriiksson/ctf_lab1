from sacred_code_generator import generate_sacred_code

def validate_offering(sacred_password, user_code):
    expected_code = generate_sacred_code()
    if sacred_password == "ECHO" and user_code == expected_code:
        return True
    return False
