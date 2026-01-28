import secrets 
import string 

def generate_code():
	digits = string.digits
	code = "".join(secrets.choice(digits) for i in range(6))
	return code 