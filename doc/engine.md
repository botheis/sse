Create an Engine Object
===

Create a new SSE Engine object is the starting point for any project.
This Engine object is located in sse.engine.Engine.

```python
from sse.engine import Engine
```

To proceed, you need to :
- import the engine lib
- create an object
- to load a Scene 
- run the event loop.


```python
# Load what we need.
from sse.engine import Engine
from path.to.scenes import MyScene

title = "My SSE is so cool"
width = 800
height = 600

# Create a new engine object
engine = Engine(title, width, height)

# Load a Scene Object
engine.load_scene(MyScene)

# Run the event loop
engine.run()
```

In this example we are loading a scene *MyScene* but this object doesn't exist yet.

Let's go to the next chapter, where we will see how to [create a scene](scene.md) (or go back to [index](rtfm.md))