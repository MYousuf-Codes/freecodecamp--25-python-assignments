import turtle

# creating game window
window = turtle.Screen()
window.title("Pong Game - Intermediate Version")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)  

# scores 
score_a = 0
score_b = 0

#Left Paddle
paddle_a = turtle.Turtle()
paddle_a.speed(0)  # Max speed
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)  # Taller paddle
paddle_a.penup()
paddle_a.goto(-350, 0)

# Right Paddle 
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2  # Move by 0.2 pixels each frame (x direction)
ball.dy = 0.2  # Move by 0.2 pixels each frame (y direction)

# === Score Display ===
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0 | Player B: 0", align="center", font=("Courier", 24, "normal"))

# white lines as padle

def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250:
        paddle_a.sety(y + 20)

def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        paddle_a.sety(y - 20)

def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        paddle_b.sety(y + 20)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        paddle_b.sety(y - 20)

# keyboard keys

window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")

# the Instructions for playe
instruction_pen = turtle.Turtle()
instruction_pen.hideturtle()
instruction_pen.color("white")
instruction_pen.penup()
instruction_pen.goto(0, 50)
instruction_pen.write("Welcome to Pong!\n\nW/S for Player A | Up/Down for Player B\n\nClick to Start",
                      align="center", font=("Courier", 16, "normal"))


# start the game

def start_game(x, y):
    instruction_pen.clear()
    run_game()

def run_game():
    global score_a, score_b
    while True:
        window.update()

        # Moveing the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Top & bottom bounce
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1

        # Left & right border 
        if ball.xcor() > 390:
            score_a += 1
            update_score()
            ball.goto(0, 0)
            ball.dx *= -1

        if ball.xcor() < -390:
            score_b += 1
            update_score()
            ball.goto(0, 0)
            ball.dx *= -1

        # Paddle collision
        if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
            ball.setx(340)
            ball.dx *= -1

        if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
            ball.setx(-340)
            ball.dx *= -1

def update_score():
    pen.clear()
    pen.write(f"Player A: {score_a} | Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

# Wait for click to start game
window.onscreenclick(start_game)

window.mainloop()