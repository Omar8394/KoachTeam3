# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import hashlib

from datetime import datetime
from datetime import timedelta
import random


def getVerificationLink(user_email):
    x = random.randint(0, 999)
    user_email += str(x)
    h = hashlib.sha1(user_email.encode())
    salt = h.hexdigest()
    print("salt", salt)
    activation_key = hashlib.sha1(str(salt + user_email).encode()).hexdigest()
    key_expires = datetime.today() + timedelta(2)
    print("activation_key:", activation_key)
    print("key expiration:", key_expires)


print("tadifred link")
getVerificationLink("tadifred@gmail.com")
print("kass link")
getVerificationLink("kassandra.arellano17@gmail.com")



