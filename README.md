# Simple Structured Engine - SSE

Welcome to the SSE Project. SSE Project is a simple project that allows you to create graphicals elements, and render it.
I'm not a game developper so I can't tell for sure, but it could be usable as 2D game engine.

What I can say about SSE, it has a high flexibility. It gives to the developper generic tools to create interactions.

# How it works ?

SSE is based on pygame lib.
It defines an Engine (sse.engine.Engine) which will handle the init, the event loop, and display the final render.
On this engine we have to load a Scene (sse.scene.Scene). The scene tells which graphical elements is displayed, and how.

To proceed, a Scene needs basically 3 things:

- Objs (sse.obj.Obj)
- Controllers (sse.controller.Controller)
- Renderers (sse.renderer.Renderer)

# The Scene

The scene has access to the engine, to the controllers, renderers, and objects.
First of all the minimal code fo a new Scene:

# The Controller

An object needs a controller to be ... controlled. Each Controllers define a method :
```python
# update method prototype to redefine on every Child Controller
def update(entity:Obj, dt:float) -> None
```

Depending on the events, the scene etc. a specific object can use this controller instead of this one.
For example: it is possible to define a button object, and associate it to the LaunchSomethingController. It is also possible to associate a button to the MoveSomethingController.

Also the Controllers have access to the inputs thanks to the following methods:

- keypressed 
- mouse state


# The Renderer

An Object can be displayed. To do that it has to be associated to a renderer. The renderer will specify how to display, with what color and so on. Each Renderer define a method:
```python
def display(self, entity:Obj, screen:pygame.surface.Surface) -> None:
```

Further more a Renderer has some paint shortcuts such as:
```python

# Fill the area defined by pos with the color
def draw_rect(self, screen, color, pos) -> void:
```