class Scene:
    def __init__(self):
        self.nodes = []
        self.lights = []


    def add(self, node):
        self.nodes.append(node)

    def addLight(self, light):
        self.lights.append(light)

