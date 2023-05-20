# Achareh Test Project :

## Installation :
### Redis Settings :

you can customize redis host and port by changing:
```bash
REFIS_CONFIG = {
    "HOST": "127.0.0.1",
    "PORT": "6379"
}
```
in app settings.py

### App Installation :
```bash
cd achare
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Description :
### Beggining :
Users enter their Phone Number to login. There are two scenarios:\
1 - phone number belongs to existing user and client is given a message and will be directed to login page.\
2 - phone number doesn't belong to any user and client is given a six digit code.

### Second Steps :
#### first scenario:
user enters phone number and password to login. There are some limitation for ip and phone number.

#### second scenario:
user enters OTP code and phone number and if its correct they are given an OTP Token encrypted with phone number. then user enters other infos like firstname and lastname and email and sends OTP Token in headers as OTP-TOKEN and then user is registered.


## Documentation :
achare_saze.json is postman collection for endpoints.