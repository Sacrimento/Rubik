from vispy import scene, app
import numpy as np

from .cubie import Cubie

def init(cube):
    canvas = scene.SceneCanvas(title='Rubik', size=(800, 600), keys='interactive')

    view = canvas.central_widget.add_view()

    scale = 0.27

    for z in (-1, 0, 1):
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if x or y or z:
                    c = Cubie(scale, (x, y, z))
                    t = np.array(c.obj.transform.translate)
                    t[0], t[1], t[2] = x * scale, y * scale, z * scale
                    c.obj.transform.translate = t
                    view.add(c .obj)
                    c.colorize(cube)


    view.camera = 'turntable'

    canvas.show()

    app.run()
