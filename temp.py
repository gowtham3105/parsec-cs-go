import turtle

# Set up the turtle object
t = turtle.Turtle()

# Define the points you want to connect
points = [(50, 50), (100, 150), (200, 100), (150, 50)]

# Move to the first point and begin drawing the polygon
t.penup()
t.goto(points[0])
t.pendown()
t.fillcolor('gray')
t.begin_fill()

# Draw lines to connect each point in order
for point in points[1:]:
    t.goto(point)

# Return to the starting point to close the polygon
t.goto(points[0])

# End the fill and hide the turtle
t.end_fill()
t.hideturtle()

# Update the screen to show the completed polygon
turtle.done()
