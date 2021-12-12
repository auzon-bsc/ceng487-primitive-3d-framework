class Color3f:

    def __init__(self, red, green, blue):
        self.red = red,
        self.green = green,
        self.blue = blue

    def __repr__(self):
        return f"Color3f(red={self.red}, green={self.green}, blue={self.blue}"

    def toList(self):
        return [self.red, self.green, self.blue]


class Color4f(Color3f):

    def __init__(self, red, green, blue, alpha):
        super().__init__(red, green, blue)
        self.alpha = alpha

    def __repr__(self):
        return f"Color4f(red={self.red}, green={self.green}, blue={self.blue}, alpha={self.alpha})"

    def toList(self):
        return super().toList() + [self.alpha]
