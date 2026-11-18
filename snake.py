import pygame
import math


class Snake:
    def __init__(self, x, y, color, name=None):

        # snake body (head at index 0)
        self.body = [(x, y)]

        # snake length
        self.length = 25

        # snake color
        self.color = color

        # snake name
        self.name = name

        # movement direction
        self.direction = (1, 0)

        # smooth turning direction
        self.target_direction = (1, 0)

        # normal speed
        self.base_speed = 2.0

        # sprint speed
        self.boost_speed = 3.8

        # current speed
        self.speed = self.base_speed

        # smooth turning factor
        self.turn_speed = 0.2

        # sprint flag
        self.boosting = False

        # score for leaderboard
        self.score = 0


    # normalize vector (keep direction length = 1)
    def normalize(self, dx, dy):
        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            return (0, 0)

        return (dx / length, dy / length)


    # move snake
    def move(self):

        dx, dy = self.direction
        tdx, tdy = self.target_direction

        # smooth turning
        dx += (tdx - dx) * self.turn_speed
        dy += (tdy - dy) * self.turn_speed

        dx, dy = self.normalize(dx, dy)
        self.direction = (dx, dy)

        head_x, head_y = self.body[0]

        # new head position
        new_head = (
            head_x + dx * self.speed,
            head_y + dy * self.speed
        )

        # insert new head
        self.body.insert(0, new_head)

        # shrink when sprinting
        if self.boosting and self.length > 15:
            self.length -= 0.25

        # trim tail
        while len(self.body) > int(self.length):
            self.body.pop()


    # grow snake
    def grow(self):
        self.length += 4
        self.score += 10


    # draw snake
    def draw(self, screen):

        for i, segment in enumerate(self.body):

            # smaller tail
            radius = max(4, 8 - i // 10)

            pygame.draw.circle(
                screen,
                self.color,
                (int(segment[0]), int(segment[1])),
                radius
            )

        # draw eye
        hx, hy = self.body[0]

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(hx), int(hy)),
            3
        )

        # draw name if exists
        if self.name:
            font = pygame.font.SysFont("Arial", 12)
            text = font.render(self.name, True, (255, 255, 255))
            screen.blit(text, (int(hx) - 10, int(hy) - 20))


    # get head position
    def head(self):
        return self.body[0]