from trackgen import generateTrackCode
import math

def allIDs():
    trackPieces = {}
    for i in range(36):
        trackPieces[i] = [{"x":0,"y":0,"z":i,"r":0}]

    trackName = "EveryPieceID"

    print(generateTrackCode(trackName, trackPieces))


def generate_sphere(radius, num_points):
    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # Golden angle in radians

    for i in range(num_points):
        y = 1 - (i / float(num_points - 1)) * 2  # Range from -1 to 1
        radius_at_y = math.sqrt(1 - y * y) * radius

        theta = phi * i

        x = math.cos(theta) * radius_at_y
        z = math.sin(theta) * radius_at_y

        points.append({'x': int(x), 'y': int(y * radius), 'z': int(z)})

    return points


def remove_duplicates(points):
    unique_points = set((point['x'], point['y'], point['z']) for point in points)
    return [{'x': x, 'y': y, 'z': z} for x, y, z in unique_points]


def sphereTrack(radius):
    coords = remove_duplicates(generate_sphere(radius=radius, num_points=100000))

    coords = [{'x': i["x"], 'y': 3*(i["y"] + radius) + a, 'z': i["z"], 'r':0} for i in coords for a in range(1)]

    blockId = 30
    print(f"{len(coords)} blocks")

    trackData = {29:coords, 5:[{"x":0,"y":radius * 6 + 1,"z":0,"r":0}]}
    print(generateTrackCode("Sphere" + str(radius), trackData))


sphereTrack(50)
