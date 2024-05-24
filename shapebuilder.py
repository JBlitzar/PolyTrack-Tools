from trackbuilder import TrackBuilder
import math

class ShapeBuilder(TrackBuilder):
    def __init__(self, name: str = "") -> None:
        super().__init__(name)
    
    def add_3d_line(self, p1: tuple[int, int, int], p2: tuple[int, int, int], thickness: int, id: int = 0, rot: int = 30) -> None:
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]
        length = math.sqrt(dx**2 + dy**2 + dz**2)

        if length == 0:
            return []  # Two points are the same, no line

        ux = dx / length
        uy = dy / length
        uz = dz / length

        points = []
        for t in range(0, int(length) + 1, thickness):
            x = p1[0] + ux * t
            y = p1[1] + uy * t
            z = p1[2] + uz * t
            points.append({'x': int(x), 'y': int(y), 'z': int(z), 'id':id, 'r':rot})
        
        # Add the last point
        points.append({'x': p2[0], 'y': p2[1], 'z': p2[2], 'id':id, 'r':rot})

        points = self._remove_duplicates(points)
        self.add_pieces(points)

    def add_box(self, dims: tuple[int, int, int], offset: tuple[int, int, int] = (0, 0, 0), rot: int = 0, id: int = 30) -> None:
        points = []
        # Weird order of for loops because I want to make it fill layer-by-layer
        for y in range(dims[1]):
            for x in range(dims[0]):
                for z in range(dims[2]):
                    points.append({'x': x + offset[0], 'y': y + offset[1], 'z': z + offset[2], 'r': rot, 'id':id, 'ckpt':None})
        print(len(points))
        self.add_pieces(points)

    
    def add_sphere(self, radius: float, num_points: int, rot: int = 0, id: int = 29) -> None:
        points = []
        phi = math.pi * (3. - math.sqrt(5.))  # Golden angle in radians

        for i in range(num_points):
            y = 1 - (i / float(num_points - 1)) * 2  # Range from -1 to 1
            radius_at_y = math.sqrt(1 - y * y) * radius

            theta = phi * i

            x = math.cos(theta) * radius_at_y
            z = math.sin(theta) * radius_at_y

            points.append({'x': int(x), 'y': int(y * radius) + radius, 'z': int(z), 'id':id, 'r':rot, "ckpt":None})
        self.add_pieces(points)

    
