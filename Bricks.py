# Import necessary stuff
import arcade
import random

# Setup classes:
# Window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Bricks Game"


ROW_COUNT = 3
BRICKS_IN_ROW = 10

# set ball size here so it can be used for collisions
BALL_SIZE = 10

# set brick size here for use in collisions
BRICK_WIDTH = 60
BRICK_HEIGHT = 40


# Game area
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)

    def setup(self):
        self.ball = Ball()
        self.bat = Bat()
        self.bricks = arcade.ShapeElementList()
        brick_y = 500
        row = 0
        num_bricks = 0
        # for each_brick in range(0, BRICKS_IN_ROW):
        #     # self.bricks.append(Brick(brick_x, new_brick_y))
        #     num_bricks += 1
        #     for row in range(0, ROW_COUNT):
        #         new_brick_y = brick_y + (row * BRICK_HEIGHT)
        #         brick_x = (BRICK_WIDTH / 2) + (num_bricks - 1) * BRICK_WIDTH
        #         brick = Brick(brick_x, new_brick_y)
        #         # draw_brick = arcade.draw_rectangle_filled(
        #         #                 #     brick.brick_c_x, brick.brick_c_y, BRICK_WIDTH, BRICK_HEIGHT, brick.colour
        #         #                 # )
        #         draw_brick = arcade.draw_rectangle_filled(50, 50, 50, 50, arcade.color.BEAU_BLUE)
        #         #raise RuntimeError(draw_brick)
        #         self.bricks.append(draw_brick)
        #         row += 1
        #     #return self.bricks

        draw_brick = arcade.draw_rectangle_filled(50, 50, 50, 50, arcade.color.BEAU_BLUE)
        self.bricks.append(draw_brick)

    def on_draw(self):
        # start rendering, must be done before any drawing
        arcade.start_render()
        arcade.draw_circle_filled(self.ball.center_x, self.ball.center_y, self.ball.size, self.ball.colour)
        arcade.draw_rectangle_filled(
            self.bat.center_x, self.bat.center_y, self.bat.width, self.bat.height, self.bat.colour
        )
        #for brick in self.bricks:
            #arcade.draw_rectangle_filled(brick.brick_c_x, brick.brick_c_y, BRICK_WIDTH, BRICK_HEIGHT, brick.colour)
        self.bricks.draw()

    def on_update(self, delta_time):
        self.ball.update(delta_time)
        self.ball.bounce(self.bat)
        self.ball.reset_position()

    def on_mouse_motion(self, x, y, dx, dy):
        self.bat.center_x = x
        self.bat.left = (self.bat.center_x - self.bat.width / 2)
        self.bat.right = (self.bat.center_x + self.bat.width / 2)
        self.bat.top = (self.bat.center_y + self.bat.height / 2)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.ball.delta_y = -200
        # waits for the mouse to be clicked to start the game


class Ball:
# Ball stuff:
    def __init__(self):
        self.center_x = 300
        self.center_y = 300
        self.delta_x = 0
        self.delta_y = 0
        self.size = BALL_SIZE
        self.colour = arcade.color.STIZZA

    # If the ball drops off the bottom
    def reset_position(self):
        if self.center_y < 0:
            self.center_x = 300
            self.center_y = 300
            self.delta_x = 0
            self.delta_y = 0

    # How the ball moves
    def update(self, delta_time):
        self.center_x += self.delta_x * delta_time
        self.center_y += self.delta_y * delta_time

    def bounce(self, bat):
        # Below are the bounce conditions upon hitting a wall
        if self.center_x < BALL_SIZE / 2:
            self.delta_x *= -1
        if self.center_x > SCREEN_WIDTH - BALL_SIZE / 2:
            self.delta_x *= -1
        if self.center_y > SCREEN_HEIGHT - BALL_SIZE / 2:
            self.delta_y *= -1

        # conditions for hitting the bat
        if (
                (self.center_x - BALL_SIZE / 2 < bat.right)
                and (self.center_x + BALL_SIZE / 2) > bat.left
                and (self.center_y - BALL_SIZE / 2 < bat.top)
        ):
            self.delta_y *= -1
            if self.center_x < bat.left:
                self.delta_x -= 10
            if self.center_x > bat.right:
                self.delta_x += 10

        # Below are the bounce conditions upon hitting a brick
        if (self.center_x + BALL_SIZE / 2 > brick.brick_c_x - (BRICK_WIDTH/2)
            and self.center_x - BALL_SIZE / 2 < brick.brick_c_x + (BRICK_WIDTH/2)
                and self.center_y + BALL_SIZE / 2 > brick.brick_c_y - (BRICK_HEIGHT / 2)
                    and self.center_y - BALL_SIZE / 2 < brick.brick_c_y + (BRICK_HEIGHT/2)):
                        self.delta_x *= -1
                        brick.level -= 1

        if (self.center_x - BALL_SIZE / 2 < brick.brick_c_x + (BRICK_WIDTH / 2)
            and self.center_x + BALL_SIZE / 2 > brick.brick_c_x - (BRICK_WIDTH / 2)
                and self.center_y + BALL_SIZE / 2 > brick.brick_c_y - (BRICK_HEIGHT / 2)
                    and self.center_y - BALL_SIZE / 2 < brick.brick_c_y + (BRICK_HEIGHT / 2)):
                        self.delta_x *= -1
                        brick.level -= 1

        if (self.center_y + BALL_SIZE / 2 > brick.brick_c_y - (BRICK_HEIGHT / 2)
            and self.center_y - BALL_SIZE / 2 < brick.brick_c_y + (BRICK_HEIGHT / 2)
                and self.center_x - BALL_SIZE / 2 < brick.brick_c_x + (BRICK_WIDTH / 2)
                    and self.center_x + BALL_SIZE / 2 > brick.brick_c_x - (BRICK_WIDTH / 2)):
                        self.delta_y *= -1
                        brick.level -= 1

        if (self.center_y - BALL_SIZE / 2 < brick.brick_c_y + (BRICK_HEIGHT / 2)
            and self.center_y + BALL_SIZE / 2 > brick.brick_c_y - (BRICK_HEIGHT / 2)
                and self.center_x - BALL_SIZE / 2 < brick.brick_c_x + (BRICK_WIDTH / 2)
                    and self.center_x + BALL_SIZE / 2 > brick.brick_c_x - (BRICK_WIDTH / 2)):
                        self.delta_y *= -1
                        brick.level -= 1


class Brick:
    # Bricks stuff

    def __init__(self, bbrick_x, bbrick_y):
        self.brick_c_x = bbrick_x
        self.brick_c_y = bbrick_y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.level = random.randint(1, 6)
       # self.level = 1
        self.colour = self.level_colour(self.level)

    def brick(self, brick_c_x, brick_c_y):
        arcade.draw_rectangle_filled(brick_c_x, brick_c_y, BRICK_WIDTH, BRICK_HEIGHT, self.colour)

    @staticmethod
    def level_colour(level):
        level_colour = {
            1: (170, 152, 169),
            2: (252, 247, 94),
            3: (158, 253, 56),
            4: (15, 192, 252),
            5: (204, 0, 255),
            6: (253, 14, 53),
        }
        return level_colour[level]




class Bat(object):
    # stuff about the bat
    width = 60
    height = 20
    center_x = 300
    center_y = 20
    colour = arcade.color.SUNSET

    def __init__(self):
        self.left = (self.center_x - self.width/2)
        self.right = (self.center_x + self.width/2)
        self.top = (self.center_y + self.height/2)


def main():

    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
