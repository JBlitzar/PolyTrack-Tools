# from trackinfo import gen_track_code
import math

# def all_IDs() -> str:
#     track_pieces = {}
#     for i in range(36):
#         track_pieces[i] = [{"x":0,"y":0,"z":i,"r":0}]

#     track_name = "EveryPieceID (Almost)"

#     return gen_track_code(track_name, track_pieces)


def remove_duplicates(points) -> list[dict[str, int]]:
    unique_points = set((point['x'], point['y'], point['z']) for point in points)
    return [{'x': x, 'y': y, 'z': z} for x, y, z in unique_points]


def gen_sphere(radius: float, num_points: int, offset: tuple[int, int, int] = (0,0,0), rot: int = 0) -> list[dict[str, int]]:
    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # Golden angle in radians

    for i in range(num_points):
        y = 1 - (i / float(num_points - 1)) * 2  # Range from -1 to 1
        y += offset[1]
        radius_at_y = math.sqrt(1 - y * y) * radius

        theta = phi * i

        x = math.cos(theta) * radius_at_y + offset[0]
        z = math.sin(theta) * radius_at_y + offset[2]

        points.append({'x': int(x), 'y': int(y * radius), 'z': int(z), 'r': rot})

    return remove_duplicates(points)


def gen_box(dims: tuple[int, int, int], offset: tuple[int, int, int] = (0, 0, 0), rot: int = 0) -> list[dict[str, int]]:
    points = []
    # Weird order of for loops because i want to make it fill layer-by-layer
    for y in range(dims[1]):
        for x in range(dims[0]):
            for z in range(dims[2]):
                points.append({'x': x + offset[0], 'y': y + offset[1], 'z': z + offset[2], 'r': rot})
    print(len(points))
    return points


# def sphere_track(radius: float) -> str:
#     coords = gen_sphere(radius=radius, num_points=100000)

#     coords = [{'x': i["x"], 'y': 3*(i["y"] + int(radius)), 'z': i["z"], 'r':0} for i in coords]

#     _block_id = 30
#     # print(f"{len(coords)} blocks")

#     track_data = {29:coords, 5:[{"x":0,"y":int(radius) * 6 + 1,"z":0,"r":0}]}
#     return gen_track_code("Sphere" + str(radius), track_data)
