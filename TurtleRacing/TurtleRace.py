import turtle
import time
import random

WIDTH, HEIGHT = 800, 800
COLORS = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "black", "cyan"] 




def number_of_racers():
    racers = 0
    while True:
        racers = input("Enter the number of racers (2 - 10): ")
        if racers.isdigit():
            racers = int(racers)
        else:
            print("Input is not numeric.... Please enter a number")
            continue

        if 2<= racers <= 10:
            return racers
        else:
            print("Oops.. Number not in range 2 - 10. ")

def create_turtles(colors):
    turtles =[]
    
    for i, color in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(color)
        racer.shape("turtle")
        racer.left(90) 
        racer.penup()
        racer.pos(0,10)
        racer.pendown()
        turtles.append(racer)
       
def race(colors):
    turtles = create_turtles(colors)

    while True:
        for racers in turtles:
            distance = random.randrange(1, 20)  #between 1 to 20 pixels randomly generate a number
            racers.forward(distance)
            
            x, y = racers.pos()
            if y >= HEIGHT // 2 - 10:
                return colors[turtles.index(racers)]



def create_turtles(colors):
    turtles = []
    spacingx = WIDTH // (len(colors) + 1)
    for i, color in enumerate(colors):
        racers = turtle.Turtle()
        racers.color(color)
        racers.shape("turtle")
        racers.left(90)
        racers.penup()
        racers.setpos(-WIDTH//2 + (i + 1) * spacingx, -HEIGHT//2 + 20)
        racers.pendown()
        turtles.append(racers)
    
    return turtles


def init_turtle():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Turtle Race")
  


racers = number_of_racers()
init_turtle()

random.shuffle(COLORS)
colors = COLORS[:racers]

winner = race(colors)
print (winner)

