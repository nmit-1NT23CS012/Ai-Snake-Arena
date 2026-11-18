import math

WIDTH = 800
HEIGHT = 600


# distance between two points
def distance(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


# normalize vector
def normalize(dx,dy):
    length = math.sqrt(dx*dx+dy*dy)
    if length == 0:
        return (0,0)
    return (dx/length,dy/length)


# find closest food
def nearest_food(head,foods):
    return min(foods,key=lambda f:distance(head,(f.x,f.y)))


# avoid walls
def wall_avoid(head):
    x,y = head

    dx,dy = 0,0
    margin = 60

    # left wall
    if x < margin:
        dx += 1

    # right wall
    if x > WIDTH-margin:
        dx -= 1

    # top wall
    if y < margin:
        dy += 1

    # bottom wall
    if y > HEIGHT-margin:
        dy -= 1

    return dx,dy


# AI movement logic
def ai_move(snake,foods,snakes):

    head = snake.head()

    # find nearest food
    target = nearest_food(head,foods)

    # food direction
    fx = target.x - head[0]
    fy = target.y - head[1]

    # avoid walls
    wx,wy = wall_avoid(head)

    # combine both
    dx = fx + wx*200
    dy = fy + wy*200

    # set direction
    snake.target_direction = normalize(dx,dy)