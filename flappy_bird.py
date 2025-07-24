import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.vector import Vector


class Bird(Image):
    """
    The player's character. It has a velocity that is affected by gravity.
    """
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        # Give the bird an upward boost when the screen is touched
        self.velocity = 10  # Adjust this value for higher/lower jumps


class Pipe(Widget):
    """
    The pipe obstacles. Each Pipe widget manages a top and bottom pipe image.
    """
    # Constants for the pipe appearance and behavior
    PIPE_GAP = 200  # Gap between the top and bottom pipes
    PIPE_WIDTH = 80
    PIPE_VELOCITY = 4  # How fast the pipes move to the left

    # Properties to track state
    scored = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the top and bottom parts of the pipe
        self.top_pipe = Image(source='atlas://data/images/defaulttheme/button_pressed')
        self.bottom_pipe = Image(source='atlas://data/images/defaulttheme/button_pressed')
        self.add_widget(self.top_pipe)
        self.add_widget(self.bottom_pipe)

    def update_position(self, window_height):
        """
        Sets the initial vertical position of the pipes with a random gap.
        """
        # Randomly determine the center of the gap
        gap_center = random.randint(self.PIPE_GAP, window_height - self.PIPE_GAP)

        # Position the bottom pipe
        self.bottom_pipe.size = self.PIPE_WIDTH, gap_center - self.PIPE_GAP / 2
        self.bottom_pipe.pos = self.pos[0], 0

        # Position the top pipe
        self.top_pipe.size = self.PIPE_WIDTH, window_height - (gap_center + self.PIPE_GAP / 2)
        self.top_pipe.pos = self.pos[0], gap_center + self.PIPE_GAP / 2

    def move(self):
        """
        Moves the pipe to the left.
        """
        self.x -= self.PIPE_VELOCITY
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x


class Game(Widget):
    """
    The main game widget that contains all the game logic.
    """
    bird = ObjectProperty(None)
    pipes = ListProperty([])
    score = NumericProperty(0)
    game_over = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_label = Label(text=str(self.score), font_size='60sp', bold=True)
        self.add_widget(self.score_label)
        self.game_over_label = Label(text="", font_size='40sp', bold=True)
        self.add_widget(self.game_over_label)

    def on_size(self, *args):
        """
        Called when the window size changes. Used to position UI elements.
        """
        self.score_label.pos = self.width / 2 - self.score_label.width / 2, self.height * 0.8
        self.game_over_label.pos = self.width / 2 - self.game_over_label.width / 2, self.height / 2

    def start_game(self):
        """
        Initializes or resets the game state.
        """
        self.game_over = False
        self.score = 0
        self.score_label.text = str(self.score)
        self.game_over_label.text = ""

        # Reset bird position and velocity
        self.bird.center = self.center_x / 2, self.center_y
        self.bird.velocity = 0

        # Clear old pipes
        for pipe in self.pipes:
            self.remove_widget(pipe)
        self.pipes = []

        # Start the game loop and pipe spawning
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_pipe, 1.5)

    def spawn_pipe(self, dt):
        """
        Creates a new pipe and adds it to the game.
        """
        new_pipe = Pipe(pos=(self.width, 0))
        new_pipe.update_position(self.height)
        self.pipes.append(new_pipe)
        self.add_widget(new_pipe)

    def on_touch_down(self, touch):
        """
        Handles screen touches.
        """
        if self.game_over:
            # If the game is over, a touch restarts it
            self.start_game()
        else:
            # Otherwise, pass the touch to the bird to make it flap
            self.bird.on_touch_down(touch)

    def update(self, dt):
        """
        The main game loop, called every frame.
        """
        # --- Bird Physics ---
        # Apply gravity
        self.bird.velocity -= 0.5  # Gravity strength
        self.bird.y += self.bird.velocity

        # --- Pipe Logic ---
        pipes_to_remove = []
        for pipe in self.pipes:
            pipe.move()

            # Check for scoring
            if not pipe.scored and pipe.right < self.bird.x:
                pipe.scored = True
                self.score += 1
                self.score_label.text = str(self.score)

            # Check for collision with the bird
            if pipe.top_pipe.collide_widget(self.bird) or pipe.bottom_pipe.collide_widget(self.bird):
                self.end_game()

            # Mark pipes that are off-screen for removal
            if pipe.right < 0:
                pipes_to_remove.append(pipe)

        # Remove off-screen pipes
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
            self.remove_widget(pipe)

        # --- Collision with screen bounds ---
        if self.bird.top > self.height or self.bird.y < 0:
            self.end_game()

    def end_game(self):
        """
        Stops the game and displays a game over message.
        """
        if not self.game_over:
            self.game_over = True
            self.game_over_label.text = "Game Over\nTap to Restart"
            # Stop the game loop and pipe spawning
            Clock.unschedule(self.update)
            Clock.unschedule(self.spawn_pipe)


class FlappyBirdApp(App):
    """
    The main Kivy application class.
    """
    def build(self):
        game = Game()
        # We need to wait for the game widget to be fully initialized
        # before starting the game logic.
        Clock.schedule_once(lambda dt: game.start_game(), 1)
        return game


if __name__ == '__main__':
    FlappyBirdApp().run()