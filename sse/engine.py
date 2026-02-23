import pygame

class Engine:
    """Engine is the Over the top Object. All elements are depending on it: It calls Scene which calls Obj which call Controller then call Renderer.
    It gives global configuration and states of the window.
    """

    def __init__(self, title="", width=800, height=600):
        """Instanciate a new Engine Object

        Args:
            self (Engine): Instance of Engine Object.
            title (str, default=""): The window title.
            width (int, default=800): The window width.
            height (int, default=600): The window height."""
        super().__init__()
        pygame.init()
        pygame.font.init()

        self.pygame_inited = pygame.get_init()
        self.title = title
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.window_width = width
        self.window_height = height

        self.mouse = {"left": False, "middle": False, "right": False, "pos":pygame.mouse.get_pos()}

        self.keyboard = pygame.key.get_pressed()

        self.fps = 60

        self.running = False

        self.current_scene = None
        self.clock = pygame.time.get_ticks()

    def inited(self):
        """Check if the engine has been inited.

        Args:
            self (Engine): Instance of Engine Object.

        Returns:
            bool: True if Engine is inited. Else False."""
        return pygame.get_init() and pygame.font.get_init() and self.window is not None

    def run(self):
        """Launch the engine event loop.

        Args:
            self (Engine): Instance of Engine Object."""
        if self.inited() == False:
            return

        self.running = True
        dt = 0.0
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(self.fps) / 1000

            self._listen()

            self._update(dt)
            self.render()

            pygame.time.get_ticks()

        pygame.font.quit()
        pygame.quit()


    def _listen(self):
        """Handle the keyboard and mouse events. This method should never be called outside the event loop.

        Args:
            self (Engine): Instance of Engine Object.
        """
        event = None
        # while event:=pygame.event.poll():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN or event.type==pygame.KEYUP:
                self.keyboard = pygame.key.get_pressed()
            if event.type == pygame.MOUSEMOTION:
                self.mouse["pos"] = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse["left"] = True
                elif event.button == 2:
                    self.mouse["middle"] = True
                elif event.button == 3:
                    self.mouse["right"] = True
                elif event.button == 4:
                    self.mouse["scroll_down"] = True
                elif event.button == 5:
                    self.mouse["scroll_up"] = True
                else:
                    pass
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse["left"] = False
                elif event.button == 2:
                    self.mouse["middle"] = False
                elif event.button == 3:
                    self.mouse["right"] = False
                elif event.button == 4:
                    self.mouse["scroll_down"] = False
                elif event.button == 5:
                    self.mouse["scroll_up"] = False

    def _update(self, dt):
        """
        Call the Scene update method. Should never be called outside the event loop.

        Args:
            self (Engine): Instance of Engine Object.
            dt (float): The time elapsed since last call."""
        if self.current_scene is not None:
            self.current_scene.update(dt)

    def render(self):
        """Call the Scene render method. Should never be called outside the event loop.

        Args:
            self (Engine): Instance of Engine Object."""
        self.window.fill((0, 0, 0))
        if self.current_scene is not None:
            self.current_scene.render(self.window)
        pygame.display.flip()

    def key_pressed(self, name):
        """Get the state of the key specified by its name.

        Args:
            self (Engine): Instance of Engine Object.
            name (str): the name of the key to check.

        Returns:
            bool: True if the key is pressed. Else False.
        """
        return self.keyboard[pygame.key.key_code(name)]

    def load_scene(self, scene):
        """Unload the current Scene and initialize a new scene object (specified in parameters) and load the scene load method.

        Args:
            self (Engine): Instance of Engine Object.
            scene (sse.scene.Scene): Reference to the (non instanciated) Scene Object.
            """
        self.unload_scene()
        self.current_scene = scene(self)
        self.current_scene.load()

    def unload_scene(self):
        """Unload the current Scene.

        Args:
            self (Engine): Instance of Engine Object.
        """
        self.current_scene = None

    def stop(self):
        """Stop the event loop.In general assimilated to quit.

        Args:
            self (Engine): Instance of Engine Object."""
        self.running = False

    def mouse_pressed(self, key):
        """Check if a mouse button is pressed.

        Args:
            self (Engine): Instance of Engine Object.
            key (str): the button name. Can be "left" "middle" "right" "scroll_up" or "scroll_down".

        Returns:
            bool: True if the button is pressed. Else False."""
        if key not in self.mouse:
            return False
        return self.mouse[key]

    def get_mouse_state(self):
        """Get the general mouse states, without any filters.

        Args:
            self (Engine): Instance of Engine Object.

        Returns:
            dict: mouse general state."""
        return self.mouse

    def get_mouse_pos(self):
        """Get the current mouse position. Filter on self.mouse

        Args:
            self (Engine): Instance of Engine Object.
        returns:
            tuple: (x, y) the position of the mouse.
        """
        return self.mouse["pos"]

    def get_inputs(self):
        """Get references to the inputs methods. Used by Scene.load_controller method.
        Args:
            self (Engine): Instance of Engine Object.

        Returns:
            dict: references to keyboard states and mouse states methods."""
        ret = {
            "keys": self.key_pressed,
            "mouse": self.get_mouse_state,
        }
        return ret

    def get_window_size(self):
        """Sortcut to get the window dimensions.

        Args:
            self (Engine): Instance of Engine Object.

        Returns:
            tuple: (width, height) the dimensions.
        """
        return self.window.get_size()
