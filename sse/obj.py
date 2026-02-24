class Signal:

    def __init__(self, obj, callback=None):
        """Instanciate a new Signal Object. Signal have almost the same usage as Qt signals. Under specific events, an object can emit a signal.
        When a signal is emitted, it triggers some actions to do (the callback).

        I.E.: When we click on a button, the signal <clicked> will be emitted. The callback will execute the code corresponding to
        "what to do" when the button is clicked.

        Args:
            self (Signal): Instance of Signal Object.
            obj (any): Reference to the Object which contains this Signal. Can be usefull when we are in the callback and the callback is a member another object.

                As example: objA is a Button. objB is a Popup. When when objA.isclicked is emitted, it calls objB.show method. And objB needs to modify objA parameter.

            callback (function, default=None): The callback to launch when this signal is emitted.
        """
        self._ref = obj
        self._callback = callback


    def connect(self, callback) -> bool:
        """Associate this signal to a callback method.

        Args:
            self: Instance of Signal Object.
            callback (callable): The method / function to call when this signal is emitted. If needed, it is possible to send parameters to the callback function through the emit call.
                None value is not permitted. If needed, the callback can be disconnected from the Signal by using disconnect method.

                I.E.: objA.emit("clicked", objA.property("x"), objA.property("y")) will send ObjA x and y properties (or None) if not defined.

        Returns:
            bool: True on success.
            False on failure. Empty callback gives a False result. Already connected Signal will result a False result.
        """

        # self._callback is already connected it is locked unless the disconnect method is called.
        if callback is None or self._callback is not None:
            return False
        self._callback = callback
        return True


    def disconnect(self):
        """Disconnect the callback from this Signal. Actually we can associate only one callback to a signal.

        Args:
            self: Instance of Signal object.
        """
        self._callback = None


    def is_connected(self) -> bool:
        """Only tells if the current Signal is connected to any callback.

        Args:
            self: Instance of Signal Object.

        Returns:
            bool: True if the Signal is connected to a callback. False if the Signal is not connected to a callback.
        """
        return self._callback != None


    def emit(self, *args, **kwargs):
        """If this Signal is connected to a callback, launch it without parameters.
        To launch a function with parameters, use a lambda function, on a wrapper function as callback.

        Args:
            self (Signal): Instance of Signal Object.
            *args (tuple): list of given parameters when the function has been called.
            **kwargs (dict): list of given named parameters when the function has been called.

        Returns:
            any: The value returned by the callback function.
        """
        if self._callback != None:
            return self._callback(*args, **kwargs)
        return True



class Property:
    """Property is one of the most important component of this lib.
    They are used to gives "configuration" values to objects.
    So a property can have a default value too.
    """

    def __init__(self, value, default_value=None):
        """Initialize a new property object.

        Args:
            self (Property): Property instanciation.
            value (any): the property value. The user has to know what he is pushing as property.
            default_value (any, default=None): A property can store a default value, used to restore the value attribute.
        """
        self._default_value = default_value
        self._value = value

    def get(self):
        """Get the property value.

        Args:
            self (Property): Instance of Property Object.

        Returns:
            any: the value stored as property.
        """
        return self._value

    def set(self, value):
        """Edit the property value.

        Args:
            self (Property): Instance of Property Object.
            value (any): the new value to store in this property.
        """
        self._value = value

    def get_default(self):
        """Get the default property value.

        Args:
            self (Property): Instance of Property Object.

        Returns:
            any: the default value of the Property Object."""
        return self._default_value

    def set_default(self, value):
        """Redefine the default value.

        Args:
            self (Property): Instance of Property Object.
            value (any): the new default value to set.
        """
        self._default_value = value

    def reset(self):
        """Reset the current value with the default value.

        Args:
            self (Property): Instance of Property Object.
        """
        self._value = self._default_value


class Stat:
    """Almost like Property object.
    Stat Object is more specialized in int min-max values. For example caracter strength stat in a game.
    """

    def __init__(self, min_value:int=0, max_value:int=100, value:int=0):
        """Instanciate a new Stat Object.

        Args:
            self (Stat): Instance of Stat Object.
            min_value (int, default=0): Minimale value allowed in the min-max range. Negative values are set to 0
            max_value (int, default=100): Maximale value allowed in the min-max range. If max value is <= to min value, max is set to min+1.
            value (int, default=0): Current value for this Stat.
                If value is lower than min value, it is set to min.
                If value is greater than max value, it is set to max.
                Else it is set to the given value.
            """
        self._max = self.set_max(max_value)
        self._min = self.set_min(min_value)
        self._value = self.set_value(value)

    def set_min(self, value):
        """Redefine the min value. Do some verifications.

        Args:
            self (Stat): Instance of Stat Object.
            value (int): Redefine the value, negative value are set to 0"""
        if value < 0 or value >= self.max:
            value = 0
        self._min = value

    def set_max(self, value):
        """Set the max value to the given value.
        If the given value is lower than min value, the max value is set to min+1.

        Args:
            self (Stat): Instance of Stat Object.
            value (int): value used to set the max value."""
        if value <= self._min:
            value = self._min +1
        self._max = value

    def set_value(self, value):
        """Set the current value to the given value. Do some verification on min-max values.
        If value <= min value then value = min.
        If value >= max value then value = max.

        Args:
            self (Stat): Instance of Stat object
            value (int): the new current value."""
        if value <= self.min:
            value = self.min
        elif value >= self.max:
            value = self.max
        self._value = value

    def get(self):
        """Get the current value.

        Args:
            self (Stat): Instance of Stat Object.

        Returns:
            int: the current value stored in this Stat Object."""
        return self._value


