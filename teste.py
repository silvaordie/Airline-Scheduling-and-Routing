from search import astar_search
from solution import ASARProblem

f = open("simple6.txt", "r")
w = open("out.txt", "w+")
p= ASARProblem()
p.load(f)

a=astar_search(p)
p.save(w, a.state)