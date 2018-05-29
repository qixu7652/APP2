from skimage import io
import sys
import math
import distance_transform
import construct_neuron_tree
import hierarchy_prune
import numpy
import node
import segment

#=============================== Set parameters ==================================

image_file = ""
length_thresh = 1.0
SR_ratio = 3.0 / 9.0
bkg_thresh = 30
cnn_type = int(2)
is_break_accept = False
channel = int(0)

im = io.imread("1.tif")

X = im.shape[0]
Y = im.shape[1]
Z = im.shape[2]

#===================== Distance transform using fast marching ====================

phi = numpy.zeros((X, Y, Z), dtype = numpy.float)

distance_transform.distance_transform(im, phi, X, Y, Z, cnn_type, bkg_thresh)

#=============================== Detect soma =====================================

soma_val = 0.0
soma = node.node(0, 0, 0)

for i in range(0, X):
    for j in range(0, Y):
        for k in range(0, Z):
            if phi[i][j][k] > soma_val:
                soma_val = phi[i][j][k]
                soma.x = i
                soma.y = j
                soma.z = k

#================== Construct neuron tree using fast marching ====================

neuron_tree = []

construct_neuron_tree.construct_neuron_tree(soma, phi, neuron_tree, X, Y, Z, cnn_type, bkg_thresh, is_break_accept)

#============================== Hierarchy prune ==================================

tree_after_pruning = []

hierarchy_prune.hierarchy_prune(neuron_tree, tree_after_pruning, im, X, Y, Z, bkg_thresh, length_thresh, SR_ratio)

#============================== Output SWC file ==================================