class Obj:
    """Generic Object used on Scene. An Obj can be a background or a button or text.
    The user defines it and defines how to use it."""

    def __init__(self):
        """Instanciate a new Obj Object

        Args:
            self (Obj): Instance of Obj Object.
                Takes no parameters to be versatile."""

        # Store here all the Obj stats
        self._stats = {}

        # Store here all the Obj Properties
        self._properties = {}

        # Store here all the Obj Signals
        self._signals = {}

        # Store here all the controllers associated to it.
        self._controller = []

        # Store the render used to display the Obj.
        self._renderer = None

        # Store the dependencies list to load the object
        self._dependencies = {
        }

    def add_stat(self, name:str, min_value:int=0, max_value:int=100, value:int=0) -> bool:
        """Create a new Stat Object and associate it to Obj.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique name of the new Stat associated. None or "" are not allowed.
            min_value (int, default=0): The min value for the new Stat.
            max_value (int, default=100): The max value for the new Stat.
            value (int, default=0): The current value for the new Stat.

        Returns:
            bool: True if the Stat has been created and added to the list of Obj stats.
                Or False if anything went wrong.
            """
        if name == "" or self._stats is None or name in self._stats:
            return False

        tmp = Stat(min_value, max_value, value)
        self._stats[name] = tmp
        return True

    def get_stat(self, name:str)->Stat|None:
        """Get the Stat Object from its given name. usefull to manipulate the Stat object directly.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name of the Stat to get.

        Returns:
            Stat: if a Stat object is associated to the given name.
            None: if nothing is found for the given name."""
        if name == "" or self._stats is None or name not in self._stats:
            return None
        return self._stats[name]

    def stat(self, name):
        """Get the Stat value from the given name.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name of Stat to get.

        Returns:
            int: if a Stat object has been found, returns its current value.
            None: if nothing is found for the given name."""
        if name == "" or self._stats is None or name not in self._stats:
            return None
        return self._stats[name].get()

    def has_stat(self, name:str)->bool:
        """Check if the current Obj has the Stat defined by the given name.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name of Stat to check.

        Returns:
            bool: True if a Stat has been found. Else returns false."""
        if self._stats is None or name == "":
            return False
        return name in self._stats

    def del_stat(self, name:str)->bool:
        """Delete a Stat from its given name.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name of Stat to del.

        Returns:
            bool: True if the stat has been found. Else returns False."""
        if name == "" or self._stats is None or name not in self.stats:
            return False
        del self._stats[name]
        return True

    # Manage Object Properties
    def add_property(self, name:str, value, default_value=None):
        """Create a new Property Object and associates it to the current Obj.
        The Property can be fully qualified by name, value and default_value.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the new Property Object. None and "" values are not allowed.
            value (any): Define the Property value. (None allowed).
            default_value (any, default=None): Define a default value for this property.

        Returns:
            bool: True if the property has been created and added. False if the Property already exists.
        """
        if name is None or name == "" or name in self._properties:
            return False

        self._properties[name] = Property(value, default_value)
        return True

    def get_property(self, name:str):
        """Get the Property Object by its given name. Usefull to modify it directly.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name associated to the Property Object.

        Returns:
            Property: if a Property Object is associated to the given name.
            Else returns None."""
        if name == "" or self._properties is None or name not in self._properties:
            return None
        return self._properties[name]

    def set_property(self, name:str, property:Property) -> Property|None:
        """Replace the Property Object associated to the given name by an another Property object.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique name associated to the Property to replace. None and "" are not allowed.
                If no property is associated to the given name, the replacement is not done.
            property (Property): The new property which will replace the current property associated to name. None not allowed.

        Returns:
            Property: The previous value associated to the given name. If nothing has been found: returns None."""
        if name is None or name == "":
            return None

        old = self.get_property(name)
        if property != None:
            self._properties[name] = property
        return old

    def property(self, name, value=None):
        """Quick acces to Property Objects. It's used to get/set the property value.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the Property. None and "" values are not allowed.
            value (any, default=None): If value is None, we are in get mode. Then returns the value of the property associated to the given name.
                If value is not None, set the property value associated to the given name with the new value.
                I.E.:
                    - elem.property("bg_color") # getter mode : get the value associated to the parameter bg_color.
                    - elem.property("bg_color", None) # getter mode : get the value associated to the parameter bg_color. It's not possible to set the value to None with the quick access. In this case, use add_property method.
                    - elem.property("bg_color", (0, 0, 0)) # setter mode: set the value (0, 0, 0) to the paramter bg_color.
        """
        if name is None or name == "":
            return None

        # Get mode
        prop = self.get_property(name)
        if value is None:
            return prop.get() if prop is not None else None
        else:
            old = prop.get() if prop is not None else None
            if prop is None:
                self.add_property(name, value)
            else:
                self._properties[name].set(value)
            return old

    def has_property(self, name):
        """Check if the property associated to the given name exists.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the Property. None or "" values are not allowed."""
        if name is None or name == "":
            return False

        return self._properties is not None and name in self._properties

    def del_property(self, name):
        """Delete a property associated to the given name.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the Property. None and "" values are not allowed.

        Returns:
            bool: True on success. Else False."""
        if name == "" or self._properties is None or name not in self._properties:
            return False
        del self._properties[name]
        return True

    # Manage Object Signals
    def add_signal(self, name, callback=None):
        """Create a new signal and associate it to the given name.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the signal. None and "" values are not allowed. The name can't be already associated.

        Returns:
            bool: True if the signal has been created. Else False."""
        if name is None or name == "" or name in self._signals:
            return False
        self._signals[name] = Signal(self, callback)
        return True

    def has_signal(self, name):
        """Check if Obj has a signal associated to the given name.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the signal. None and "" values are not allowed.

        Returns:
            bool: True if a signal has been found. Else False."""
        return name in self._signals

    def del_signal(self, name):
        """Delete the signal associated to the given name.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the signal. None and "" values are not allowed."""
        del self._signals[name]

    def signal_connect(self, name, callback):
        """Associate a signal to a callback.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the signal. None and "" values are not allowed.
            callback (function): Function associated to the signal.

        Returns:
            bool: True on success. Else False."""
        if name == "" or name is None or name not in self._signals:
            return False
        return self._signals[name].connect(callback)

    def signal_emit(self, name, *args, **kwargs):
        """Call the callback associated to the signal specified by the given name. The callback is called with generic parameters.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the signal. None and "" values are not allowed.
            *args (tuple): list of unnamed parameters given during the call.
            **wkargs (dict): list of named parameters given during the call.

        Returns:
            any: The value returned by the signal callback.
            """
        if name == "" or name not in self._signals:
            return False
        return self._signals[name].emit(*args, **kwargs)

    def signal_disconnect(self, name):
        """Disconnect the selected signal specified by its given name.

        Args:
            self (Obj): Instance of Obj Object.
            name (str): Unique given name for the signal. None and "" values are not allowed.

        Returns:
            bool: True if the signal has been disconnected. Else False."""
        if name == "" or name not in self._signals:
            return False
        return self._signals[name].disconnect()

    def update(self, dt):
        """Call the method update method. This method is automatically called by the Scene.

        Args:
            self (Obj): Instance of Obj Object.
            dt (float): Delta time elapsed since previous call."""
        if self._controller != []:
            for ctrl in self._controller:
                ctrl.update(self, dt)

    def render(self, screen):
        """Call the renderer display method. This method is automatically called by the Scene.

        Args:
            self (Obj): Instance of Obj Object.
            screen (pygame.surface.Surface): Reference to the screen Surface.
        """
        if self._renderer is not None:
            self._renderer.display(self, screen)

    def set_controller(self, controller):
        """Push a unique or a list of controllers on the controllers list.

        Args:
            self (Obj): Instance of Obj Object.
            controller (list|sse.controller.Controller): controller(s) to push. None value not allowed. Set the controller attribute to the given. Can be used to push several controllers with one call.

        Returns:
            bool: True on success. Else False."""
        if controller is None:
            return False

        if isinstance(controller, list):
            self._controller = controller
        else:
            self._controller = [controller]
        return True

    def add_controller(self, controller):
        """Add a controller to the list of controllers. An Obj can use several controllers.
        The controllers are loaded in the declaration order.

        Args:
            self (Obj): Instance of Obj Object.
            controller (sse.controller.Controller): The controller to associate. None value not allowed.

        Returns:
            bool: True on success. Else False."""

        if controller is None:
            return False
        if controller in self._controller:
            return True

        self._controller.append(controller)

    def set_renderer(self, renderer):
        """Associate a renderer to this Object.

        Args:
            self (Obj): Instance of Obj Object.
            renderer (sse.renderer.Renderer): the render to associate to this object. None value not allowed.

        Returns:
            bool: True on success. Else False."""

        if renderer is None:
            return False

        self._renderer = renderer
        return True


    def needs(self, category, name):
        """Add a dependecy to this object.

        Args:
            self (Obj): Instance of Obj Object.
            category (str): kind of dependency to add. It can be "controller", "renderer", "font", "texture". None and "" values not allowed.
            name (str): Unique given name of the dependency (name given in the ressource manageer). None and "" values not allowed.
        """
        if self._dependencies == None:
            self._dependencies = {}

        if category is None or category == "" or name is None or name == "":
            return

        if category not in self._dependencies:
            self._dependencies[category] = []

        if name in self._dependencies[category]:
            return

        self._dependencies[category].append(name)

    def get_needs(self):
        """Returns the dependencies list

        Args:
            self (Obj): Instance of Obj Object.

        Returns:
            dict: the dependencies full list"""
        return self._dependencies
