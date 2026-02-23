import pygame

class RessourceManager:
    def __init__(self, loader):
        self._ressources = {}
        self._loader = loader

    def load(self, name, ressource, *args, **kwargs):
        try:
            self._ressources[name] = self._loader(ressource, *args, **kwargs)
            return True
        except Exception as e:
            return False

    def get(self, name):
        if name == "" or name not in self._ressources:
            return None
        return self._ressources[name]

    def has(self, name):
        return name in self._ressources


class Scene:
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.fonts = RessourceManager(self.load_font)
        self.textures = RessourceManager(self.load_texture)
        self.controllers = RessourceManager(self.load_controller)
        self.renderers = RessourceManager(self.load_renderer)
        self.sounds = RessourceManager(self.load_sound)
        self.entities = []

    def load(self):
        self.entities = list([])

    def load_font(self, filename, size=20):
        font = pygame.font.Font(filename, size)
        return font

    def load_controller(self, ctrl):
        return ctrl(self.engine.get_inputs())

    def load_renderer(self, renderer):
        return renderer()

    def load_texture(self, filename):
        texture = pygame.image.load(filename)
        return texture

    def unload_texture(self, name):
        pass

    def load_sound(self, name, filename):
        pass

    def unload_sound(self, name):
        pass

    def update(self, dt):
        for entity in self.entities:
            if hasattr(entity, "update"):
                entity.update(dt)
        # defined by children
        pass

    def render(self, screen):
        for entity in self.entities:
            if hasattr(entity, "render"):
                entity.render(screen)
