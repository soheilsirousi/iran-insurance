import random
from django.core.cache import cache


def generate_otp(phone):
    code = str(random.randint(1000, 9999))
    cache.set(f"otp_{phone}", code, timeout=120)
    return code


def verify_otp(phone, otp):
    code = cache.get(f"otp_{phone}")
    if otp == code:
        cache.delete(f"otp_{phone}")
        return True

    return False