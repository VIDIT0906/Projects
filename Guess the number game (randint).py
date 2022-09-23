import random
inp="y"
tries=0
num=0
while (inp=="y" or inp=="Y"):
    print("Guess the Number Game")
    rannum=random.randint(1,101)
    while num!=rannum:
        num=int(input("Enter the guess between 1 and 100: "))
        tries+=1
        if num>rannum:
            print("Too high. Try again.")
        elif num<rannum:
            print("Too low. Try again.")
        else:
            print("Excellent! You guessed it right.")
            print(f"It took you {tries} tries")
    inp=str(input("Do you want to play again.\n(y/n)->"))
else:
    print("Adios!!")