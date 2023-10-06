from tkinter import *
import random
from enum import Enum

# Game configuration constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Constants for difficulty
DIFFICULTY = {
    "Easy": 150,
    "Medium": 100,
    "Difficult": 50
}

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class CenteredWindow(Tk):
    def geometry_centered(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = [self.create_square(x, y) for x, y in self.coordinates]

    def create_square(self, x, y):
        return canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def initialize_game():
    global canvas, label
    label = Label(window, text="Score: 0", font=('consolas', 40))
    label.pack()
    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    global score, direction, snake, food
    score = 0
    direction = Direction.DOWN
    snake = Snake()
    food = Food()
    window.after(SPEED, next_turn, snake, food)

def next_turn(snake, food):
    x, y = snake.coordinates[0]
    dx, dy = direction.value
    x += dx * SPACE_SIZE
    y += dy * SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = snake.create_square(x, y)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if direction is not new_direction and not any((direction.value[i] + new_direction.value[i]) == 0 for i in range(2)):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for coord in snake.coordinates[1:]:
        if coord == [x, y]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    restart_button = Button(canvas, text="Play Again", command=restart_game)
    restart_button_window = canvas.create_window(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 100, anchor="center", window=restart_button)

def restart_game():
    canvas.delete(ALL)
    canvas.destroy()
    label.destroy()
    start_menu()

def set_difficulty(difficulty):
    global SPEED
    SPEED = DIFFICULTY[difficulty]
    menu_frame.destroy()
    initialize_game()

def start_menu():
    global menu_frame
    menu_frame = Frame(window, bg=BACKGROUND_COLOR)
    menu_frame.pack(expand=True, fill=BOTH)
    
    Label(menu_frame, text="Select Game Difficulty", bg=BACKGROUND_COLOR, fg="white", font=('consolas', 40)).pack(pady=50)
    
    for difficulty, _ in DIFFICULTY.items():
        Button(menu_frame, text=difficulty, font=('consolas', 30), command=lambda diff=difficulty: set_difficulty(diff)).pack(pady=20)

window = CenteredWindow()
window.title("Snake game")
window.resizable(False, False)
window.geometry_centered(GAME_WIDTH, GAME_HEIGHT + 40)  # Assuming a label height of 40

key_map = {"<Up>": Direction.UP, "<Down>": Direction.DOWN, "<Left>": Direction.LEFT, "<Right>": Direction.RIGHT}
for key, direction in key_map.items():
    window.bind(key, lambda event, dir=direction: change_direction(dir))

# Initialize with the start menu
start_menu()
window.mainloop()
