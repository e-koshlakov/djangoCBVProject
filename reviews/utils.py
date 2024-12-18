import string, random

def slug_generator(size=20, chars=string.ascii_lowercase+ string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

