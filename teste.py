from search import astar_search
from solution import ASARProblem
import time
for k in range(1,9):
    f = open("simple"+str(k)+".txt", "r")
    w = open("out.txt", "w+")

    p= ASARProblem()
    p.load(f)
    start = time.time()
    a=astar_search(p)
    elapsed_time_fl = (time.time() - start)
    print("P" +str(k) + ":" , end=" ")
    if(a != None):
        p.save(w, a.state)
    else:
        p.save(w,None)
    