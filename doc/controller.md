Create a Controller
===

The controller handle behaviours, set properties from objects.

**The controller can only access to the Entity object.** If the entity do some interactions with others objects, it has to be done through signals/slots and entity properties.

# Create a new Controller

We have to create a new Controller inherited from sse.controller.Controller.

```python
from sse.controller import Controller

class MyCtrl(Controller):
    def __init__(self, inputs):
        super().__init__(inputs)

    def update(self, entity, dt):
        pass
```

Here is the minimal form of a Controller.

# The init method

The init is called by the scene.controllers RessourceManager when we call :

```python
# Inside the Scene.__init__
self.controllers.load("MyCtrl", Myctrl)
```

To be precise the RessourceManager called a Scene._load_controller(ctrl) method.

The _load_controller instanciate the controller:

```python
tmp = ctrl(self.engine.get_inputs())
```

So, as you can see, we don't need to know what is the inputs parameter from init. The loader handles it by himself.

# Contracts
On init we can declare a contract.

The contract define what are the prerequires to work with objects.

## Declare a contract

We add contract during Controller instanciation:

```python
from sse.controller import Controller

class MyCtrl(Controller):
    def __init__(self, inputs):
        # Add a contract on property <hover>
        self.add_contract("property", "hover")

        # Add a contract on signal <clicked>
        self.add_contract("signal", "clicked")
```

## Not mandatory

The contracts are not mandatory, but they are usefull, to avoid to check manually if the object to update has the property (or another element).

Even though constraints are not mandatory, if it's defined as contract, it became mandatory.

## Constraints elements

We can check three kind of constraints:
- constraint on **property**
- constraint on **signal**
- constraint on **stat**

# update method

The update method is the controller core. The object mecanic is done here.

```python
def update(self, dt:float):
```
It takes one parameter **dt**. Dt corresponds to the delta time elapsed since the last call.

So if you need to calculate a new position depending on speed, we can imaging something like this:

```python
def update(self, dt:float):
    # Do things
    # ...
    # The speed is independant from the framerate
    speed = entity.property("move_speed")
    position = speed*dt
    # ...
    entity.property("x", position)
```

On update method, we can add/edit properties or signals or stats. We can also emit signals.

# Micro vs Macro

The SSE framework allows micro controllers (one controller for one behaviour) or macro controllers (one controller for one objects and all its behaviours).

The decision is up to the developper, and I assume to the circumstances.