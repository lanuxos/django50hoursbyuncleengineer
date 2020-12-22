# generate ascii code

import string
import random

allchar = []
for i in range(65, 91):
    allchar.append(chr(i))
for i in range(97, 123):
    allchar.append(chr(i))
for i in range(10):
    allchar.append(str(i))
print(allchar)

print(list(string.ascii_letters))
print(list(string.ascii_uppercase))
print(list(string.ascii_lowercase))

allChar = [chr(i) for i in range(65, 91)]
allChar.extend([str(i) for i in range(10)])
print(allChar)

AllChar = [chr(i) for i in range(65, 91)]
AllChar.extend([chr(i) for i in range(97, 123)])
AllChar.extend([str(i) for i in range(10)])
print(AllChar)


def GenerateToken(domain='http://localhost:8000/confirm/'):
    allChar = [chr(i) for i in range(65, 91)]
    allChar.extend([chr(i) for i in range(97, 123)])
    allChar.extend([str(i) for i in range(10)])
    emailToken = ''
    for i in range(50):
        emailToken += random.choice(allChar)
    url = domain + emailToken
    return url


GenerateToken()
