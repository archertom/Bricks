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

# SPRITE_SCALING_BAT
# SPRITE_SCALING_BALL
# SPRITE_SCALING_BRICK

# Drawing as primitives has not worked (it seems Python struggles to keep up with the drawing requirements).
    # Tried a ShapeElementList which should reduce the overhead, but had a failure from Arcade:
    # "AttributeError: 'NoneType' object has no attribute 'mode'" which suggests the primitives are arriving as
        # None rather than shapes.  Odd.
# Need to try redrawing the shapes as sprites, the Arcade examples show this can be coped with, and then it will be
    # possible to use the "collisions" method against a sprite list.


# Game area
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.set_mouse_visible(False)

        # Set up the sprite lists
        self.bat_list = None
        self.ball_list = None
        self.brick_list = None

        # Set up the player
        self.bat_sprite = None

    def setup(self):

        #set up the ball
        self.ball_list = arcade.SpriteList()
        self.ball_sprite = Ball(0.1)
        self.ball_list.append(self.ball_sprite)

        # set up the bat
        self.bat_list = arcade.SpriteList()
        self.bat_sprite = Bat(0.2)
        self.bat_list.append(self.bat_sprite)

        # set up the bricks
        #self.bricks = arcade.ShapeElementList()
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

        #draw_brick = arcade.draw_rectangle_filled(50, 50, 50, 50, arcade.color.BEAU_BLUE)
        #self.bricks.append(draw_brick)

    def on_draw(self):
        # start rendering, must be done before any drawing
        arcade.start_render()

        self.ball_list.draw()
        # arcade.draw_circle_filled(self.ball.center_x, self.ball.center_y, self.ball.size, self.ball.colour)
        self.bat_list.draw()

        #for brick in self.bricks:
            #arcade.draw_rectangle_filled(brick.brick_c_x, brick.brick_c_y, BRICK_WIDTH, BRICK_HEIGHT, brick.colour)
        #self.bricks.draw()


    def on_update(self, delta_time):

        self.ball_list.update()

    def on_mouse_motion(self, x, y, dx, dy):
        self.bat_sprite.center_x = x

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.ball_sprite.delta_y = -2
        # waits for the mouse to be clicked to start the game


class Ball(arcade.Sprite):
# Ball stuff:
    def __init__(self, sprite_scaling):
        super().__init__("ball red.png", sprite_scaling)
        self.center_x = 300
        self.center_y = 300
        self.delta_x = 0
        self.delta_y = 0


    # If the ball drops off the bottom
    def reset_position(self):
        self.center_x = 300
        self.center_y = 300
        self.delta_x = 0
        self.delta_y = 0


    # How the ball moves
    def update(self):
        self.center_x += self.delta_x
        self.center_y += self.delta_y

        if self.left < 0:
            self.delta_x *= -1

        if self.right > SCREEN_WIDTH:
            self.delta_x *= -1

        if self.bottom < 0:
            self.reset_position()

        if self.top > SCREEN_HEIGHT:
            self.delta_y *= -1


    def bounce(self, bat):
        # Below are the bounce conditions upon hitting a wall
        # if self.center_x < BALL_SIZE / 2:
        #     self.delta_x *= -1
        # if self.center_x > SCREEN_WIDTH - BALL_SIZE / 2:
        #     self.delta_x *= -1
        # if self.center_y > SCREEN_HEIGHT - BALL_SIZE / 2:
        #     self.delta_y *= -1

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


class Brick(arcade.Sprite):
    # Bricks stuff

    def __init__(self, bbrick_x, bbrick_y):
        self.brick_c_x = bbrick_x
        self.brick_c_y = bbrick_y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.level = random.randint(1, 6)
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




class Bat(arcade.Sprite):
    # stuff about the bat

    def __init__(self, sprite_scaling):
        super().__init__("bat yellow.png", sprite_scaling)
        self.center_x = 300
        self.center_y = 20


def main():

    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
