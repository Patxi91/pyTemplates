class Shape:

    def __init__(self, color, is_polygon, description):
        self.color = color
        self.is_polygon = is_polygon
        self.description = description

    def display_data(self):
        print(f"\n=== {self.description.capitalize()} ===")
        print("Color:", self.color)
        print("Is the shape a polygon?", "Yes" if self.is_polygon else "No")

class Triangle(Shape):

    def __init__(self, color, vertices, base, height):
        Shape.__init__(self, color, True, "Triangle")
        self.vertices = vertices
        self.base = base
        self.height = height

class Circle(Shape):

    def __init__(self, color, radius):
        Shape.__init__(self, color, False, "Circle")
        self.radius = radius


#Driver code

triangle = Triangle("red", [(-2, 0), (2, 0), (0, 7)], 4, 7)
circle = Circle("blue", 6.3)

triangle.display_data()
circle.display_data()