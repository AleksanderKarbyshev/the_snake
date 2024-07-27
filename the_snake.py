from random import randint
from typing import Optional, Tuple, List

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

    def __init__(self, position: Optional[Tuple[int, int]] = CENTER_SCREEN,
                 body_color: Optional[Tuple[int, int]] = None) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Абстрактный метод"""
        pass

    def draw_cell(self, body: pygame.Surface,
                  position: Tuple[int, int]) -> None:
        """Отрисовываем ячейки на экране и далее будем пользоваться
        в дочерних классах для отрисовки объектов
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(body, self.body_color, rect)


class Snake(GameObject):
    """Описываем змейку"""

    def __init__(self) -> None:
        """Описываем начальное положение змейки"""
        super().__init__(CENTER_SCREEN, SNAKE_COLOR)
        self.reset()
        self.positions: List[Tuple[int, int]] = [self.position]
        self.last = None

    def update_direction(self, new_direction: Tuple[int, int]) -> None:
        """Обновляем направление змейки"""
        if new_direction:
            self.direction = new_direction
            new_direction = None

    def move(self) -> None:
        """Прописываем движения змейки"""
        old_x_coordinates, old_y_coordinates = self.positions[0]
        x_coordinates, y_coordinates = self.direction
        self.new_head = ((old_x_coordinates + (x_coordinates * GRID_SIZE))
                         % SCREEN_WIDTH,
                         (old_y_coordinates + (y_coordinates * GRID_SIZE))
                         % SCREEN_HEIGHT)
        self.positions.insert(0, self.new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
            self.last = self.positions[-1]

    def draw(self) -> None:
        """Отрисовываем змейку"""
        self.draw_cell(screen, self.positions[0])
        self.draw_cell(screen, self.last)

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

    def draw(self) -> None:
        """Прописываем яблоко на игровом поле"""
        self.draw_cell(screen, self.position)

    def randomize_position(self) -> None:
        """Закидываем яблоко в рандомное место на игровом поле"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


def handle_keys(snake: Snake) -> None:
    """Описываем управление змейкой"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """'Заводим' игру: прописываем объекты и основную логику игры"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if len(snake.positions) > 2 and snake.new_head in snake.positions[2:]:
            snake.reset()
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            while apple.randomize_position() in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
