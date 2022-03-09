import numpy as np
import polyscope as ps
import polyscope.imgui as psim


def line(cnt=20, h=1):
    nodes = np.zeros((3 + 2 * cnt, 3))
    edges = np.zeros((2 + cnt, 2))

    # axis
    n = np.array([[0.0, 0, 0], [0, h, 0], [1, 0, 0]])
    e = np.array([[0, 1], [0, 2]])
    nodes[:3] = n
    edges[:2] = e

    h_seg = float(h) / cnt
    seg = 1.0 / cnt

    for i in range(1, cnt + 1):
        ns = 3 + 2 * (i - 1)
        es = 2 + (i - 1)

        new_nodes = np.array([[0.0, h - h_seg * i, 0], [seg * i, 0, 0]])
        nodes[ns: ns + 2] = new_nodes
        edges[es] = np.array([ns, ns + 1])

    return nodes, edges


num = 10
height = 1
ps_net = None


def curve():
    global ps_net
    if ps_net:
        ps_net.remove()

    nodes, edges = line(num, height)
    ps_net = ps.register_curve_network("line", nodes, edges, radius=0.0014)
    color = np.random.rand(nodes.shape[0], 3)
    ps_net.add_color_quantity("color", color)


def callback():
    global num, height
    changed1, num = psim.InputInt("num", num, step=1, step_fast=10)
    changed2, height = psim.SliderFloat("height", height, v_min=0.2, v_max=3)

    if changed1 or changed2:
        curve()


ps.init()
ps.set_ground_plane_mode('none')
ps.set_SSAA_factor(4)

ps.set_user_callback(callback)
curve()
ps.show()
