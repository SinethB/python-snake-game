import tkinter as tk
from random import randint

GAME_WIDTH = 900
GAME_HEIGHT = 600
SPACE_SIZE = 50
BODY_PARTS = 3

# Colors 
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
BUTTON_COLOR = "#333333"  
BUTTON_TEXT_COLOR = "white"  
SCORE_COLOR = "Blue"  

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = [(0, 0) for _ in range(BODY_PARTS)]
        self.squares = [canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake") for x, y in self.coordinates]

class Food:
    def __init__(self, canvas):
        x = randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags='food')

class Game:
    def __init__(self, window):
        self.window = window
        self.direction = "down"
        self.score = 0
        self.game_started = False

        # Score label
        self.label = tk.Label(window, text=f"Score:{self.score}", font=("consolas", 40), fg=SCORE_COLOR)
        self.label.pack()

        # Canvas with set width and height
        self.canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        # Button frame for horizontal placement
        button_frame = tk.Frame(window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)  # Fill horizontally

        # Difficulty selection dropdown (adjusted positioning)
        difficulty_options = ("EASY", "MEDIUM", "HARD")
        self.difficulty_var = tk.StringVar(window)
        self.difficulty_var.set(difficulty_options[0])  # Default to EASY

        difficulty_menu = tk.OptionMenu(window, self.difficulty_var, *difficulty_options)
        difficulty_menu.pack(side=tk.TOP)  # Pack on top for correct placement

        # Buttons with same size using grid
        self.start_button = tk.Button(button_frame, text="Start Game", command=self.start_game, font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.restart_button = tk.Button(button_frame, text="Restart", command=self.restart_game, font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        self.restart_button.grid(row=0, column=1, padx=10, pady=10)

        self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_game, font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        self.exit_button.grid(row=0, column=2, padx=10, pady=10)

        self.window.bind('<Left>', lambda event: self.change_direction("left"))
        self.window.bind('<Right>', lambda event: self.change_direction("right"))
        self.window.bind('<Up>', lambda event: self.change_direction("up"))
        self.window.bind('<Down>', lambda event: self.change_direction("down"))

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

    def start_game(self):
        self.game_started = True
        
        if self.difficulty_var.get() == "EASY":
            speed = 200
        elif self.difficulty_var.get() == "MEDIUM":
            speed = 100
        else:
            speed = 75
        self.next_turn(speed)

    def next_turn(self, speed=200):
        self.speed = speed 

        if self.difficulty_var.get() == "EASY":
            speed = 200
        elif self.difficulty_var.get() == "MEDIUM":
            speed = 100
        else:
            speed = 75

        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.snake.coordinates.insert(0, (x, y))
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score:{self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(speed, self.next_turn)
        

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collisions(self):
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, font=('consolas', 70),
                                text="GAME OVER", fill="red", tags="gameover")

    def restart_game(self):
        self.canvas.delete(tk.ALL)
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.score = 0
        self.direction = 'down'
        self.label.config(text=f"Score:{self.score}")
        self.next_turn()

    def exit_game(self):
        self.window.destroy()
    


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Snake Game")
    window.resizable(False, False)

    game = Game(window)

    window.mainloop()
