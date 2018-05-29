from skimage import io
import sys
import math
import numpy
import node
import segment

#========================================================================================================================

def generate_segments(in_tree, segments, im, X, Y, Z):

    #===================== Generate children ====================
    
    node_id = {}

    for i in range(0, len(in_tree)):

        node_id[in_tree[i]] = i

    number_of_children = []
    for i in range(0, len(in_tree)):
        number_of_children.append(0)

    for i in range(0, len(in_tree)):
        if in_tree[i].parent != None:

            number_of_children[node_id[in_tree[i].parent]] += 1

    leaves = []

    for i in range(0, len(in_tree)):

        if number_of_children[i] == 0:

            leaves.append(in_tree[i])

    #================ Calculate distance for nodes ==============

    dis = []
    for i in range(0, len(in_tree)):
        dis.append(0.0)

    leaf = []
    for i in range(0, len(in_tree)):
        leaf.append(None)

    for i in range(0, len(leaves)):

        tmp_leaf = leaves[i]

        tmp_child = leaves[i]
        tmp_parent = leaves[i].parent

        cid = node_id[leaves[i]]

        leaf[cid] = leaves[i]
        dis[cid] = float(im[leaves[i].x][leaves[i].y][leaves[i].z]) / 255.0

        while tmp_parent != None:

            pid = node_id[tmp_parent]

            tmp_dis = float(im[tmp_parent.x][tmp_parent.y][tmp_parent.z]) / 255.0 + dis[cid]

            if tmp_dis > dis[pid]:

                dis[pid] = tmp_dis
                leaf[pid] = leaf[cid]

            else:
                break

            tmp_child = tmp_parent
            cid = pid
            tmp_parent = tmp_parent.parent

    #================= Create hierarchy segments ====================

    leave_id = {}
    for i in range(0, len(leaves)):
        leave_id[leaves[i]] = i

    segment = {}

    for i in range(0, len(leaves)):

        tmp_leaf = leaves[i]
        tmp_root = leaves[i]
        tmp_root_parent = leaves[i].parent

        level = 1

        while tmp_root_parent != None && leave[node_id[tmp_root_parent]] == tmp_leave:

            if number_of_children[node_id[tmp_root]] >= 2:

                level += 1

            tmp_root = tmp_root_parent
            tmp_root_parent = tmp_root_parent.parent

        tmp_dis = dis[node_id[tmp_root]]

        tmp_segment = segment.segment(tmp_leaf, tmp_root, tmp_dis, level)
        segment[tmp_root] = tmp_segment
        segments.append(tmp_segment)

    for i in range(0, len(segments)):

        if segments[i].root.parent == None:

            segments[i].parent = None

        else:

            segments[i].parent = segment[segments[i].root.parent]

#========================================================================================================================

def hierarchy_prune(in_tree, out_tree, im, X, Y, Z, bkg_thresh, length_thresh, SR_ratio):

    T_max = 1000000 # (111 << sizeof(T))???

    #===================== Generate leaves ==========================

    leaves = []

    #================= Obtain hierarchy segments ====================

    segments = []

    generate_segments(in_tree, segments, im, X, Y, Z)
