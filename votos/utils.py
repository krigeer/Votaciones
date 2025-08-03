import re
import string ,hashlib, random, openpyxl

def validar_contrasena(password):
    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'[0-9]', password):
        return False
    
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #     return False

    return True

def generar_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

