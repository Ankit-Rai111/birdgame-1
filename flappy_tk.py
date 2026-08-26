import tkinter as tk
import random

# --- Constants ---
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.4
JUMP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPACING = 220  # horizontal distance between pipe pairs

BIRD_X = 80
BIRD_SIZE = 20

class FlappyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird - Press any key to jump")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.bird_y = HEIGHT // 2
        self.bird_vel = 0

        self.pipes = []  # list of [x, top_height]
        self.score = 0
        self.game_over = False

        # Create first pipe
        first_pipe_x = WIDTH + 50
        top_h = random.randint(80, HEIGHT - PIPE_GAP - 80)
        self.pipes.append([first_pipe_x, top_h])

        # Bind any key press
        self.root.bind("<Key>", self.on_key)

        self.update()

    def on_key(self, event):
        if self.game_over:
            # Restart
            self.bird_y = HEIGHT // 2
            self.bird_vel = 0
            self.pipes = []
            self.score = 0
            self.game_over = False
            first_pipe_x = WIDTH + 50
            top_h = random.randint(80, HEIGHT - PIPE_GAP - 80)
            self.pipes.append([first_pipe_x, top_h])
        else:
            # Jump
            self.bird_vel = JUMP_STRENGTH

    def update(self):
        if not self.game_over:
            # Physics
            self.bird_vel += GRAVITY
            self.bird_y += self.bird_vel

            # Move pipes
            for p in self.pipes:
                p[0] -= PIPE_SPEED

            # Remove off-screen pipes
            if self.pipes and self.pipes[0][0] + PIPE_WIDTH < 0:
                self.pipes.pop(0)

            # Add new pipe
            if WIDTH - self.pipes[-1][0] >= PIPE_SPACING:
                top_h = random.randint(80, HEIGHT - PIPE_GAP - 80)
                self.pipes.append([WIDTH, top_h])

            # Score
            for x, _ in self.pipes:
                if x + PIPE_WIDTH < BIRD_X and x + PIPE_WIDTH + PIPE_SPEED >= BIRD_X:
                    self.score += 1

            # Collision
            if self.check_collision():
                self.game_over = True

        # Draw
        self.draw()

        # Schedule next frame
        self.root.after(16, self.update)  # ~60 FPS

    def check_collision(self):
        # Top/bottom
        if self.bird_y <= 0 or self.bird_y + BIRD_SIZE >= HEIGHT:
            return True

        bird_left = BIRD_X
        bird_right = BIRD_X + BIRD_SIZE
        bird_top = self.bird_y
        bird_bottom = self.bird_y + BIRD_SIZE

        for x, top_h in self.pipes:
            # Top pipe
            top_left = x
            top_right = x + PIPE_WIDTH
            top_top = 0
            top_bottom = top_h

            # Bottom pipe
            bot_left = x
            bot_right = x + PIPE_WIDTH
            bot_top = top_h + PIPE_GAP
            bot_bottom = HEIGHT

            if self.rects_overlap(bird_left, bird_top, bird_right, bird_bottom,
                                  top_left, top_top, top_right, top_bottom):
                return True
            if self.rects_overlap(bird_left, bird_top, bird_right, bird_bottom,
                                  bot_left, bot_top, bot_right, bot_bottom):
                return True

        return False

    def rects_overlap(self, x1, y1, x2, y2, x3, y3, x4, y4):
        return not (x2 <= x3 or x1 >= x4 or y2 <= y3 or y1 >= y4)

    def draw(self):
        self.canvas.delete("all")

        # Draw pipes
        for x, top_h in self.pipes:
            # Top pipe
            self.canvas.create_rectangle(
                x, 0, x + PIPE_WIDTH, top_h,
                fill="green", outline="black"
            )
            # Bottom pipe
            bottom_y = top_h + PIPE_GAP
            self.canvas.create_rectangle(
                x, bottom_y, x + PIPE_WIDTH, HEIGHT,
                fill="green", outline="black"
            )

        # Draw bird
        self.canvas.create_rectangle(
            BIRD_X, self.bird_y, BIRD_X + BIRD_SIZE, self.bird_y + BIRD_SIZE,
            fill="yellow", outline="black"
        )

        # Score
        self.canvas.create_text(
            10, 10, anchor="nw",
            text=f"Score: {self.score}",
            fill="black", font="Consolas 16"
        )

        if self.game_over:
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                text="Game Over - Press any key to restart",
                fill="black", font="Consolas 18"
            )


def main():
    root = tk.Tk()
    root.resizable(False, False)
    game = FlappyGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()