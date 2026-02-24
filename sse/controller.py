
class Controller:
    """Controller is a class which defines behaviour(s) to the given entity."""

    def __init__(self, inputs):
        """Instanciate a new Controller Object.

        Args:
            self (Controller): Instance of Controller Object.
            inputs (dict): dict containing keyboard and mouse events.
        """
        self.keypressed = inputs["keys"]
        self.mouse = inputs["mouse"]
        self._contract = {}

        super().__init__()

    @staticmethod
    def _check_contract(fnc):
        """Decorator to check contracts element on given entity

        Args:
            fnc (method): Reference to Controller.update method

        Returns:
            method: The decorated method
        """
        def wrapper(self, entity, dt):
            """Decorator wrapper for _check_contract decorator. For each constraint declared into the contract, check if it's present on entity.

            Args:
                self (Controller): Instance of Controller Object.
                entity (sse.obj.Obj): The Object to update.
                dt (float): Delta time elapsed since previous call."""
            flag = True
            for category in self._contract:
                for element in self._contract[category]:
                    if category == "signal":
                        if entity.has_signal(element) is False:
                            flag = False
                    elif category == "property":
                        if entity.has_property(element) is False:
                            flag = False
                    elif category == "stat":
                        if entity.has_stat(element) is False:
                            flag = False
            # If the contract is successfull, launch the update
            if flag is True:
                fnc(self, entity, dt)
        return wrapper

    @_check_contract
    def update(self, entity, dt):
        """To be defined by the children. This method is called by the Scene through each Entity (obj) Objects.
        The update method set the entity properties for the current time.

        Args:
            self (Controller): Instance of Controller Object.
            entity (Obj): Reference to the Obj which call upade method.
            dt (float): time elapsed since last call.
        """
        pass

    def add_contract(self, category, name):
        """Add constraint on the controller contract. Constraints are like promises. If they are missing, the entity is not updated.

        Args:
            self (Controller): Instance of Controller Object.
            category (str): kind of constraint to add. It can be "property", "signal", "stat". None and "" values not allowed.
            name (str): unique given name to add. None and "" values not allowed.
        """
        if self._contract is None:
            self._contract = []

        if category is None or category == "" or name is None or name == "":
            return

        if category not in self._contract:
            self._contract[category] = []

        if name in self._contract[category]:
            return

        self._contract[category].append(name)
