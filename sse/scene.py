import pygame


class RessourceManager:
    """RessourceManager gives a normalized interface to handle Scene ressources."""

    def __init__(self, loader):
        """Initialize a new RessourceManager Object.

        Args:
            self (RessourceManager): Instance of RessourceManager Object.
            loader (function): reference to a load ressource function"""
        self._ressources = {}
        self._loader = loader

    def load(self, name, ressource, *args, **kwargs):
        """Load a new ressource and associates it to the given name.

        Args:
            self (RessourceManager): Instance of RessourceManager Object.
            name (str): Unique given name to the ressource. None and "" values not allowed.
            ressource (object): Reference to the ressource object to instanciate.
            *args (tuple): list of parameters needed by the ressource init function
            **kwargs (dict): dict of named parameters needed by the ressource init function.

        Returns:
            bool: True on success. Else False.
            """
        try:
            self._ressources[name] = self._loader(ressource, *args, **kwargs)
            return True
        except Exception as e:
            return False

    def get(self, name):
        """Get the ressource from the given name.

        Args:
            self (RessourceManager): Instance of RessourceManager Object.
            name (str): Unique given name of the ressource. None and "" values are not allowed.

        Returns:
            object: If found returns the object associated to the name. Else returns None.
        """
        if name is None or name == "" or name not in self._ressources:
            return None
        return self._ressources[name]

    def has(self, name):
        """Check if the ressource manager has a ressource associated to the given name.

        Args:
            self (RessourceManager): Instance of RessourceManager Object.
            name (str): Unique given name. None and "" values are not allowed.

        Returns:
            bool: True if a ressource is associated to the given name. Else False."""
        return name in self._ressources


class Scene:
    """Scene is loaded by the engine, and loads all needed components:
    - controllers
    - renderers
    - fonts
    - images
    - obj

    Then the Scene Object connects everybody all together.
    """
    def __init__(self, engine):
        """Instanciate a new Scene Object

        Args:
            self (Scene): Instance of Scene Object.
            engine (sse.engine.Engine): Reference to engine Object."""
        super().__init__()
        self.engine = engine
        self.fonts = RessourceManager(self._load_font)
        self.textures = RessourceManager(self._load_texture)
        self.controllers = RessourceManager(self._load_controller)
        self.renderers = RessourceManager(self._load_renderer)
        self.entities = []

    def load(self):
        """NEED TO BE REDEFINED BY CHILDREN. By default only reset the entities list.

        Args:
            self (Scene): Instance of Scene Object."""
        self.entities = list([])

    def _load_font(self, filename, size=20):
        """Load ttf font from its filename. This method is automatically launched by the Font RessourceManager when scene.fonts.load method is called.

        Args:
            self (Scene): Instance of Scene Object.
            filename (str): The path to the TTF file.
            size (int): The font size used on the font file.

        Returns:
            pygame.font.Font: the new Font."""
        font = pygame.font.Font(filename, size)
        return font

    def _load_controller(self, ctrl):
        """Load a new Controller. This method is automatically launched by the Controller RessourceManager when scene.controllers.load method is called.

        Args:
            self (Scene): Instance of Scene Object.
            ctrl (sse.controller.Controller): Instanciate a new Controller object.

        Returns:
            sse.controller.Controller: Instance of Controller."""
        return ctrl(self.engine.get_inputs())

    def _load_renderer(self, renderer):
        """Load a new Renderer. This method is automatically launched by the Renderer RessourceManager when scene.renderers.load method is called.

        Args:
            self (Scene): Instance of Scene Object.
            renderer (sse.renderer.Renderer): Instanciate a new Renderer object.

        Returns:
            sse.renderer.Renderer: Instance of Renderer."""
        return renderer()

    def _load_texture(self, filename):
        """Load a new Image as Texture. This method is automatically launched by the Texture RessourceManager when scene.textures.load method is called.

        Args:
            self (Scene): Instance of Scene Object.
            filename (str): The path to the image.

        Returns:
            pygame.surface.Surface: Instance of Texture (in sdl2.x) / Surface (in sdl1.x) """
        texture = pygame.image.load(filename)
        return texture

    def _update(self, dt):
        """On all entities, launch update method.

        Args:
            self (Scene): Instance of Scene Object.
            dt (float): The time elapsed since previous call.
        """
        for entity in self.entities:
            if hasattr(entity, "update"):
                entity.update(dt)

    def _render(self, screen):
        """On all entities, launch the render method.

        Args:
            self (Scene): Instance of Scene Object.
            screen (pygame.surface.Surface): The engine.window surface."""
        for entity in self.entities:
            if hasattr(entity, "render"):
                entity.render(screen)
