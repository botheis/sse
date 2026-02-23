import pygame
from sse.engine import Engine
from sse.scene import Scene
from sse.controller import Controller
from sse.renderer import Renderer
from sse.obj import Obj


"""Example:
Build a scene with a background and a button.
The background will be blue
The button will :
    - be gray
    - be lighter when the mouse is hover
    - launch the "quit" action when clicked

Note: Even if the render can directly define a default color, it is better to define properties in the object.
Like this the property can be used and manipulated by controllers.
"""



class ButtonScene(Scene):
    """Define a simple Scene which will display a background color and a button"""
    def __init__(self, engine:Engine):
        """Init Scene method
        
        Args:
            engine: reference to the ngine object"""
        super().__init__(engine)

        # Load controllers needed by the button.
        self.controllers.load("PressedCtrl", PressedCtrl)
        self.controllers.load("HoverCtrl", HoverCtrl)
        self.controllers.load("HoverColorCtrl", HoverColorCtrl)
        # Alternative : a controller which handle everything
        # self.controllers.load("ButtonCtrl", ButtonCtrl)

        # We need a background renderer, either for background and button
        self.renderers.load("BGRenderer", BGRenderer)


    def load(self):
        """Define the objects here"""
        # Add a background Obj
        background = Obj()

        # Define parameters needed by controllers and renderers
        background.property("x", 0)
        background.property("y", 0)
        background.property("w", self.engine.window.get_width())
        background.property("h", self.engine.window.get_height())
        background.property("bg_color", (100, 100, 220))

        # Associate controllers
        # No controller needed here
        
        # Associate renderers
        background.set_renderer(self.renderers.get("BGRenderer"))

        #
        # /!\ Background obj is completely useless. Technically there is a method on renderer object to do that: Renderer.fill
        #
        # The purpose here is to show there is several possibilities to get the result we want.
        #

        # Add a button Obj
        button = Obj()

        # Define parameters needed by controllers and renderers
        button.property("x", 50)
        button.property("y", 50)
        button.property("w", 100)
        button.property("h", 50)

        # Set the bg_color and a default value
        button.add_property("bg_color", (100, 100, 100), (100, 100, 100))
        # Define a hover color, it's better to use a defined color on hover, than calculate it.
        # If it's wrongly calculated,it can crashes
        button.property("bg_color_hover", (120, 120, 120))

        # Add signals
        # Add a <clicked> signal to the button, and associate it to the engine.stop method
        button.add_signal("clicked", self.engine.stop)

        # Associate Controllers to the button :
        # = associate behaviours to the button
        button.add_controller(self.controllers.get("PressedCtrl"))
        button.add_controller(self.controllers.get("HoverCtrl"))

        # Note it is possible to define a signal hover and handle this in a scene method
        # the signal method is used if we want to modify objects depending on other objetcs states
        button.add_controller(self.controllers.get("HoverColorCtrl"))

        # Associate renderer to the button
        button.set_renderer(self.renderers.get("BGRenderer"))

        self.entities.append(background)
        self.entities.append(button)


class PressedCtrl(Controller):
    """Micro Controller for <Button Pressed> event

    Properties:
        hover (bool): True when the mouse is hover the obj area.
    Emits:
        "clicked": when the button is clicked (only when the click is valided).
    """
    def __init__(self, inputs):
        """General init method
        
        Args:
            inputs (dict): Automatically given by the Scene. Corresponding to the engine inputs in realtime (almost).
            We can find mouse buttons states, mouse position, keyboard keydown states...
        """
        super().__init__(inputs)

    def update(self, entity, dt:float)->None:
        """Do the object' state update in realtime. If something happens, it happens here.

        Args:
            dt (float): delta time elapsed since last call.
            Can be needed for moves, where moves are depending on a speed and the time elapsed.
            new_pos = speed*dt
        """

        # Get the mouse state
        clicked = self.mouse()["left"] is True

        # Handle differents cases:

        # - clic + mouse not in the button : lock the button to <not clicked>
        if clicked is True and entity.property("hover") is False and entity.property("pressed_lock") is False:
            entity.property("pressed", False)
            entity.property("pressed_lock", True)

        # - clic + mouse in the button : lock the button to <clicked>
        if clicked is True and entity.property("hover") is True and entity.property("pressed_lock") is False:
            entity.property("pressed", True)
            entity.property("pressed_lock", True)

        # - clic released + mouse not in the button : unlock the button <clicked> & cancel the clicked action
        if clicked is False and entity.property("hover") is False:
            entity.property("pressed", False)
            entity.property("pressed_lock", False)

        # - clic released + mouse in the button : unlock the button <clicked> & emit the signal "clicked"
        if clicked is False and entity.property("hover") is True and entity.property("pressed") is True:
            entity.signal_emit("clicked")
            entity.property("pressed", False)
            entity.property("pressed_lock", False)



