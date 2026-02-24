Create a Scene Object
===

The scene is used as interface between all the components. It has the role to load objects, update them and render them.
On updating, some actions can be triggered through signals. One more time the Scene has to handle this signals.

Now we need to create a new Scene. All Scene are inherited from the object sse.scene.Scene.

```python
from sse.scene import Scene
```

# Create a new Scene

Now we know where is located the Scene object, we have to create a child from it:

```python
from sse.engine import Engine

class MyScene(Scene):
    def __init__(self, engine:Engine):
        super().__init__(engine)

        # HERE LOAD CONTROLLERS
        # HERE LOAD RENDERERS
        # here load fonts
        # here load images
        # ...

    @Scene._load_obj
    def load(self):
        # HERE LOAD ENTITIES
        pass
```

Congratuation you just created a new scene. 

Do you remember on the engine instanciation, we declared something like:
```python
from path.to.scenes import MyScene
# ...
# ...
# Load a Scene Object
engine.load_scene(MyScene)
```

The engine will instanciate for us the Scene object with the \_\_init \_\_ parameter given. To be precise, when we call the engine.load_scene method, the engine instanciate a new Scene Object, and just after, launch the Scene.load method.

# This Scene is useless...

To do something, our Scene needs 3 things:

- Entities (or Objects)
- Controllers
- Renderers

## Current state

In the current state, yes this scene is loaded, and that's all.

But you probably noticed 3 lines in the Scene declaration:
- \# HERE LOAD CONTROLLERS
- \# HERE LOAD RENDERERS
- \# HERE LOAD ENTITIES

We will load controllers, renderers, entities. And with that, our Scene will not be no longer useless.

# Load Entities

Previously we talked about objects. Entities and Obj are the same thing, it's just a question of semantic.

An Entity is an object in the scene container.

Please refers to the [create Obj](obj.md) section for details on objects creation. Here we have to see how to load then.

The Scene has this derivated method:
```python
    @Scene._load_obj
    def load(self):
        # define your objects here
        objA = Obj()
        objB = Obj()
        objC = Obj()
        # ...
        # ...
        # ...
        # At the end of declaration append the objs to the entities list
        self.entities.append(objA)
        self.entities.append(objB)
        self.entities.append(objC)
```

Yes... Thats all. Maybe you want extra info. 

After the entities are added into the self.entities list, the Scene will load the following decorator:

```python
# declare this decorator in all Scene.load, or you have to handle manually all the objects dependencies.

@Scene._load_obj
```

This decorator will try to associate all the dependencies to the obj.

Here we call dependency, any data handeled by a ressource manager. One more time go check on the [create Obj](obj.md) page to see what to do with objects.

# Ressource Manager

The Scene possesses some Ressource Managers. Actually it possesses a ressource manager for:
- controllers (yes it is a dependency)
- renderers (yes renderers too)
- fonts
- images

Each ressource manager has the same way to work: On the right ressource manager, we associate a unique name to an object Reference.

I.E.:
```python
# Don't forget, we are in a Scene.__init__, self refers to the Scene object.

# Load a controller called MyCtrl
self.controllers.load("MyCtrl", MyCtrl)

# Load a renderer called MyRenderer
self.renderers.load("MyRenderer", MyRenderer)


# Load a font located in /path/to.file.ttf, with the font-size of 20
self.fonts.load("MyFont", "/path/to/file.ttf", 20)

# or Texture / Surface
self.textures.load("MySurface", "/path/to/img.png")

```

## Load a Controller or a Renderer

Now we know how to load things on our Scene, we can load a controller called MyCtrl and a renderer called MyRenderer.

```python
# used only to declare the type for the __init__ param
from sse.engine import Engine

# Don't forget to 
from path.to.controllers import MyCtrl
from path.to.renderers import MyRenderer

class MyScene(Scene):
    def __init__(self, engine:Engine):
        super().__init__(engine)

        # HERE LOAD CONTROLLERS
        self.controllers.load("MyCtrl", MyCtrl)

        # HERE LOAD RENDERERS
        self.renderers.load("MyRenderer", MyRenderer)

    @Scene._load_obj
    def load(self):
        # HERE LOAD ENTITIES
        pass
```

## How to access to a ressource ?

The ressource manager gives access to a ressource through the get method:

```python
self.controllers.get("MyCtrl")
self.renderers.get("MyRenderer")
```

If a ressource is associated to "MyCtrl", the RessourceManager will returns the ressource. But if there is nothing found, the result of this call will be simply: **None**.

# And this Scene is ... Still useless

Wait, don't quit now. If I summarize what we saw:

- We have to create a new scene
- We have to declare which ressource the scene has to load
- We have to load Obj called Entities and their dependencies

In this chapter we saw how to load things into the Scene. But not how to create them.

You can visit other links:
- Go back to [index](rtfm.md)
- Go to [Obj creation](obj.md)
- Go to [Controller creation](controller.md)
- Go to [Renderer creation](renderer.md)
