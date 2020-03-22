# Import necessary stuff
import arcade
import random

# Setup classes:
# Window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Bricks Game"

# set the layout here
ROW_COUNT = 6
BRICKS_IN_ROW = 20

# set ball size here so it can be used for collisions
BALL_SIZE = 10

# set brick size here for use in collisions
BRICK_WIDTH = 30
BRICK_HEIGHT = 20

# adjust the scalings here
SPRITE_SCALING_BAT = 0.1
SPRITE_SCALING_BALL = 0.03
SPRITE_SCALING_BRICK = 0.09

# Game redrawn as sprites, still need to work out collisions.  Should be possible with list collisions.
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
        self.ball_sprite = Ball(SPRITE_SCALING_BALL)
        self.ball_list.append(self.ball_sprite)

        # set up the bat
        self.bat_list = arcade.SpriteList()
        self.bat_sprite = Bat(SPRITE_SCALING_BAT)
        self.bat_list.append(self.bat_sprite)

        # set up the bricks
        self.brick_list = arcade.SpriteList()

        brick_y = 500
        num_bricks = 0

        for each_brick in range(0, BRICKS_IN_ROW):
            num_bricks += 1

            for row in range(0, ROW_COUNT):
                brick_sprite = Brick(SPRITE_SCALING_BRICK)
                brick_sprite.center_y = brick_y + (row * BRICK_HEIGHT)
                brick_sprite.center_x = (BRICK_WIDTH / 2) + (num_bricks - 1) * BRICK_WIDTH
                self.brick_list.append(brick_sprite)


    def on_draw(self):
        # start rendering, must be done before any drawing
        arcade.start_render()

        self.ball_list.draw()
        self.bat_list.draw()
        self.brick_list.draw()


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

    def __init__(self, sprite_scaling):
        level = random.randint(1, 6)
        filename = self.level_colour(level)

        super().__init__(filename, sprite_scaling)
        self.level = level
        self.brick_c_x = 0
        self.brick_c_y = 0


    @staticmethod
    def level_colour(level):
        level_colour = {
            1: "brick l1 grey.png",
            2: "brick l2 yellow.png",
            3: "brick l3 green.png",
            4: "brick l4 blue.png",
            5: "brick l5 purple.png",
            6: "brick l6 red.png",
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
