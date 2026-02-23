# Simple Structured Engine - SSE

Welcome to the SSE Project. SSE Project is a simple project that allows you to create graphicals elements, and render it.
I'm not a game developper so I can't tell for sure, but it could be usable as 2D game engine.

What I can say about SSE, it has a high flexibility. It gives to the developper generic tools to create interactions between objects, controllers, renders, others objects...

# How it works ?

SSE is based on pygame lib.
It defines an Engine (sse.engine.Engine) which will handle the init, the event loop, and display the final render.
On this engine we have to load a Scene (sse.scene.Scene). The scene tells which object is loaded, graphical elements is displayed, and how.

To proceed, a Scene needs basically 3 things:

- Objs (sse.obj.Obj)
- Controllers (sse.controller.Controller)
- Renderers (sse.renderer.Renderer)

Any Scene can load any Controller, Renderer or Object.

# Hierarchy
For example, we can create a hierarchy like this. The example shows that one controller can be used in several Scene. It is the same for the Renderer.

- Engine
  - SceneA
    - Controllers
      - ControllerA
      - ControllerB
      - ControllerC
    - Renderers
      - RendererA
    - Objs
      - ObjA
      - ObjB
      - ObjC
      - ObjD
  - SceneB
    - Controllers
      - ControllerA
      - ControllerD
      - ControllerE
    - Renderers
      - RendererA
      - RendererB
      - RendererC
    - Objs
      - ObjA
      - ObjD
      - ObjE

The MOST important thing to understand, is the user can do anything he wants.
- If the user wants to create micro controllers, he can.
- If the user wants to create macro controllers, he can.
- If the user needs specific renderer for a specific object, he can.
- If the user needs specific object he can heritate a new object.
- If the user needs signals, he can create as many as he wants

This Engine gives the user the possibility to create basics bricks. From this basics brics, the user can associate them alltogether to get a build.

Objects, controllers, renderers and scenes are highly exportable.

- To use a controller, we need to define the object properties needed.
- To use a renderer, we need defined properties.
- To use a signal, we need to define a "standard" name.
- Everything become a question of how this parameter is named

# The Scene

The scene has full access to the engine, to the controllers, renderers, and objects. It is the glue between all the elements.

In the Scene, we declare what to do when this signal is emitted, or which controller(s) (and/or which renderer) is used for this object.
- It is an interface to engine for controllers, renderer, objects.
- It define objects needed
- It define how objects will works (through controllers)
- It define how objects will works together (through signal-emit) and objects properties.
- It define how to render objects (through renderers).
- Call another Scene on event handled by signal. I.E.: _Load new scene when buttonA is clicked_

## Scene init
On initialization, the Scene declare the controllers and renderers it needs.

Each renderer and each controller are associated to a unique name.

```python
# Here we are in the Renderer.__init__ method

# ########### #
# CONTROLLERS #
# ########### #

# Load the MouseHover (micro) Controller
self.controllers.load("HoverCtrl", HoverCtrl)
# Load the Button pressed (micro) Controller
self.controllers.load("PressedCtrl", PressedCtrl)

# Load the Button (macro) Controller
self.controllers.load("ButtonQuitCtrl", ButtonQuitCtrl)

# ####### #
# RENDERS #
# ####### #

# Load the generic Button Renderer
self.renderers.load("ButtonRenderer", ButtonRenderer)

```

## Load objects

The objects are loaded separetely from initialization. They are declared in the **load** method.

```python
def load(self):
    # Empty all the objects stored in the scene
    self.entities = list([])

    btn_quit = Obj()
    # Gives property to the object
    btn_quit.add_property("x", 50)
    btn_quit.add_property("y", 50)
    btn_quit.add_property("w", 150)
    btn_quit.add_property("h", 50)

    # Associate the controllers needed by this object
    btn_quit.add_controller(self.controllers.get("HoverCtrl"))
    btn_quit.add_controller(self.controllers.get("PressedCtrl"))
    
    # Associate the renderer needed by this object
    btn_quit.set_renderer(self.renderers.get("PressedCtrl"))

    # Create a signal to this object
    btn_quit.add_signal("pressed", self.engine.quit)
```

To finish with the Scene, it needs to be loaded by the engine to be effective:

```python
# ############ #
# From a Scene #
# ############ #

# Call the scene loader from another Scene
self.engine.load_scene(MyScene)



# ############### #
# With the engine #
# ############### #

# Call the scene from outside
engine = Engine()
# do something here
engine.load_scene(MyScene)

# do something here

engine.run()
```

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

# The Objs

The objs are generic objects which can handle elements such as:

- property: config elements, such as bg_color etc.
- stats : if you want to separate stats like (health, strength) from properties, you can use stats
- signals: embedded signals which can be emitted by controllers.

Each Obj can be connected from 0 to many controllers.
It allows you to use micro controllers or macro controller(s), or if there is only rendering things to do, no controller at all.

For rendering, We try to avoid to use several renderers for one object. But if the object doesn't need to be rendered, it is possible to not associate it to any renderer.


The import point is you define what to do with your own Scenes, Controllers, Renderers and Objs.