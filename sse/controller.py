
class Controller:
    def __init__(self, inputs):
        self.keypressed = inputs["keys"]
        self.mouse = inputs["mouse"]
    
        super().__init__()

    def update(self, entity, dt):
        pass