class Signal:

    def __init__(self, obj, callback=None):
        """
        Instanciate a new Signal Object. Signal have almost the same usage as Qt signals. Under specific events, an object can emit a signal.
        When a signal is emitted, it triggers some actions to do (the callback).

        I.E.: When we click on a button, the signal <clicked> will be emitted. The callback will execute the code corresponding to 
        "what to do" when the button is clicked.
    
        :param self: Signal Instanciation
        :param obj: Reference to the Object which contains this Signal. Can be usefull when we are in the callback and the callback is a member another object.
        As example: objA is a Button. objB is a Popup. When when objA.isclicked is emitted, it calls objB.show method. And objB needs to modify objA parameter.
        :param callback: The callback to launch when this signal is emitted
        """
        self._ref = obj
        self._callback = callback


    def connect(self, callback) -> bool:
        """
        Associate this signal to a callback method.
        
        :param self: Signal instanciated object
        :param callback: The method / function to call when this signal is emitted. If needed, it is possible to send parameters to the callback function through the emit call.
        None value is not permitted. If needed, the callback can be disconnected from the Signal by using disconnect method
        
        I.E.: objA.emit("clicked", objA.property("x"), objA.property("y")) will send ObjA x and y properties (or None) if not defined

        :return: True on success
        :return: False on failure. Empty callback gives a False result. Already connected Signal will result a False result.
        :rtype: bool
        """

        # self._callback is already connected it is locked unless the disconnect method is called.
        if self._callback is None:
            return False
        self._callback = callback
        return True


    def disconnect(self) -> bool:
        """
        Disconnect the callback from this Signal. Actually we can associate only one callback to a signal.
        
        :param self: Signal Instanciated object
        :return: True on success. Actually returns always True
        :rtype: bool
        """
        self._callback = None
        return True
    

    def is_connected(self) -> bool:
        """
        Only tells if the current Signal is connected to any callback.
        
        :param self: Signal Instanciated object
        :return: True if the Signal is connected to a callback. False if the Signal is not connected to a callback.
        :rtype: bool
        """
        return self._callback != None


    def emit(self, *args, **kwargs):
        """
        If this Signal is connected to a callback, launch it without parameters.
        To launch a function with parameters, use a lambda function, on a wrapper function as callback.
        :return: mixed value
        """
        if self._callback != None:
            return self._callback(*args, **kwargs)
        return True




class Property:
    _types = ["None", "bool", "int", "float", "str", "array", "dict"]

    def __init__(self, value, default_value=None):
        self._default_value = default_value
        self._value = value

    def get(self):
        return self._value
    
    def set(self, value):
        self._value = value

    def get_default(self):
        return self._default_value
    
    def set_default(self, value):
        self._default_value = value

    def reset(self):
        self._value = self._default_value


class Stat:
    def __init__(self, min_value:int=0, max_value:int=100, value:int=0):
        self._min = 0
        self._max = 100
        self._value = 0

    def set_min(self, value):
        if value < 0 or value >= self.max:
            value = 0
        self._min = value

    def set_max(self, value):
        if value <= self._min:
            value = self._min +1
        self._max = value

    def set_value(self, value):
        if value <= self.min:
            value = self.min
        elif value >= self.max:
            value = self.max
        self._value = value

    def get(self):
        return self._value


class Obj:
    def __init__(self):
        self._stats = {}
        self._properties = {}
        self._signals = {}
        self._controller = []
        self._renderer = None

    def add_stat(self, name:str, min_value:int=0, max_value:int=100, value:int=0) -> bool:
        if name == "" or self._stats is None or name in self._stats:
            return False
    
        tmp = Stat(min_value, max_value, value)
        self._stats[name] = tmp
        return True

    def get_stat(self, name:str)->Stat|None:
        if name == "" or self._stats is None or name not in self._stats:
            return None
        return self._stats[name]
    
    def stat(self, name):
        if name == "" or self._stats is None or name not in self._stats:
            return None
        return self._stats[name].get()
    
    def has_stat(self, name:str)->bool:
        if self._stats is None or name == "":
            return False
        return name in self._stats
    
    def del_stat(self, name:str)->bool:
        if name == "" or self._stats is None or name not in self.stats:
            return False
        del self._stats[name]
        return True
    
    # Manage Object Properties
    def add_property(self, name:str, value, default_value=None):
        if name == "" or name in self._properties:
            return False
        
        self._properties[name] = Property(value, default_value)
        return True

    def get_property(self, name:str):
        if name == "" or self._properties is None or name not in self._properties:
            return None
        return self._properties[name]
    
    def set_property(self, name:str, property:Property) -> Property|None:
        old = self.get_property(name)
        if property != None:
            self._properties[name] = property
        return old
    
    def property(self, name, value=None):
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
        return self._properties is not None and name in self._properties[name]
    
    def del_property(self, name):
        if name == "" or self._properties is None or name not in self._properties:
            return False
        del self._properties[name]
        return True        
    
    # Manage Object Signals
    def add_signal(self, name, callback=None):
        if name == "" or name in self._signals:
            return False
        self._signals[name] = Signal(self, callback)
        return True

    def has_signal(self, name):
        return name in self._signals

    def del_signal(self, name):
        del self._signals[name]
        return True

    def signal_connect(self, name, callback):
        if name == "" or name not in self._signals:
            return False
        return self._signals[name].connect(callback)

    def signal_emit(self, name, *args, **kwargs):
        if name == "" or name not in self._signals:
            return False
        return self._signals[name].emit(*args, **kwargs)

    def signal_disconnect(self, name):
        if name == "" or name not in self._signals:
            return False
        return self._signals[name].disconnect()


    def update(self, dt):
        if self._controller != []:
            for ctrl in self._controller:
                ctrl.update(self, dt)

    def render(self, screen):
        if self._renderer is not None:
            self._renderer.display(self, screen)

    def set_controller(self, controller):
        if controller is None:
            self._controller = []
            return False
        
        if isinstance(controller, list):
            self._controller = controller
        else:
            self._controller = [controller]
        return True
    
    def add_controller(self, controller):
        if controller is None:
            return False
        if controller in self._controller:
            return True
        
        self._controller.append(controller)
    
    def set_renderer(self, renderer):
        if renderer is None:
            return False
        
        self._renderer = renderer
        return True
