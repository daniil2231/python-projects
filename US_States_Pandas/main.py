from turtle import Turtle, Screen
import pandas

screen = Screen()
screen.title("U.S. States")
screen.addshape("blank_states_img.gif")
t = Turtle()
t.shape("blank_states_img.gif")

data = pandas.read_csv("50_states.csv")

score = 0
guessed_states = []
game_on = True
while game_on:
    answer = screen.textinput("Guess the state", f"{score}/50 guessed")
    check = data[data["state"] == answer]
    if not check.empty and guessed_states.count(answer) == 0:
        tu = Turtle()
        tu.penup()
        tu.hideturtle()
        tu.speed("fastest")
        x = check["x"].values[0]
        y = check["y"].values[0]
        tu.goto(x, y)
        tu.write(answer)
        score += 1
        guessed_states.append(answer)
