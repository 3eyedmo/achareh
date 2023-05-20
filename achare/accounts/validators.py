from rest_framework import serializers
import string

def valid_password(password1, password2):
    if password1 != password2:
        raise serializers.ValidationError("passwords are not same")

    if not 8<=len(password2)<=25:
        raise serializers.ValidationError("passwords must be between 8 and 25 charecters")
    
    if password2 == password2.lower():
        raise serializers.ValidationError("passwords must contain atleast one uppercase charecter")

    if password2 == password2.upper():
        raise serializers.ValidationError("passwords must contain atleast one lowercase charecter")

    digits = string.digits
    if not any(char in digits for char in password2):
        raise serializers.ValidationError("passwords must contain atleast one digit.")