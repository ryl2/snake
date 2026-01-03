import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Minimal game core and renderer using Pillow (no pygame required).

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20
INITIAL_SPEED = 10
SPEED_INCREMENT_EVERY = 5
SPEED_INCREMENT = 2

class GameCore:
    def __init__(self):
        # create PIL image buffer for rendering
        self.font = ImageFont.load_default()
        self.reset()

    def reset(self):
        self.snake = [[WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]]
        self.snake_length = 1
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.speed = INITIAL_SPEED
        self.game_over = False
        self.food_x, self.food_y = self.random_food_position()

    def random_food_position(self):
        max_x = (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE
        max_y = (WINDOW_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE
        while True:
            x = random.randint(0, max_x) * BLOCK_SIZE
            y = random.randint(0, max_y) * BLOCK_SIZE
            if [x, y] not in self.snake:
                return x, y

    def set_direction(self, direction):
        if direction == 'left' and self.dx == 0:
            self.dx = -BLOCK_SIZE; self.dy = 0
        elif direction == 'right' and self.dx == 0:
            self.dx = BLOCK_SIZE; self.dy = 0
        elif direction == 'up' and self.dy == 0:
            self.dx = 0; self.dy = -BLOCK_SIZE
        elif direction == 'down' and self.dy == 0:
            self.dx = 0; self.dy = BLOCK_SIZE

    def tick(self):
        if self.game_over:
            return
        if self.dx == 0 and self.dy == 0:
            return

        head_x = self.snake[0][0] + self.dx
        head_y = self.snake[0][1] + self.dy
        new_head = [head_x, head_y]
        self.snake.insert(0, new_head)

        if head_x == self.food_x and head_y == self.food_y:
            self.score += 1
            self.snake_length += 1
            if self.score % SPEED_INCREMENT_EVERY == 0:
                self.speed += SPEED_INCREMENT
            self.food_x, self.food_y = self.random_food_position()
        else:
            if len(self.snake) > self.snake_length:
                self.snake.pop()

        # collisions
        if head_x < 0 or head_x >= WINDOW_WIDTH or head_y < 0 or head_y >= WINDOW_HEIGHT:
            self.game_over = True
        if new_head in self.snake[1:]:
            self.game_over = True

    def render_png_bytes(self):
        img = Image.new('RGB', (WINDOW_WIDTH, WINDOW_HEIGHT), (0,0,0))
        draw = ImageDraw.Draw(img)
        # food
        draw.rectangle([self.food_x, self.food_y, self.food_x+BLOCK_SIZE-1, self.food_y+BLOCK_SIZE-1], fill=(255,0,0))
        # snake
        for block in self.snake:
            draw.rectangle([block[0], block[1], block[0]+BLOCK_SIZE-1, block[1]+BLOCK_SIZE-1], fill=(0,255,0))
        # score
        draw.text((10,10), f"Score: {self.score}", font=self.font, fill=(255,255,255))

        buf = BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

    def get_state(self):
        return {'score': self.score, 'game_over': self.game_over}
