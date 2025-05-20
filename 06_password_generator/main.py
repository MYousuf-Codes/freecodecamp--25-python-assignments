import random

print("Welcome to the Password Generator!")

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*.,?0123456789'
number = (input("How many passwords do you want to generate? ")) 
number = int(number) # convert to int

length = int(input("How long do you want your passwords to be? ")) 
length = int(length) # convert to int

print('\nHere are your passwords: \n')

for pwd in range(number):
    passwords = ''
    for c in range(length):
        passwords += random.choice(chars)
    print(passwords)
