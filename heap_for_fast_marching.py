from skimage import io
import sys
import math
import numpy
import node


class MyHeap:

    def __init__(self, X, Y, Z):

        self.a = []
        self.size = 0
        self.a.append(None)
        self.mark = numpy.zeros((X, Y, Z), dtype = numpy.int)

    #========================================================================================================

    def insert(self, obj):

        now = 0

        if self.mark[obj.x][obj.y][obj.z] != 0:
            
            now = self.mark[obj.x][obj.y][obj.z]
            
            self.a[now].x = obj.x
            self.a[now].y = obj.y
            self.a[now].z = obj.z

            self.a[now].parent = obj.parent

            self.a[now].dis = obj.dis         
        else:
            self.size += 1
            self.a.append(obj)
            now = self.size

        while now != 1:

            parent = int(now / 2)

            if self.a[now].dis >= self.a[parent].dis:           
                break;

            tmp = self.a[now]
            self.a[now] = self.a[parent]
            self.a[parent] = tmp

            now = parent

        while now <= self.size:

            left = now * 2
            right = now * 2 + 1

            if left > self.size and right > self.size:
                break

            elif left <= self.size and right > self.size:

                if self.a[now].dis <= self.a[left].dis:
                    break

                tmp = self.a[now]
                self.a[now] = self.a[left]
                self.a[left] = tmp
                now = left

            elif left > self.size and right <= self.size:

                if self.a[now].dis <= self.a[right].dis:
                    break

                tmp = self.a[now]
                self.a[now] = self.a[right]
                self.a[right] = tmp
                now = right

            else:

                if self.a[now].dis <= self.a[left].dis and self.a[now].dis <= self.a[right].dis:
                    break

                if self.a[now].dis > self.a[left].dis:

                    tmp = self.a[now]
                    self.a[now] = self.a[left]
                    self.a[left] = tmp
                    now = left

                else:

                    tmp = self.a[now]
                    self.a[now] = self.a[right]
                    self.a[right] = tmp
                    now = right

        self.mark[obj.x][obj.y][obj.z] = now

    #========================================================================================================

    def top(self):

        if self.size == 0:
            return None
        else:
            return self.a[1]

    #========================================================================================================

    def pop(self):

        self.a[1] = self.a[self.size]
        self.size -= 1

        now = 1

        while now <= self.size:

            left = now * 2
            right = now * 2 + 1

            if left > self.size and right > self.size:
                break

            elif left <= self.size and right > self.size:

                if self.a[now].dis <= self.a[left].dis:
                    break

                tmp = self.a[now]
                self.a[now] = self.a[left]
                self.a[left] = tmp
                now = left

            elif left > self.size and right <= self.size:

                if self.a[now].dis <= self.a[right].dis:
                    break

                tmp = self.a[now]
                self.a[now] = self.a[right]
                self.a[right] = tmp
                now = right

            else:

                if self.a[now].dis <= self.a[left].dis and self.a[now].dis <= self.a[right].dis:
                    break

                if self.a[now].dis > self.a[left].dis:

                    tmp = self.a[now]
                    self.a[now] = self.a[left]
                    self.a[left] = tmp
                    now = left

                else:

                    tmp = self.a[now]
                    self.a[now] = self.a[right]
                    self.a[right] = tmp
                    now = right
