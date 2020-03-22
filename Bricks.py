# Import necessary stuff
import arcade
import random

# Setup classes:
# Window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Bricks by Fox Zero Games"

# set the layout here
ROW_COUNT = 6
BRICKS_IN_ROW = 20

# set ball speed here so it can be used for collisions
SPEED = -3

# set brick size here for use in collisions
BRICK_WIDTH = 30
BRICK_HEIGHT = 20

# adjust the scalings here
SPRITE_SCALING_BAT = 0.15
SPRITE_SCALING_BALL = 0.04
SPRITE_SCALING_BRICK = 0.095


# Game area
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        # self.set_mouse_visible(False)

        # Set up the sprite lists
        self.bat_list = None
        self.ball_list = None
        self.ball_sprite = None
        self.brick_list = None

        # Set up the player
        self.bat_sprite = None

        # Set up brick textures
        self.brick_textures = arcade.load_spritesheet("bricks textures.png", 300, 200, 6, 6)

        self.gameover = False

    def setup(self):

        self.gameover = False


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
                brick_sprite = Brick(SPRITE_SCALING_BRICK, self.brick_textures)
                brick_sprite.center_y = brick_y + (row * BRICK_HEIGHT)
                brick_sprite.center_x = (BRICK_WIDTH / 2) + (num_bricks - 1) * BRICK_WIDTH
                self.brick_list.append(brick_sprite)


    def on_draw(self):
        # start rendering, must be done before any drawing
        arcade.start_render()

        self.ball_list.draw()
        self.bat_list.draw()
        self.brick_list.draw()

        start_x = 400
        start_y = 15
        arcade.draw_text("Balls remaining: %d" % (self.ball_sprite.balls_left -1), start_x, start_y, arcade.color.WHITE)


        # gameover conditions
        if self.ball_sprite.balls_left < 1:
            self.game_over()


    def on_update(self, delta_time):
        self.ball_list.update()

        # Below are the bounce conditions upon hitting a brick
        self.ball_sprite.center_x += self.ball_sprite.delta_x
        direction_changed = False
        for brick in self.ball_sprite.collides_with_list(self.brick_list):
            if not direction_changed:
                if self.ball_sprite.delta_x > 0:
                    self.ball_sprite.right = brick.left
                    if self.ball_sprite.center_x < brick.left:
                        self.ball_sprite.delta_x -= random.uniform(1, 1.5)
                elif self.ball_sprite.delta_x < 0:
                    self.ball_sprite.left = brick.right
                    if self.ball_sprite.center_x > brick.right:
                        self.ball_sprite.delta_x += random.uniform(1, 1.5)
                self.ball_sprite.delta_x *= -1
                direction_changed = True

            if brick.level > 1:
                brick.level -= 1
                brick.set_texture(brick.level -1)
            else:
                brick.kill()
                if len(self.brick_list) == 0:
                    self.restart()


        self.ball_sprite.center_y += self.ball_sprite.delta_y
        for brick in self.ball_sprite.collides_with_list(self.brick_list):
            if not direction_changed:
                if self.ball_sprite.delta_y > 0:
                    self.ball_sprite.top = brick.bottom
                elif self.ball_sprite.delta_y < 0:
                    self.ball_sprite.bottom = brick.top

                self.ball_sprite.delta_y *= 1.01
                self.ball_sprite.delta_x *= 1.01
                self.ball_sprite.delta_y *= -1
                direction_changed = True

            if brick.level > 1:
                brick.level -= 1
                brick.set_texture(brick.level - 1)
            else:
                brick.kill()
                if len(self.brick_list) == 0:
                    self.restart()


        # collisions with walls
        if self.ball_sprite.left < 0:
            self.ball_sprite.delta_x *= -1
        if self.ball_sprite.right > SCREEN_WIDTH:
            self.ball_sprite.delta_x *= -1
        if self.ball_sprite.bottom < 0:
            self.ball_sprite.reset_position()
        if self.ball_sprite.top > SCREEN_HEIGHT:
            self.ball_sprite.delta_y *= -1


        # conditions for hitting the bat
        if self.ball_sprite.collides_with_sprite(self.bat_sprite):
            self.ball_sprite.delta_y *= -1
            self.ball_sprite.delta_y *= 1.01
            self.ball_sprite.delta_x *= 1.01

            if self.ball_sprite.center_x < self.bat_sprite.left:
                self.ball_sprite.delta_x -= random.uniform(1, 1.5)
            if self.ball_sprite.center_x > self.bat_sprite.right:
                self.ball_sprite.delta_x += random.uniform(1, 1.5)

            if self.ball_sprite.center_x < (
                self.bat_sprite.left + (self.bat_sprite.center_x - self.bat_sprite.left) -5
            ):
                self.ball_sprite.delta_x -= random.uniform(0, 0.5)
            if self.ball_sprite.center_x > (
                self.bat_sprite.right - (self.bat_sprite.right - self.bat_sprite.center_x) +5
            ):
                self.ball_sprite.delta_x += random.uniform(0, 0.5)


    def on_key_press(self, key, _modifiers):
        if self.gameover:
            self.restart()


    def on_mouse_motion(self, x, y, dx, dy):
        self.bat_sprite.center_x = x


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.ball_sprite.delta_y = SPEED
        # waits for the mouse to be clicked to start the game


    def restart(self):
        self.setup()


    def game_over(self):
        self.gameover = True
        start_x = 200
        start_y = 400
        arcade.draw_text("Game Over", start_x, start_y, arcade.color.WHITE)
        start_x = 200
        start_y = 300
        arcade.draw_text("Press spacebar to restart", start_x, start_y, arcade.color.WHITE)



class Ball(arcade.Sprite):
# Ball stuff:
    def __init__(self, sprite_scaling):
        super().__init__("ball red.png", sprite_scaling)
        self.center_x = 300
        self.center_y = 300
        self.delta_x = 0
        self.delta_y = 0
        self.balls_left = 4


    #If the ball drops off the bottom
    def reset_position(self):
        self.center_x = 300
        self.center_y = 300
        self.delta_x = 0
        self.delta_y = 0
        self.balls_left -= 1


class Brick(arcade.Sprite):
    # Bricks stuff

    def __init__(self, sprite_scaling, textures):
        randomising_list = [1] * 75 + [2] * 5 + [3] * 5 + [4] * 5 + [5] * 5 + [6] * 5
        level = random.choice(randomising_list)
        filename = self.level_colour(level)


        super().__init__(filename, sprite_scaling)
        self.level = level
        self.brick_c_x = 0
        self.brick_c_y = 0
        self.textures = textures


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
        self.center_y = 40


def main():

    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
