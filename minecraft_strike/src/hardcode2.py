import minecraft_strike.src.variable as var_
import random
class structures:
        def __init__(self,a=0):
            if a==0:
                self.arr =[]
                self.arr1 = []
            else:
                self.arr = [3, 1, 3, 2, 3, 3, 1, 3, 2, 1, 1, 2, 0, 1, 3, 2, 1, 1, 0, 1, 2, 3, 3, 2, 0, 1, 2, 1]
                self.arr1 = [0, 1, 3, 0, 1, 0, 2, 1, 2, 1, 2, 2, 2, 2, 3, 2, 0, 2, 0, 0, 3, 1, 1, 3, 2, 2, 3, 1]
            self.poi = 0

        def cloud(self,x,y,h,l,w):
            arr =[]
            for i in range(-l,l):
                for j in range(-w,w):
                    arr.append((x+i, y+j, h))
            return arr
        #arr_ = None for contoller of the map(generate map)
        def building(self,self_,x,y,z,h,w,l,n=2,arr_= 1):
            #walls
            if arr_ ==None:
                t=random.randint(0,3)
                t1=random.randint(0,3)
            else:
                t=self.arr[self.poi]
                t1=self.arr[self.poi]
                self.poi+=1
            wall = [var_.WALL1,var_.WALL2,var_.WALL3,var_.WALL4]
            floor = [var_.FLOOR1,var_.FLOOR2,var_.FLOOR3,var_.FLOOR4]
            self.arr.append(t)
            self.arr1.append(t1)
            for k in range(y,y+h):
                f=False
                for i in range(n):
                    if y+6*i<k<y+4+6*i:
                        f=True
                        break

                for i in range(-l-1,l+2):
                    if not (((l+1-2>i>l+1-6) or (-l-1+2<i<-l-1+6)) and f):
                        self_.add_block((x+i, k, z+w),wall[t],immediate=False)
                        self_.add_block((x+i, k, z-w),wall[t],immediate=False)
                for j in range(-w,w+1):
                    if not (((w+1-2>j>w+1-6) or (-w-1+2<j<-w-1+6)) and f):
                        self_.add_block((x+l,k ,z+j),wall[t],immediate=False)
                        self_.add_block((x-l, k,z+j),wall[t],immediate=False)
            #roof
            for i in range(-l-1,l+2):
                for j in range(-w-1,w+2):
                    self_.add_block((i+x,y+h,j+z),floor[t1],immediate=False)
            for i in range(-l-1,l+2):
                for j in range(-w-1,w+2):
                    self_.add_block((i+x,y,j+z),floor[t1],immediate=False)
            #middle layer
            for m in range(1,n):
                for i in range(-l+1,l):
                    for j in range(-w+1,w):
                        if not (i>l-4 and j>w-4):
                            self_.add_block((i+x,m*h/(n)-1,j+z),floor[t1],immediate=False)

            if n==1:
                for k in range(y+h,y+h+5):
                    for i in range(-5,6):
                            self_.add_block((x+i, k, z+5),wall[abs(t-1)],immediate=False)
                            self_.add_block((x+i, k, z-5),wall[abs(t-1)],immediate=False)
                    for j in range(-5,6):
                            self_.add_block((x+5, k ,z+j),wall[abs(t-1)],immediate=False)
                            self_.add_block((x-5, k ,z+j),wall[abs(t-1)],immediate=False)
                for i in range(-5,6):
                    for j in range(-5,6):
                        self_.add_block((x+i, y+h+5 ,z+j),floor[abs(t-1)],immediate=False)

        def tower(self,self_,x,y,z,h,w,l,extra,n=2):
                # x,y,z,h,w,l = int(x),int(y),int(z),int(h),int(w),int(l)
                t=7
                for k in range(y,y+h):
                    for i in range(-l,l+1):
                            self_.add_block((x+i, k, z+w),var_.TOWER,immediate=False)
                            self_.add_block((x+i, k, z-w),var_.TOWER,immediate=False)
                    for j in range(-w,w+1):
                            self_.add_block((x+l, k ,z+j),var_.TOWER,immediate=False)
                            self_.add_block((x-l, k ,z+j),var_.TOWER,immediate=False)
                for k in range(y,int(y+h/2)):
                    for i in range(-l-extra,l+1+extra):
                            self_.add_block((x+i, k, z+w),var_.TOWER,immediate=False)
                            self_.add_block((x+i, k, z-w),var_.TOWER,immediate=False)
                    for j in range(-w-extra,w+1+extra):
                            self_.add_block((x+l, k ,z+j),var_.TOWER,immediate=False)
                            self_.add_block((x-l, k ,z+j),var_.TOWER,immediate=False)
                for i in range(-l-1-extra,l+2+extra):
                    for j in range(-w-1-extra,w+2+extra):
                        if not (-l<i<l and -w<j<w):
                            self_.add_block((x+i, y+h/2 ,z+j),var_.TOWER,immediate=False)
                for i in range(-l-1,l+2):
                    for j in range(-w-1,w+2):
                        self_.add_block((x+i, y+h ,z+j),var_.TOWER,immediate=False)
                for f in range(10):
                    self_.add_block((x, y+h+f ,z),var_.TOWER2,immediate=False)
                    self_.add_block((x+1, y+h+f ,z),var_.TOWER2,immediate=False)
                    self_.add_block((x+1, y+h+f ,z+1),var_.TOWER2,immediate=False)
                    self_.add_block((x, y+h+f ,z+1),var_.TOWER2,immediate=False)


    #return arr
#tmp = [-73,-59,-38,38,59,73]

#print "arra =",
#print(building(0,-1,0,18,6,6,3))
