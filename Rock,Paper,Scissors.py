import random
while True:
    list=("rock","paper","scissors")
    comp=random.choice(list)
    user=None
    print('''Let's begin The Game of Rock, Paper, Scissors \n''')
    while user not in list:
        user=input("Choose between Rock, Paper or Scissors:  ").lower()
        print("-"*50)
    print("Computer: ",comp)
    print("Player: ",user)
    score=0

    if user==comp:
        print('''It's a tie''')
        score+=0
    elif user=="rock":
        if comp=="scissors":
            print("You win")
            score+=1
        elif comp=="paper":
            print("You lose")
            score+=0
    elif user=="paper":
        if comp=="rock":
            print("You win")
            score+=1
        elif comp=="scissors":
            print("You lose")
            score+=0
    elif user=="scissors":
        if comp=="paper":
            print("You win")
            score+=1
        elif comp=="rock":
            print("You lose")
            score+=0
    print(f"Score = {score}")
    print("-"*50)
    repeat=input('''Play Again? (yes/no)  : ''').lower()
    if repeat !="yes":
        break
print("Bye")