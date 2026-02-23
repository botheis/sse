
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

        super().__init__()

    def update(self, entity, dt):
        """To be defined by the children. This method is called by the Scene through each Entity (obj) Objects.
        The update method set the entity properties for the current time.

        Args:
            self (Controller): Instance of Controller Object.
            entity (Obj): Reference to the Obj which call upade method.
            dt (float): time elapsed since last call.
        """
        pass
