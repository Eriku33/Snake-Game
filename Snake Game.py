import tkinter
import random


class Constraints:
    """map and item constraints"""
    board_height = 300
    board_width = 300
    delay = 100
    dot_size = 10
    apple_limit_position = 29


class Board(tkinter.Canvas):
    def __init__(self):
        super().__init__(height=Constraints.board_height, width=Constraints.board_width, background="black")
        self.score = 0
        self.in_game = True

        """ apple starting position"""
        self.apple_x = 150
        self.apple_y = 150

        """snake movement direction"""
        self.move_x = Constraints.dot_size
        self.move_y = 0

        self.initialise_game()
        self.pack()

    def initialise_game(self):

        self.create_objects()
        self.bind_all("<Key>", self.on_key_press)
        self.after(Constraints.delay, self.on_timer)

    def create_circle_image(self, x, y, colour, tag):
        self.create_oval(x, y, x + Constraints.dot_size, y + Constraints.dot_size, fill=colour, tag=tag)

    def create_square_image(self, x, y, colour, tag):
        self.create_rectangle(x, y, x + Constraints.dot_size, y + Constraints.dot_size, fill=colour, tag=tag)

    def create_objects(self):
        """ create initial objects"""
        self.create_text(30, 10, text="Score: {0}".format(self.score), tag="score", fill="white")
        self.create_circle_image(50, 50, "red", "head")
        self.create_circle_image(40, 50, "green", "body")
        self.create_circle_image(30, 50, "green", "body")
        self.create_circle_image(20, 50, "green", "body")
        self.create_square_image(self.apple_x, self.apple_y, "white", "apple")

    def create_apple(self):
        """replace apple on the map"""

        apple = self.find_withtag("apple")
        self.delete(apple[0])

        snake = self.find_withtag("body") + self.find_withtag("head")
        exclude_set = [self.coords(body_part)[0:2] for body_part in snake]
        self.apple_x, self.apple_y = self.custom_random(exclude_set)

        self.create_square_image(self.apple_x, self.apple_y, "white", "apple")

    def custom_random(self, exclude_set):
        """ensures apple cannot spawn on top of snake"""
        random_x = random.randint(0, Constraints.apple_limit_position) * Constraints.dot_size
        random_y = random.randint(0, Constraints.apple_limit_position) * Constraints.dot_size
        if [random_x, random_y] in exclude_set:
            random_x, random_y = self.custom_random(exclude_set)
            return random_x, random_y
        else:
            return random_x, random_y

    def on_key_press(self, e):
        """bind arrow keys to change direction"""
        key = e.keysym

        if key == "Right" and self.move_x >= 0:
            self.move_x = Constraints.dot_size
            self.move_y = 0

        if key == "Left" and self.move_x <= 0:
            self.move_x = -Constraints.dot_size
            self.move_y = 0

        if key == "Up" and self.move_y <= 0:
            self.move_x = 0
            self.move_y = -Constraints.dot_size

        if key == "Down" and self.move_y >= 0:
            self.move_x = 0
            self.move_y = Constraints.dot_size

    def check_collision(self):
        """check collisions between head and body"""
        body = self.find_withtag("body")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1+2, y1+2, x2-2, y2-2)
        for over in overlap:
            if over in body:
                self.in_game = False
                break

        """check collisions between head and edge of map"""
        if x1+1 < 0 or x1+1 > Constraints.board_width - Constraints.dot_size \
                or y1+1 < 0 or y1+1 > Constraints.board_height - Constraints.dot_size:
            self.in_game = False

    def check_apple_collision(self):
        """check collision between snake and apple"""
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1+2, y1+2, x2-2, y2-2)
        if apple[0] in overlap:
            self.score += 1
            self.create_apple()
            return True
        else:
            return False

    def extend_snake(self):
        """adds a body part for snake"""
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.coords(head)
        self.create_circle_image(x1, y1, "green", "body")
        self.move(head, self.move_x, self.move_y)

    def move_snake(self):
        """move each body part of the snake"""
        body = self.find_withtag("body")
        head = self.find_withtag("head")

        snake = body + head

        z = 0

        while z < len(snake)-1:
            a1 = self.coords(snake[z])
            a2 = self.coords(snake[z+1])
            self.move(snake[z], a2[0] - a1[0], a2[1] - a1[1])
            z += 1

        self.move(head, self.move_x, self.move_y)

    def show_score(self):
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

    def game_over(self):
        """loser"""
        self.delete(tkinter.ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2,
                         text="Game Over! You have a score of {0}".format(self.score), fill="white")

    def on_timer(self):
        """ time incrementation"""
        self.show_score()
        self.check_collision()

        if self.in_game:
            apple_found = self.check_apple_collision()
            if apple_found:
                self.extend_snake()
            else:
                self.move_snake()
            self.after(Constraints.delay, self.on_timer)
        else:
            self.game_over()


class Snake(tkinter.Frame):

    def __init__(self):
        super().__init__()
        self.board = Board()
        self.pack()


def main():
    window = tkinter.Tk()
    window.title("Snake")
    Snake()
    window.mainloop()


if __name__ == '__main__':
    main()
