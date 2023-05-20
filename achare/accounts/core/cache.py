from redis_driver.core import redis_client
from accounts.exceptions import BannedUser

def otp_limit_for_ip(request):
    key_name = "otp:ip:" + request.META.get("REMOTE_ADDR")
    number = redis_client.incr(key_name)
    if number==1:
        redis_client.expire(name=key_name, time=60 * 5)


def ban_ip_for_otp(request):
    ip = request.META.get("REMOTE_ADDR")
    key_name = "otp:ip:" + ip
    number = redis_client.get(name=key_name)
    if number:
        if int(number) >= 3:
            redis_client.set("banned:otp:ip:" + ip, 1, ex=60*60)


def is_otp_ip_banned(request):
    ip = request.META.get("REMOTE_ADDR")
    name = "banned:otp:ip:" + ip
    is_banned = redis_client.get(name=name)
    if is_banned:
        raise BannedUser()
    

def delete_otp_ip(request):
    ip = request.META.get("REMOTE_ADDR")
    name = "banned:otp:ip:" + ip
    redis_client.delete(name)


def otp_pn_limiter(phone_number):
    key_name = "otp:phone:limiter:" + str(phone_number)
    number = redis_client.incr(name=key_name)
    if number == 1:
        redis_client.expire(key_name, 60 * 5)
    
    if number >= 3:
        redis_client.set(name="banned:otp:pn:" + str(phone_number), value=1, ex=60*60)


def check_otp_pn_is_banned(phone_number):
    name = "banned:otp:pn:" + str(phone_number)
    number = redis_client.get(name=name)
    if number:
        raise BannedUser()


def delete_banned_pn(phone_number):
    name = "banned:otp:pn:" + str(phone_number)
    redis_client.delete(name)



def limit_phone_number_for_login(phone_number):
    key_name = "login:phone:" + str(phone_number)
    tries = redis_client.incr(key_name)
    if tries == 1:
        redis_client.expire(phone_number, 10)
    if tries >= 3:
        redis_client.set("banned:login:phone:" + str(phone_number), 1, 60)


def limit_ip_for_login(ip):
    key_name = "login:ip:" + ip
    tries = redis_client.incr(key_name)
    if tries == 1:
        redis_client.expire(ip, 10)
    if tries >= 3:
        redis_client.set("banned:login:ip:" + ip, 1, 60)


def check_ip_for_login(ip):
    cached_ip = redis_client.get("banned:login:ip:" + ip)
    if cached_ip:
        raise BannedUser()
    return True


def check_phonenumber_for_login(phonenumber):
    cached_phonenumber = redis_client.get("banned:login:phone:" + phonenumber)
    if cached_phonenumber:
        raise BannedUser()
    return True