class HoverCtrl(Controller):
    """Micro Controller for <Mouse Hover Button> event
    
    Properties IN
        x (int): button x position
        y (int): button y position
        w (int): button width
        h (int): button height

    Properties OUT
        hover (bool): True if the mouse is hover the area
    Emits:
        No emit
    """

    def __init__(self, inputs):
        """General init method
        
        Args:
            inputs (dict): Automatically given by the Scene. Corresponding to the engine inputs in realtime (almost).
            We can find mouse buttons states, mouse position, keyboard keydown states...
        """
        super().__init__(inputs)

    def update(self, entity, dt):
        x = entity.property("x")
        y = entity.property("y")
        w = entity.property("w")
        h = entity.property("h")
        # mouse in the area
        pos = self.mouse()["pos"]
        if pos[0] >= x and pos[0] < x+w and pos[1] >= y and pos[1] < y+h:
            entity.property("hover", True)
        else:
            entity.property("hover", False)

class HoverColorCtrl(Controller):
    """Micro Controller for <Mouse Hover Button> event
    
    Properties
        hover (bool): True if the mouse is hover the button
        bg_color (tuple): (red, green, blue) where the values are between 0 and 255. Used by the render. This color changes on hover
        bg_color(default value) (tuple): (red, green, blue) where the values are between 0 and 255. Used to reset the bg_color when hover is False
        bg_color_hover (tuple): (red, green, blue) where the values are between 0 and 255. Used to set the hover color.
    Emits:
        No emit
    """

    def __init__(self, inputs):
        """General init method
        
        Args:
            inputs (dict): Automatically given by the Scene. Corresponding to the engine inputs in realtime (almost).
            We can find mouse buttons states, mouse position, keyboard keydown states...
        """
        super().__init__(inputs)

    def update(self, entity, dt):
        if entity is None:
            return

        # Reset the color with the default value
        color_property = entity.get_property("bg_color")
        color_property.reset()

        # get the color value
        color = color_property.get()

        if entity.property("hover") is True:
            # Calculate the hover color if bg_color_hover is not defined
            if entity.property("bg_color_hover") is None:
                color = ((color[0]+10)%255, (color[1]+10)%255, (color[2]+10)%255)
            else:
                color = entity.property("bg_color_hover")
            color_property.set(color)


class BGRenderer(Renderer):
    """BGRender fill the defined area with the bg_color.

    Parameters:
        x (int): x starting pos
        y (int): y starting pos
        w (int): width pos. (x+w) = x ending pos
        h (int): height pos. (y+h) = y ending pos
        bg_color (tuple): r,g,b tuple values where r,g,b are betweend 0 and 255.
    """
    def display(self, entity, screen):
        if entity is None or screen is None:
            return
        
        x = entity.property("x")
        y = entity.property("y")
        w = entity.property("w")
        h = entity.property("h")
        bg_color = entity.property("bg_color")
 
        self.draw_rect(screen, bg_color, (x, y, w, h))



if __name__ == "__main__":

    # To launch it from /path/to/sse
    # /path/to/sse $ python3 -m examples.simpleButton


    # Define a new engine
    engine = Engine("Test on display", 300, 300)

    # Load a specific Scene
    engine.load_scene(ButtonScene)

    # Launch the main loop
    engine.run()