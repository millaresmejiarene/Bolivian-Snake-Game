import tkinter as tk
import random

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

snake = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)
apple = (5, 5)
running = True

def spawn_apple():
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)

def change_direction(dx, dy):
    global direction
    if (dx, dy) == (-direction[0], -direction[1]):
        return
    direction = (dx, dy)

def on_key(event):
    key = event.keysym
    if key == "Up":
        change_direction(0, -1)
    elif key == "Down":
        change_direction(0, 1)
    elif key == "Left":
        change_direction(-1, 0)
    elif key == "Right":
        change_direction(1, 0)

def draw():
    canvas.delete("all")

    # Pomme
    ax, ay = apple
    canvas.create_rectangle(
        ax * CELL_SIZE,
        ay * CELL_SIZE,
        (ax + 1) * CELL_SIZE,
        (ay + 1) * CELL_SIZE,
        fill="red",
    )

    for i, (x, y) in enumerate(snake):
        color = "green" if i == 0 else "lightgreen"
        canvas.create_rectangle(
            x * CELL_SIZE,
            y * CELL_SIZE,
            (x + 1) * CELL_SIZE,
            (y + 1) * CELL_SIZE,
            fill=color,
        )

def game_loop():
    global snake, apple, running

    if not running:
        return

    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
        running = False
        canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 24, "bold"),
        )
        return

    # Collision
    if new_head in snake:
        running = False
        canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 24, "bold"),
        )
        return

    # Avancer
    snake.insert(0, new_head)

    # Pomme ?
    if new_head == apple:
        apple = spawn_apple()
    else:
        snake.pop()

    draw()
    # Rappeler game_loop dans 200 ms
    root.after(200, game_loop)

root = tk.Tk()
root.title("Snake (Tkinter, sans Pygame)")

canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
canvas.pack()

apple = spawn_apple()
draw()

root.bind("<Key>", on_key)

root.after(200, game_loop)
root.mainloop()
