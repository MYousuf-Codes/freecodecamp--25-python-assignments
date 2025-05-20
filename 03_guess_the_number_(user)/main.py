import random

def computer_guess(x : int):
    low =1
    high = x
    feedback = ''
    while feedback != 'c': 
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low # this could also be high bcz low = high
        feedback = input(f"Is {guess} too high (H), too Low (L), or correct (c)??").lower()
        if feedback =='h':
            high = guess -1
        elif feedback == 'l':
            low = guess + 1
    print(f"Yahoo, the computer guessed your number {guess}, correctly!!")

computer_guess(1000)