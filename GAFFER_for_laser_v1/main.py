import geatpy as ea
from WfOptimize import WfOptimize

problem = WfOptimize()
Encoding ='RI'# coding type
NIND = 80# population size
Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges,problem.borders)# field descriptor
population = ea.Population(Encoding, Field, NIND)

with open('pop_info.txt','w') as f:
    f.write('population size = ' + str(NIND) + '\n')

myAlgorithm = ea.soea_DE_best_1_L_templet(problem, population)# instantiate a template object
myAlgorithm.MAXGEN = 20# maximum number of generation
myAlgorithm.mutOper.F = 0.5# parameter F in DE
myAlgorithm.recOper.XOVR = 0.7# crossover probability
myAlgorithm.logTras = 1# log interval, 0 = no log
myAlgorithm.verbose = True# print log
myAlgorithm.drawing = 1# 0 none, 1 fitness trace, 3 best parameter trace
[BestIndi, population] = myAlgorithm.run()
BestIndi.save()

print('Total number of individuals: %s'% myAlgorithm.evalsNum)
print('Run time: %s s'% myAlgorithm.passTime)
if BestIndi.sizes != 0:
    print('Best fitness: %s'% BestIndi.ObjV[0][0])
    print('Best parameter set:')
    for i in range(BestIndi.Phen.shape[1]):
        print(BestIndi.Phen[0, i])
else:
    print('No feasible solution :(')
