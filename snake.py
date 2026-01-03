import pygame
import random
import os

# Simple Snake game using Pygame
# Controls: Arrow keys to move. Press R to restart or Q/ESC to quit on Game Over.

# --- Configuration ---
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20
INITIAL_SPEED = 10  # base FPS
SPEED_INCREMENT_EVERY = 5  # points
SPEED_INCREMENT = 2

HIGH_SCORE_FILE = 'highscore.txt'


def load_highscore():
    if not os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write('0')
        return 0
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0


def save_highscore(score):
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))
    except Exception:
        pass


def draw_snake(surface, color, snake_list):
    for block in snake_list:
        rect = pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, color, rect)


def show_score(surface, score, highscore, font):
    score_surf = font.render(f"Score: {score}  High Score: {highscore}", True, (255, 255, 255))
    surface.blit(score_surf, (10, 10))


def game_over_screen(surface, score, highscore, font):
    surface.fill((0, 0, 0))
    go_surf = font.render("GAME OVER", True, (255, 0, 0))
    score_surf = font.render(f"Final Score: {score}", True, (255, 255, 255))
    instr_surf = font.render("Press R to Restart or Q/ESC to Quit", True, (200, 200, 200))

    surface.blit(go_surf, (WINDOW_WIDTH // 2 - go_surf.get_width() // 2, WINDOW_HEIGHT // 3))
    surface.blit(score_surf, (WINDOW_WIDTH // 2 - score_surf.get_width() // 2, WINDOW_HEIGHT // 3 + 50))
    surface.blit(instr_surf, (WINDOW_WIDTH // 2 - instr_surf.get_width() // 2, WINDOW_HEIGHT // 3 + 110))
    pygame.display.flip()


def random_food_position(snake_list):
    max_x = (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE
    max_y = (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE
    while True:
        x = random.randint(0, max_x) * BLOCK_SIZE
        y = random.randint(0, max_y) * BLOCK_SIZE
        if [x, y] not in snake_list:
            return x, y


def game_loop():
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        pass

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('consolas', 20)

    # Color themes: (bg, snake, food)
    THEMES = [
        ((0, 0, 0), (0, 255, 0), (255, 0, 0)),
        ((30, 30, 60), (200, 200, 50), (255, 100, 100)),
        ((240, 240, 240), (0, 120, 0), (200, 0, 0)),
    ]
    theme_index = 0
    bg_color, snake_color, food_color = THEMES[theme_index]

    # Sound placeholders (optional files in same folder): eat.wav, gameover.wav, music.mp3
    eat_sound = None
    gameover_sound = None
    music_playing = False
    music_on = True
    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        if os.path.exists('eat.wav'):
            eat_sound = pygame.mixer.Sound('eat.wav')
        if os.path.exists('gameover.wav'):
            gameover_sound = pygame.mixer.Sound('gameover.wav')
        if os.path.exists('music.mp3') and music_on:
            pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.play(-1)
            music_playing = True
    except Exception:
        eat_sound = None
        gameover_sound = None
        music_playing = False

    # Game state
    highscore = load_highscore()

    running = True
    while running:
        # Initialize new game
        snake_list = [[WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]]
        snake_length = 1
        dx = 0
        dy = 0
        score = 0
        speed = INITIAL_SPEED

        food_x, food_y = random_food_position(snake_list)

        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx = -BLOCK_SIZE
                        dy = 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx = BLOCK_SIZE
                        dy = 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dx = 0
                        dy = -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx = 0
                        dy = BLOCK_SIZE
                    elif event.key == pygame.K_t:
                        # cycle themes
                        theme_index = (theme_index + 1) % len(THEMES)
                        bg_color, snake_color, food_color = THEMES[theme_index]
                    elif event.key == pygame.K_m:
                        # toggle music
                        music_on = not music_on
                        if music_on and os.path.exists('music.mp3'):
                            try:
                                pygame.mixer.music.play(-1)
                                music_playing = True
                            except Exception:
                                music_playing = False
                        else:
                            try:
                                pygame.mixer.music.stop()
                            except Exception:
                                pass

            # If no movement yet, keep waiting for key press
            if dx == 0 and dy == 0:
                screen.fill(bg_color)
                intro_surf = font.render('Use arrow keys to move the snake', True, (180, 180, 180))
                screen.blit(intro_surf, (WINDOW_WIDTH // 2 - intro_surf.get_width() // 2, WINDOW_HEIGHT // 2 - 20))
                show_score(screen, score, highscore, font)
                pygame.display.flip()
                clock.tick(15)
                continue

            # Move snake
            head_x = snake_list[0][0] + dx
            head_y = snake_list[0][1] + dy
            new_head = [head_x, head_y]
            snake_list.insert(0, new_head)

            # Check for food
            if head_x == food_x and head_y == food_y:
                score += 1
                snake_length += 1
                # play eat sound if available
                if eat_sound:
                    try:
                        eat_sound.play()
                    except Exception:
                        pass
                # Increase speed occasionally
                if score % SPEED_INCREMENT_EVERY == 0:
                    speed += SPEED_INCREMENT
                food_x, food_y = random_food_position(snake_list)
            else:
                # keep tail length
                if len(snake_list) > snake_length:
                    snake_list.pop()

            # Check collisions
            # Wall collision
            if head_x < 0 or head_x >= WINDOW_WIDTH or head_y < 0 or head_y >= WINDOW_HEIGHT:
                game_over = True
            # Self collision
            if new_head in snake_list[1:]:
                game_over = True

            # Draw everything
            screen.fill(bg_color)
            pygame.draw.rect(screen, food_color, (food_x, food_y, BLOCK_SIZE, BLOCK_SIZE))
            draw_snake(screen, snake_color, snake_list)
            show_score(screen, score, highscore, font)
            pygame.display.flip()

            clock.tick(speed)

        # End of one playthrough
        if score > highscore:
            highscore = score
            save_highscore(highscore)

        # play game over sound
        if gameover_sound:
            try:
                gameover_sound.play()
            except Exception:
                pass

        # stop music when game ends
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        # Show Game Over and wait for player action
        waiting = True
        while waiting:
            game_over_screen(screen, score, highscore, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False  # will restart outer loop
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return


if __name__ == '__main__':
    game_loop()
