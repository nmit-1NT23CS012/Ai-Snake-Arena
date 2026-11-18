import pygame
import random

# import modules
from snake import Snake
from food import Food
import settings
import ai
import collision

pygame.init()

# create window
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()

# font for leaderboard
font = pygame.font.SysFont("Arial", 18)
small_font = pygame.font.SysFont("Arial", 14)
large_font = pygame.font.SysFont("Arial", 32)

# Game states
GAME_START = 0
GAME_PLAYING = 1
GAME_PAUSED = 2
GAME_OVER = 3

game_state = GAME_START
use_mouse_control = False

# create player
player = Snake(400, 300, settings.PLAYER_COLOR)

# create AI snakes with names
ai_snakes = [
    Snake(random.randint(100, 700),
          random.randint(100, 500),
          settings.AI_COLOR,
          name=f"A{i+1}")
    for i in range(settings.MAX_AI)
]

# create food
foods = [
    Food(settings.WIDTH, settings.HEIGHT)
    for _ in range(settings.FOOD_COUNT)
]

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen, font):
        color = tuple(min(c + 50, 255) for c in self.color) if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)


# Create buttons
start_button = Button(300, 250, 200, 50, "START GAME", (0, 200, 0), (255, 255, 255))
mouse_button = Button(300, 320, 200, 50, "Mouse Control", (100, 100, 255), (255, 255, 255))
pause_button = Button(settings.WIDTH - 120, 10, 110, 40, "PAUSE", (200, 100, 0), (255, 255, 255))

running = True

