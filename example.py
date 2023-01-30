# from tkinter import PhotoImage
# import turtle

# screen = turtle.Screen()

# # click the image icon in the top right of the code window to see
# # which images are available in this trinket
# image = "among_us.gif"

# # larger = PhotoImage(file="among_us.gif").subsample(2, 2)

# # screen.addshape("larger", turtle.Shape("image", larger))
# # add the shape first then set the turtle shape
# screen.addshape(image)
# print(turtle.shapesize())
# turtle.resizemode("user")
# turtle.shapesize(stretch_len=0.01, stretch_wid=0.01)
# print(turtle.shapesize())
# turtle.shape(image)

# # tortoise = turtle.Turtle("larger")
# # tortoise.hideturtle()
# screen.bgcolor("lightblue")

# move_speed = 10
# turn_speed = 10

# # these defs control the movement of our "turtle"
# def forward():
#   turtle.forward(move_speed)

# def backward():
#   turtle.backward(move_speed)

# def left():
#   turtle.left(turn_speed)

# def right():
#   turtle.right(turn_speed)

# turtle.penup()
# turtle.speed(0)
# turtle.home()

# # now associate the defs from above with certain keyboard events
# screen.onkey(forward, "Up")
# screen.onkey(backward, "Down")
# screen.onkey(left, "Left")
# screen.onkey(right, "Right")
# screen.listen()
# screen.exitonclick()


from turtle import Turtle, Screen

# https://cdn-img.easyicon.net/png/10757/1075705.gif

SQUIRREL_IMAGE = 'among_us.gif'

screen = Screen()

screen.register_shape(SQUIRREL_IMAGE )

turtle = Turtle(shape=SQUIRREL_IMAGE )
turtle.penup()

turtle.pensize(0.3)
turtle.goto(100, 100)
turtle.stamp()
turtle.goto(-100, -100)
turtle.stamp()

turtle.hideturtle()

screen.exitonclick()