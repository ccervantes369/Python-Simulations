import turtle
import random
import time
import pygame

pygame.init()
collision_sound = pygame.mixer.Sound("collision.mp3")

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Bouncing Ball")
wn.setup(width=700, height=700)
wn.tracer(0)

border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.goto(-300, 300)
border.pendown()
border.pensize(3)
for _ in range(4):
    border.forward(600)
    border.right(90)
border.hideturtle()

num_balls = 5
balls = [turtle.Turtle() for _ in range(num_balls)]
colors = ["red", "white", "cyan", "#90EE90", "#b9346d"]

for i, ball in enumerate(balls):
    ball.shape("circle")
    ball.color(colors[i % len(colors)])
    ball.penup()
    ball.speed(0)
    ball.goto(random.randint(-30, 290), random.randint(200, 400))
    ball.vy = 0
    ball.vx = random.randint(-5, 5)
    ball.da = random.randint(-5, 5)

gravity = 0.4

velocity_display = turtle.Turtle()
velocity_display.speed(0)
velocity_display.penup()
velocity_display.hideturtle()
velocity_display.goto(-290, 250)

vector_turtles = [turtle.Turtle() for _ in range(num_balls)]
for vector in vector_turtles:
    vector.color("yellow")
    vector.penup()
    vector.hideturtle()

def draw_arrow(turtle_obj, length, angle):
    turtle_obj.setheading(angle)
    turtle_obj.pendown()
    turtle_obj.forward(length)
    turtle_obj.right(150)
    turtle_obj.forward(10)
    turtle_obj.right(120)
    turtle_obj.forward(10)
    turtle_obj.right(150)
    turtle_obj.penup()
    turtle_obj.forward(length - 10)
    turtle_obj.setheading(angle)

while True:
    wn.update()
    velocity_display.clear()

    for i, ball in enumerate(balls):
        ball.rt(ball.da)
        ball.vy -= gravity
        ball.sety(ball.ycor() + ball.vy)
        ball.setx(ball.xcor() + ball.vx)

        if ball.xcor() > 290 or ball.xcor() < -290:
            ball.vx *= -1
            ball.da *= -1
            collision_sound.play()

        if ball.ycor() > 290:
            ball.sety(290)
            ball.vy *= -1
            ball.da *= -1
            collision_sound.play()

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.vy *= -1
            ball.da *= -1
            collision_sound.play()

        for j in range(i + 1, len(balls)):
            if balls[i].distance(balls[j]) < 25:
                balls[i].vx, balls[j].vx = balls[j].vx, balls[i].vx
                balls[i].vy, balls[j].vy = balls[j].vy, balls[i].vy
                collision_sound.play()

        velocity_display.goto(-290, 250 - (i * 20))
        velocity_display.color(colors[i % len(colors)])
        velocity_display.write(f"Ball {i+1}: vx={ball.vx:.2f}, vy={ball.vy:.2f}", align="left", font=("Courier", 12, "normal"))

        vector_turtles[i].clear()
        vector_turtles[i].goto(ball.xcor(), ball.ycor())
        length = (ball.vx ** 2 + ball.vy ** 2) ** 0.5 * 6
        angle = vector_turtles[i].towards(ball.xcor() + ball.vx, ball.ycor() + ball.vy)
        draw_arrow(vector_turtles[i], length, angle)

    time.sleep(0.01)
