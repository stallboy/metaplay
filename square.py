import numpy as np
import polyscope as ps
import polyscope.imgui as psim


def square(cnt=20, r=0.2, h=1):
    nodes = np.zeros((4 * cnt, 3))
    edges = np.zeros((4 * cnt, 2))

    n = np.array([[0.0, 0, 0], [0, h, 0], [1, h, 0], [1, 0, 0]])
    e = np.array([[0, 1], [1, 2], [2, 3], [3, 0]])
    nodes[:4] = n
    edges[:4] = e

    for i in range(1, cnt):
        a, b, c, d = n
        a2 = a * r + d * (1 - r)
        b2 = b * r + a * (1 - r)
        c2 = c * r + b * (1 - r)
        d2 = d * r + c * (1 - r)
        n = np.array([a2, b2, c2, d2])
        e = e + 4
        nodes[4 * i:4 * (i + 1)] = n
        edges[4 * i:4 * (i + 1)] = e

    return nodes, edges


num = 40
rate = 0.05
height = 1
ps_net = None


def curve():
    global ps_net
    if ps_net:
        ps_net.remove()

    nodes, edges = square(num, rate, height)
    ps_net = ps.register_curve_network("square", nodes, edges, radius=0.0014)
    color = np.random.rand(nodes.shape[0], 3)
    ps_net.add_color_quantity("color", color)


def callback():
    global num, rate, height
    changed1, num = psim.InputInt("num", num, step=1, step_fast=10)
    changed2, rate = psim.SliderFloat("rate", rate, v_min=0.01, v_max=0.99)
    changed3, height = psim.SliderFloat("height", height, v_min=0.2, v_max=3)

    if changed1 or changed2 or changed3:
        curve()


ps.init()
ps.set_ground_plane_mode('none')
ps.set_SSAA_factor(4)

ps.set_user_callback(callback)
curve()
ps.show()
