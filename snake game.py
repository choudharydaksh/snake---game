import pygame
import random
import sys
from collections import deque

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (15, 23, 42)
GRID_COLOR = (30, 41, 59)
SNAKE_COLOR = (34, 197, 94)
HEAD_COLOR = (22, 163, 74)
FOOD_COLOR = (248, 113, 113)
TEXT_COLOR = (248, 250, 252)
ACCENT_COLOR = (96, 165, 250)


class SnakeGame:
    def __init__(self):
        self.reset()
        self.state = "start"
        self.move_delay = 120
        self.move_timer = 0

    def reset(self):
        self.snake = deque([(GRID_WIDTH // 2, GRID_HEIGHT // 2)])
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.food = self.spawn_food()
        self.move_delay = 120
        self.move_timer = 0

    def spawn_food(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position not in self.snake:
                return position

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if self.state == "start":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.state = "playing"
                return

            if self.state == "game_over":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.reset()
                    self.state = "playing"
                return

            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.next_direction = (1, 0)
            elif event.key == pygame.K_p:
                if self.state == "paused":
                    self.state = "playing"
                else:
                    self.state = "paused"
            elif event.key == pygame.K_ESCAPE:
                self.state = "start"

    def update(self, dt):
        if self.state != "playing":
            return

        self.move_timer += dt
        if self.move_timer < self.move_delay:
            return

        self.move_timer = 0
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.state = "game_over"
            return

        # Self collision
        if new_head in self.snake:
            self.state = "game_over"
            return

        self.snake.appendleft(new_head)

        if new_head == self.food:
            self.score += 1
            self.move_delay = max(55, 120 - self.score * 4)
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

    def draw(self):
        screen.fill(BG_COLOR)
        self.draw_grid()

        # Food
        food_x, food_y = self.food
        rect = pygame.Rect(food_x * CELL_SIZE, food_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, FOOD_COLOR, rect)

        # Snake
        for index, (x, y) in enumerate(self.snake):
            color = HEAD_COLOR if index == 0 else SNAKE_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # HUD
        font = pygame.font.SysFont("arial", 24, bold=True)
        score_text = font.render(f"Score: {self.score}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 20))

        # Overlay
        if self.state == "start":
            self.draw_overlay("Snake Game", "Press Enter or Space to start", "Arrow keys to move • P to pause")
        elif self.state == "paused":
            self.draw_overlay("Paused", "Press P to continue", "Press Esc to return to menu")
        elif self.state == "game_over":
            self.draw_overlay("Game Over", f"Final Score: {self.score}", "Press Enter or Space to play again")

        pygame.display.flip()

    def draw_overlay(self, title, subtitle, hint):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont("arial", 48, bold=True)
        subtitle_font = pygame.font.SysFont("arial", 28)
        hint_font = pygame.font.SysFont("arial", 22)

        title_surf = title_font.render(title, True, TEXT_COLOR)
        subtitle_surf = subtitle_font.render(subtitle, True, ACCENT_COLOR)
        hint_surf = hint_font.render(hint, True, TEXT_COLOR)

        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 2 - 90))
        screen.blit(subtitle_surf, (WIDTH // 2 - subtitle_surf.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(hint_surf, (WIDTH // 2 - hint_surf.get_width() // 2, HEIGHT // 2 + 30))


def main():
    game = SnakeGame()

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            game.handle_event(event)
        game.update(dt)
        game.draw()


if __name__ == "__main__":
    main()
