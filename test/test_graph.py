import random
import math

import pyglet
from pyglet.gl import *

from data import construct_nodes, construct_edges, read_image_rgb

win = pyglet.window.Window()

def to_coord(xyz, size):
    return (xyz[1] - size[0]/2.0, -xyz[0] - size[0]/2.0, 0)

def draw_tri():
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(3,2,0);
    glVertex3f(-1,3,0)
    glVertex3f(0,0,0)
    glEnd()

def draw_graph(graph):
    glBegin(GL_POINTS)
    for pos, node in graph.iteritems():
        glColor3f(node.intensity[2] / 255.0, node.intensity[1] / 255.0, node.intensity[0] / 255.0)
        glVertex3f(*to_coord(node.coord,(0,0)))
    glEnd()

@win.event
def on_draw():
    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glEnable(GL_CULL_FACE);
    #glCullFace(GL_FRONT);
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60.0, 4.0/3.0, 1, 40);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    #gluLookAt(4*math.cos(theta), vert, 4*math.sin(theta), 0, 0, 0, 0, 1, 0);
    loc = to_coord((-10,-10,0), (0,0))
    look= to_coord(size, (0,0))
    gluLookAt(loc[0], loc[1], 20, look[0], look[1], look[2], 0, 1, 0);

    glScaled(0.1, 0.1, 0.1)
    #draw_tri()
    draw_graph(graph)

    print "drawn.."

nara = read_image_rgb('dataset/nara.png')
nara_seed = read_image_rgb('dataset/nara-seeds.png')
graph = construct_nodes(nara, nara_seed)
size = max(graph.keys())
print size
construct_edges(graph)
print "Done constructing graph"
pyglet.clock.schedule_interval(lambda x: win.dispatch_event('on_draw'), 1/30.0)
pyglet.app.run()
