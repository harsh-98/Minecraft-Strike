import random 
import variable as var_
n = 160  # 1/2 width and height of world
s = 1  # step size
y = 0  # initial y height
arr_2=[]
arr_1=[]
arr_w = []
arr_h = []
arr_ht = []
arr_h2 = []
arr_h2t = []

o = n - 10
for _ in xrange(30):
    a = random.randint(-o, o)  # x position of the hill
    b = random.randint(-o, o)  # z position of the hill
    y =  20  # base of the hill
    t = random.choice([var_.RSTONE,var_.ALGAE,var_.SNOW, var_.MARBLE])
    h = random.randint(4, 12)  # height of the hill
    s = random.randint(4, 15)
    t = random.randint(-1,1)
    for z in xrange(a -h , a + h):
        for x in xrange(b - s, b + s + 1):
            arr_h.append((x, y, z))
            arr_ht.append(t)
# generate the hills randomly

for _ in xrange(240):
    a = random.randint(-o, o)  # x position of the hill
    b = random.randint(-o, o)  # z position of the hill
    c = -1  # base of the hill
    h = random.randint(1, 6)  # height of the hill
    s = random.randint(4, 8)  # 2 * s is the side length of the hill
    d = 1  # how quickly to taper off the hills
    t = random.randint(-1,1)
    for y in xrange(c, c + h):
        for x in xrange(a - s, a + s + 1):
            for z in xrange(b - s, b + s + 1):
                if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                    continue
                if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                    continue
                arr_h2.append((x, y, z))
                arr_h2t.append(t)
        s -= d
print "arr_h=",
print(arr_h)
print "arr_ht=",
print(arr_ht)
print "arr_h2=",
print(arr_h2)
print "arr_h2t=",
print(arr_h2t)

