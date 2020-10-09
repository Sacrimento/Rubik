from bitarray import bitarray

class ShiftedBitArray(bitarray):
    INDEXES_TRANSFORM = {
        (0, 0): 0,
        (1, 0): 1,
        (2, 0): 2,
        (0, 1): 7,
        (2, 1): 3,
        (0, 2): 6,
        (1, 2): 5,
        (2, 2): 4,
    }

    BASE_COLOR = None

    def __lshift__(self, count):
        return self[count:] + self[:count]

    def __rshift__(self, count):
        return self[-count:] + self[:-count]

    def set(self, index, val):
        self[index*4:index*4+4] = bitarray(val)
        return self

    def get(self, index):
        return self[index*4:index*4+4].to01()

    def get_color(self, x, y):
        if self.INDEXES_TRANSFORM.get((x, y)) is None:
            return
        return int(self.get(self.INDEXES_TRANSFORM.get((x, y))), 2)

class Cube:
    FACES = {
        'F': {'R': (0, 7, 6), 'D': (2, 1, 0), 'L': (4, 3, 2), 'T': (6, 5, 4)},
        'R': {'B': (4, 3, 2), 'D': (4, 3, 2), 'F': (4, 3, 2), 'T': (4, 3, 2)},
        'B': {'L': (0, 7, 6), 'D': (6, 5, 4), 'R': (4, 3, 2), 'T': (2, 1, 0)},
        'L': {'F': (0, 7, 6), 'D': (0, 7, 6), 'B': (0, 7, 6), 'T': (0, 7, 6)},
        'T': {'F': (2, 1, 0), 'L': (2, 1, 0), 'B': (6, 5, 4), 'R': (2, 1, 0)},
        'D': {'F': (6, 5, 4), 'R': (6, 5, 4), 'B': (2, 1, 0), 'L': (6, 5, 4)},
    }

    def __init__(self):
        self.cube = {}
        for i, f in enumerate(self.FACES):
            byte = i
            byte |= i << 4
            self.cube[f] = ShiftedBitArray(bin(byte)[2:].zfill(8) * 4)

    def twist(self, face, clockwise):
        involved = self.FACES[face]
        if clockwise:
            self.cube[face] >>= 4
        else:
            self.cube[face] <<= 4
        
        faces = list(involved.keys())
        save = []
        for i in reversed(range(len(involved))):
            last = i == 0
            first = i == 3
            dst_face = faces[i]
            dst_face_idx = involved[dst_face]
            src_face = faces[(i - 1) % 4]
            src_face_idx = involved[src_face]
            if first:
                save = [self.cube[dst_face].get(j) for j in dst_face_idx]
            if last:
                for val, dst_idx in zip(save, dst_face_idx):
                    self.cube[dst_face].set(dst_idx, val)
            else:
                for src_idx, dst_idx in zip(src_face_idx, dst_face_idx):
                    val = self.cube[src_face].get(src_idx)
                    self.cube[dst_face].set(dst_idx, val)

    def apply(self, seq):
        pass

    def __repr__(self):
        out = ''
        for face in self.FACES:
            out += str([int(self.cube[face].get(i), 2) for i in range(8)]) + '\n'
        return out