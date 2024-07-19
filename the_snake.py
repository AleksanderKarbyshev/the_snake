from random import randint
from typing import Optional, Tuple

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс отвечающий за взаимодействия на игровом поле"""

    def __init__(self, position: Optional[Tuple[int, int]] = None,
                 body_color: Optional[Tuple[int, int]] = None) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def update_direction(self, new_direction: Tuple[int, int]) -> None:
        """Обновляем направление змейки"""
        if new_direction != (self.direction[0] * -1, self.direction[1] * -1):
            self.next_direction = new_direction

    def draw(self, body: pygame.Surface) -> None:
        """Абстрактный метод"""
        pass

    def draw_cell(self, body: pygame.Surface, position: Tuple[int, int],
                  color: Optional[Tuple[int, int, int]] = None) -> None:
        """Отрисовываем ячейки на экране и далее будем пользоваться
        в дочерних классах для отрисовки объектов
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(body, self.body_color, rect)


class Snake(GameObject):
    """Описываем змейку"""

    def __init__(self) -> None:
        """Описываем начальное положение змейки"""
        super().__init__((GRID_WIDTH // 2 * GRID_SIZE,
                          GRID_HEIGHT // 2 * GRID_SIZE), SNAKE_COLOR)
        self.reset()
        self.next_direction: Optional[Tuple[int, int]] = None

    def move(self) -> None:
        """Прописываем движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        old_head = self.positions[0]
        x, y = self.direction
        new_head = ((old_head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                    (old_head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        if len(self.positions) > 2 and new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, body: pygame.Surface) -> None:
        """Отрисовываем змейку"""
        for position in self.positions[:-1]:
            self.draw_cell(body, position)

        head_position = self.positions[0]
        self.draw_cell(body, head_position, SNAKE_COLOR)

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращаем позицию головы змейки"""
        return self.positions[0]

    def reset(self) -> None:
        """Откатываем змейку в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


class Apple(GameObject):
    """Работаем с яблоком"""

    def __init__(self) -> None:
        """Прописываем яблоко в игре"""
        super().__init__(None, APPLE_COLOR)
        self.randomize_position()

    def draw(self, body: pygame.Surface) -> None:
        """Прописываем яблоко на игровом поле"""
        self.draw_cell(body, self.position)

    def randomize_position(self) -> None:
        """Закидываем яблоко в рандомное место на игровом поле"""
        self.position = (randint(0, GRID_HEIGHT) * GRID_SIZE,
                         randint(0, GRID_WIDTH) * GRID_SIZE)


def handle_keys(game_object) -> None:
    """Описываем управление змейкой"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """'Заводим' игру: прописываем объекты и основную логику игры"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            while apple.randomize_position() in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
