from captcha.image import ImageCaptcha
import base64
import random
import time


captchas = {}

def generate_captcha():
    image = ImageCaptcha()
    captcha = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 4))
    captchas[captcha.lower()] = time.time()
    return base64.b64encode(image.generate(captcha).getvalue()).decode()

def validate_captcha(text):
    if text.lower() in captchas:
        if time.time() - captchas[text.lower()] < 60:
            return True
        else:
            captchas.pop(text.lower())
            return False
    else:
        return False

def generate_password():
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 16))
