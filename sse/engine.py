import pygame

class Engine:

    def __init__(self, title="", w=800, h=600):
        super().__init__()
        pygame.init()
        pygame.font.init()

        self.pygame_inited = pygame.get_init()
        self.title = title
        self.window = pygame.display.set_mode((w, h))
        pygame.display.set_caption(title)
        self.window_width = w
        self.window_height = h

        self.mouse = {"left": False, "middle": False, "right": False, "pos":pygame.mouse.get_pos()}

        self.keyboard = pygame.key.get_pressed()

        self.fps = 100

        self.running = False

        self.current_scene = None
        self.clock = pygame.time.get_ticks()

    def inited(self):
        return pygame.get_init() and pygame.font.get_init() and self.window is not None

    def run(self):
        if self.inited() == False:
            return
        
        self.running = True
        dt = 0.0
        clock = pygame.time.Clock()
        
        while self.running:
            dt = clock.tick(self.fps) / 1000

            self.listen()

            self.update(dt)
            self.render()

            pygame.time.get_ticks()

        pygame.font.quit()
        pygame.quit()


    def listen(self):
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

    def update(self, dt):
        if self.current_scene is not None:
            self.current_scene.update(dt)

    def render(self):
        self.window.fill((0, 0, 0))
        if self.current_scene is not None:
            self.current_scene.render(self.window)
        pygame.display.flip()

    def key_pressed(self, name):
        return self.keyboard[pygame.key.key_code(name)]

    def load_scene(self, scene):
        self.unload_scene()
        self.current_scene = scene(self)
        self.current_scene.load()

    def unload_scene(self):
        self.current_scene = None

    def resize_screen(self, w=800, h=600):
        pass

    def stop(self):
        self.running = False

    def mouse_pressed(self, key):
        if key not in self.mouse:
            return False
        return self.mouse[key]
    
    def get_mouse_state(self):
        return self.mouse

    def get_mouse_pos(self):
        return self.mouse["pos"]

    def get_mouse_clicks(self):
        return self.mouse_clicks

    def get_inputs(self):
        ret = {
            "keys": self.key_pressed,
            "mouse": self.get_mouse_state,
        }
        return ret

    def get_window_size(self):
        return self.window.get_size()