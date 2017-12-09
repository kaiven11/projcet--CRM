#coding=utf-8

import random
import string
def random_str():
    return ''.join(random.sample(string.digits+string.ascii_lowercase,6))