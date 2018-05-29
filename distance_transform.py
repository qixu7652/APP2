from skimage import io
import sys
import math
import numpy
import node
import heap_for_fast_marching

#======================================================================================================================================================================
    
def distance_transform(im, phi, X, Y, Z, cnn_type, bkg_thresh):

    ALIVE = -1
    TRIAL = 0
    FAR = 1

    INF = float(1.1e+20)

    state = numpy.zeros((X, Y, Z), dtype = numpy.int)

    for i in range(0, X):
        for j in range(0, Y):
            for k in range(0, Z):
                
                if im[i][j][k] <= bkg_thresh:
                    phi[i][j][k] = float(im[i][j][k])
                    state[i][j][k] = ALIVE
                else:
                    phi[i][j][k] = INF
                    state[i][j][k] = FAR

    #================ Initialize heap =================

    hp = heap_for_fast_marching.MyHeap(X, Y, Z)

    for i in range(0, X):
        for j in range(0, Y):
            for k in range(0, Z):

                if state[i][j][k] == ALIVE:

                    for kk in range(-1, 2):

                        k2 = k + kk
                        if k2 < 0 or k2 >= Z:
                            continue
                    
                        for jj in range(-1, 2):
                            
                            j2 = j + jj
                            if j2 < 0 or j2 >= Y:
                                continue
                        
                            for ii in range(-1, 2):

                                i2 = i + ii
                                if i2 < 0 or i2 >= X:
                                    continue
                            
                                offset = abs(ii) + abs(jj) + abs(kk)
                                if offset == 0 or offset > cnn_type:
                                    continue
                            
                                if state[i2][j2][k2] == FAR:

                                    min_i = i
                                    min_j = j
                                    min_k = k

                                    if phi[min_i][min_j][min_k] > 0.0:

                                        for kkk in range(-1, 2):

                                            k3 = k2 + kkk
                                            if k3 < 0 or k3 >= Z:
                                                continue

                                            for jjj in range(-1, 2):

                                                j3 = j2 + jjj
                                                if j3 < 0 or j3 >= Y:
                                                    continue

                                                for iii in range(-1, 2):

                                                    i3 = i2 + iii
                                                    if i3 < 0 or i3 >= X:
                                                        continue

                                                    offset2 = abs(iii) + abs(jjj) + abs(kkk)
                                                    if offset2 == 0 or offset2 > cnn_type:
                                                        continue

                                                    if state[i3][j3][k3] == ALIVE and phi[i3][j3][k3] < phi[min_i][min_j][min_k]:
                                                        min_i = i3
                                                        min_j = j3
                                                        min_k = k3


                                    phi[i2][j2][k2] = phi[min_i][min_j][min_k] + float(im[i2][j2][k2])
                                    state[i2][j2][k2] = TRIAL

                                    tmp_node = node.node(i2, j2, k2)
                                    tmp_node.dis = phi[i2][j2][k2]
                                    hp.insert(tmp_node)
                                    #put i2,j2,k2 into heap

    #================= Fast marching ==================

    while (hp.top() != None):  #heap is not empty

        i = hp.top().x
        j = hp.top().y
        k = hp.top().z
        #i, j, k = top of the heap

        hp.pop()
        #delete i, j, k from the heap

        state[i][j][k] = ALIVE

        for kk in range(-1, 2):

            k2 = k + kk
            if k2 < 0 or k2 >= Z:
                continue

            for jj in range(-1, 2):

                j2 = j + jj
                if j2 < 0 or j2 >= Y:
                    continue

                for ii in range(-1, 2):

                    i2 = i + ii
                    if i2 < 0 or i2 >= X:
                        continue

                    offset = abs(ii) + abs(jj) + abs(kk)
                    if offset == 0 or offset > cnn_type:
                        continue

                    if state[i2][j2][k2] != ALIVE:

                        new_dist = phi[i][j][k] + float(im[i2][j2][k2]) * math.sqrt(float(offset))

                        if state[i2][j2][k2] == FAR:

                            phi[i2][j2][k2] = new_dist

                            tmp_node = node.node(i2, j2, k2)
                            tmp_node.dis = phi[i2][j2][k2]
                            hp.insert(tmp_node)
                            #add i2, j2, k2 to heap

                        elif state[i2][j2][k2] == TRIAL:

                            if new_dist < phi[i2][j2][k2]:

                                phi[i2][j2][k2] = new_dist

                                tmp_node = node.node(i2, j2, k2)
                                tmp_node.dis = phi[i2][j2][k2]
                                hp.insert(tmp_node)
                                #add i2, j2, k2 to heap

#======================================================================================================================================================================
