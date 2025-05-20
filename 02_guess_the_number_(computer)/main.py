import random

def guess(x : int):
    random_number = random.randint(1,x)
    guess = 0
    while guess != random_number:
        guess = int(input(f'Guess a Number between 1 and {x} : '))
        if guess < random_number:
            print('Sorry, guess agin, Too low.')
        elif guess > random_number:
            print("Sorry, guess again, Too high.")

    print(f" Yahoo, congrats, You guess the number {random_number} correctly!!")

guess(10)
