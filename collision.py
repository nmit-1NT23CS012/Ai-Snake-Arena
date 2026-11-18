import math
from food import Food


# distance between two points
def distance(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


# check snake collision
def check_collision(snake,snakes):

    head = snake.head()

    for other in snakes:

        # ignore itself
        if other == snake:
            continue

        # check body collision
        for segment in other.body[10:]:

            if distance(head,segment) < 6:
                return True

    return False


# convert snake to food
def snake_to_food(snake,foods,width,height):

    MAX_FOOD = 40

    for i,segment in enumerate(snake.body):

        if len(foods) > MAX_FOOD:
            break

        if i % 3 == 0:

            f = Food(width,height)

            f.x = int(segment[0])
            f.y = int(segment[1])

            foods.append(f)