def draw_start_menu():
    screen.fill(settings.BACKGROUND)
    title = large_font.render("AI SNAKE ARENA", True, (0, 255, 0))
    screen.blit(title, (settings.WIDTH // 2 - title.get_width() // 2, 100))
    
    control_text = small_font.render("Choose Control Method:", True, (200, 200, 200))
    screen.blit(control_text, (settings.WIDTH // 2 - control_text.get_width() // 2, 200))
    
    start_button.draw(screen, small_font)
    mouse_button.draw(screen, small_font)
    
    pygame.display.update()

def draw_game_over():
    screen.fill(settings.BACKGROUND)
    game_over_text = large_font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(game_over_text, (settings.WIDTH // 2 - game_over_text.get_width() // 2, 150))
    
    score_text = font.render(f"Final Score: {player.score}", True, (255, 255, 0))
    screen.blit(score_text, (settings.WIDTH // 2 - score_text.get_width() // 2, 250))
    
    restart_text = small_font.render("Press SPACE to restart or ESC to exit", True, (200, 200, 200))
    screen.blit(restart_text, (settings.WIDTH // 2 - restart_text.get_width() // 2, 350))
    
    pygame.display.update()

def reset_game():
    global player, ai_snakes, foods, game_state
    player = Snake(400, 300, settings.PLAYER_COLOR)
    ai_snakes = [
        Snake(random.randint(100, 700),
              random.randint(100, 500),
              settings.AI_COLOR,
              name=f"A{i+1}")
        for i in range(settings.MAX_AI)
    ]
    foods = [
        Food(settings.WIDTH, settings.HEIGHT)
        for _ in range(settings.FOOD_COUNT)
    ]
    game_state = GAME_START

# ================= GAME LOOP =================
while running:

    clock.tick(settings.FPS)

    # -------- WINDOW CLOSE --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and game_state == GAME_OVER:
                reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GAME_START:
                if start_button.is_clicked(event.pos):
                    use_mouse_control = False
                    game_state = GAME_PLAYING
                if mouse_button.is_clicked(event.pos):
                    use_mouse_control = True
                    game_state = GAME_PLAYING
            elif game_state == GAME_PLAYING:
                if pause_button.is_clicked(event.pos):
                    game_state = GAME_PAUSED
            elif game_state == GAME_PAUSED:
                if pause_button.is_clicked(event.pos):
                    game_state = GAME_PLAYING

    # Handle start menu
    if game_state == GAME_START:
        mouse_pos = pygame.mouse.get_pos()
        start_button.update_hover(mouse_pos)
        mouse_button.update_hover(mouse_pos)
        draw_start_menu()
        continue

    # Handle game over
    if game_state == GAME_OVER:
        draw_game_over()
        continue

    # -------- PLAYER CONTROLS --------
    if game_state == GAME_PLAYING:
        if use_mouse_control:
            # Mouse hover control
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_x, player_y = player.head()
            
            dx = mouse_x - player_x
            dy = mouse_y - player_y
            
            if abs(dx) > 5 or abs(dy) > 5:
                dx, dy = player.normalize(dx, dy)
                player.target_direction = (dx, dy)
        else:
            # Arrow key control
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                player.target_direction = (0, -1)

            if keys[pygame.K_DOWN]:
                player.target_direction = (0, 1)

            if keys[pygame.K_LEFT]:
                player.target_direction = (-1, 0)

            if keys[pygame.K_RIGHT]:
                player.target_direction = (1, 0)

        # -------- SPRINT --------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            player.speed = player.boost_speed
            player.boosting = True
        else:
            player.speed = player.base_speed
            player.boosting = False

        # move player
        player.move()

        # -------- AI MOVEMENT --------
        for snake in ai_snakes:
            ai.ai_move(snake, foods, [player] + ai_snakes)
            snake.move()

        # -------- BOUNDARY CHECK --------
        player_x, player_y = player.head()
        if player_x < 0 or player_x > settings.WIDTH or player_y < 0 or player_y > settings.HEIGHT:
            game_state = GAME_OVER

        # Check AI boundary
        for snake in ai_snakes[:]:
            snake_x, snake_y = snake.head()
            if snake_x < 0 or snake_x > settings.WIDTH or snake_y < 0 or snake_y > settings.HEIGHT:
                ai_snakes.remove(snake)
                continue

        # -------- COLLISION --------
        all_snakes = [player] + ai_snakes
        dead = []

        # check AI death
        for snake in ai_snakes:
            if collision.check_collision(snake, all_snakes):
                dead.append(snake)

        # player death
        if collision.check_collision(player, ai_snakes):
            game_state = GAME_OVER

        # -------- DEAD SNAKE → FOOD --------
        for d in dead:
            collision.snake_to_food(
                d,
                foods,
                settings.WIDTH,
                settings.HEIGHT
            )
            ai_snakes.remove(d)

        # -------- RESPAWN AI --------
        while len(ai_snakes) < settings.MAX_AI:
            ai_snakes.append(
                Snake(
                    random.randint(100, 700),
                    random.randint(100, 500),
                    settings.AI_COLOR,
                    name=f"A{len(ai_snakes)+1}"
                )
            )

        # -------- PLAYER EATS FOOD --------
        for food in foods[:]:
            hx, hy = player.head()

            if abs(hx - food.x) < 10 and abs(hy - food.y) < 10:
                player.grow()
                foods.remove(food)

                # limit food
                if len(foods) < 25:
                    foods.append(
                        Food(settings.WIDTH, settings.HEIGHT)
                    )

        # -------- AI EATS FOOD --------
        for snake in ai_snakes:
            for food in foods[:]:
                hx, hy = snake.head()

                if abs(hx - food.x) < 10 and abs(hy - food.y) < 10:
                    snake.grow()
                    foods.remove(food)

                    if len(foods) < 25:
                        foods.append(
                            Food(settings.WIDTH,
                                 settings.HEIGHT)
                        )
                    break

    # -------- DRAW --------
    screen.fill(settings.BACKGROUND)

    # Draw boundary
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, settings.WIDTH, settings.HEIGHT), 2)

    # draw food
    for food in foods:
        pygame.draw.circle(
            screen,
            settings.FOOD_COLOR,
            (int(food.x), int(food.y)),
            3
        )

    # draw snakes
    player.draw(screen)

    for snake in ai_snakes:
        snake.draw(screen)

    # -------- LEADERBOARD --------
    all_snakes = [player] + ai_snakes

    sorted_snakes = sorted(
        all_snakes,
        key=lambda s: s.score,
        reverse=True
    )

    y = 10

    screen.blit(
        font.render("Leaderboard", True, (255, 255, 255)),
        (10, y)
    )

    y += 20

    for i, s in enumerate(sorted_snakes[:5]):

        name = "Player" if s == player else (s.name if s.name else f"AI {i}")

        screen.blit(
            font.render(
                f"{name}: {s.score}",
                True,
                (200, 200, 200)
            ),
            (10, y)
        )

        y += 18

    # Draw game state info
    if game_state == GAME_PLAYING:
        control_text = f"Control: {'Mouse Hover' if use_mouse_control else 'Arrow Keys'}"
        screen.blit(small_font.render(control_text, True, (100, 255, 100)), (10, settings.HEIGHT - 25))
        
        mouse_pos = pygame.mouse.get_pos()
        pause_button.update_hover(mouse_pos)
        pause_button.draw(screen, small_font)
    elif game_state == GAME_PAUSED:
        pause_text = large_font.render("PAUSED", True, (255, 255, 0))
        screen.blit(pause_text, (settings.WIDTH // 2 - pause_text.get_width() // 2, settings.HEIGHT // 2 - 50))
        
        resume_text = small_font.render("Click PAUSE button to resume", True, (200, 200, 200))
        screen.blit(resume_text, (settings.WIDTH // 2 - resume_text.get_width() // 2, settings.HEIGHT // 2 + 20))
        
        mouse_pos = pygame.mouse.get_pos()
        pause_button.update_hover(mouse_pos)
        pause_button.draw(screen, small_font)

    pygame.display.update()

pygame.quit()