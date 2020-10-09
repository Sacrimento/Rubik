from vispy import scene
from vispy.visuals import transforms

RUBIK_COLORS = {
    0: [(0, 0, 1, 1), (0, 0, 1, 1)],
    1: [(1, 0, 0, 1), (1, 0, 0, 1)],
    2: [(0, 1, 0, 1), (0, 1, 0, 1)],
    3: [(1, 0.65, 0, 1), (1, 0.65, 0, 1)],
    4: [(1, 1, 0, 1), (1, 1, 0, 1)],
    5: [(1, 1, 1, 1), (1, 1, 1, 1)],
    -1: [(0.41, 0.41, 0.41, 1), (0.41, 0.41, 0.41, 1)]
}

class Cubie:
    FACES = 6

    def __init__(self, scale, coo):
        self.obj = scene.visuals.Box(
            width=1,
            height=1,
            edge_color='black'
        )

        self.obj.transform = transforms.STTransform(
            translate=(0., 0., 0.),
            scale=(scale, scale, scale)
        )

        self.coo = coo

    def get_face(self):
        x, y, z = self.coo
        faces = []
        if y == -1:
            faces.append('F')
        if y == 1:
            faces.append('B')
        if x == 1:
            faces.append('R')
        if x == -1:
            faces.append('L')
        if z == -1:
            faces.append('D')
        if z == 1:
            faces.append('T')
        return faces

    def d2_coo(self, face):
        x, y, z = self.coo
        x, y, z = x + 1, y + 1, z + 1
        if face == 'F':
            return x, z
        elif face == 'R':
            return y, z
        elif face == 'L':
            return 2 - y, z
        elif face == 'T':
            return x, 2 - y
        elif face == 'D':
            return x, y
        elif face == 'B':
            return x, 2 - z

    def colorize(self, raw_cube):
        faces = self.get_face()
        face_colors = {'F': -1, 'B': -1, 'L': -1, 'R': -1, 'T': -1, 'D': -1}

        for face in faces:
            cube_face = raw_cube.cube[face]
            x, y = self.d2_coo(face)
            color = cube_face.get_color(x, y) or list(raw_cube.FACES).index(face)
            face_colors[face] = color

        final_colors = []
        for face in ('D', 'T', 'F', 'B', 'L', 'R'):
            final_colors += RUBIK_COLORS[face_colors[face]]

        self.obj.mesh.mesh_data.set_face_colors(final_colors)
