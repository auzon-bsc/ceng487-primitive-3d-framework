class Scene:
    def __init__(self):
        self.nodes = []
        self.lights = []
        self.isBlinn = False

    def add(self, node):
        self.nodes.append(node)

    def addLight(self, light):
        self.lights.append(light)

