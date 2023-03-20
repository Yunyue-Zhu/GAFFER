import numpy as np
import geatpy as ea
import os
import threading

class WfOptimize(ea.Problem):
    def __init__(self):
        name = 'WfOptimize'
        M = 1  # dimension of target func
        maxormins = [-1]  # min = 1; max = -1
        Dim = 27  # dimension of variables
        varTypes = [0] * Dim  # continuous = 0; discrete = 1
        lb = [0.13, 2.00, 2.00, 2.00, 1.03, 1.00, 1.00, 1.00, 1.00, 0.53, 1.00, 0.13, 0.00, 0.00, 0.00,
              0.00, 0.00, 0.00, 0.00, 0.00, 20.00, 50.00, 100.00, 300.00, 0.1300, 0.0150, 0.0050]  # lower bound
        ub = [0.13, 3.80, 3.80, 3.80, 3.80, 3.00, 3.00, 3.00, 3.00, 2.50, 3.00, 0.13, 0.00,
              3.0, 3.0, 5.0, 10.0, 20.0, 50.0, 50.0, 50.0, 200.0, 300.0, 300.0, 0.1300, 0.0150, 0.0050]  # upper bound
        # lb = [0.13,2.00,2.00,2.00,1.03,1.00,1.00,1.00,1.00,0.53,1.00,0.13,0.00,
        # 0.00,0.00,0.00,0.00,0.00,0.00,0.00,20.00,50.00,50.00,50.00,0.1300,0.0150,0.0050] # lower bound
        # ub = [0.13,3.80,3.80,3.80,3.80,3.00,3.00,3.00,3.00,2.50,3.00,0.13,0.00,
        # 5.0,5.0,5.0,5.0,50.0,50.0,50.0,100.0,100.0,100.0,100.0,0.1300,0.0150,0.0050] # upper bound
        lbin = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1]  # lower bound included or not
        ubin = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1]  # upper bound included or not
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):
        Vars = pop.Phen
        nPop, nVars = np.shape(Vars)
        nFits = 9
        Fits = np.zeros((nPop, nFits))

        runs = []
        for iPop in range(nPop):
            tmpVars = Vars[iPop].tolist()
            inp_file_name = "inp_" + str(iPop) + ".dat"
            np.savetxt(inp_file_name, [.0], fmt='%.2f', delimiter='\n')
            with open(inp_file_name, 'a') as f:
                np.savetxt(f, tmpVars[0:nVars - 3], fmt='%.2f', delimiter='\n')
                np.savetxt(f, [.0], fmt='%.2f', delimiter='\n')
                np.savetxt(f, tmpVars[nVars - 3:], fmt='%.4f', delimiter='\n')
            run = threading.Thread(target=runMulti, args=(iPop,))
            runs.append(run)

        for run in runs:
            run.start()
        for run in runs:
            run.join()

        for iPop in range(nPop):
            fit_file_name = "fit_" + str(iPop) + ".dat"
            Fits[iPop] = np.loadtxt(fit_file_name)
            inp_file_name = "inp_" + str(iPop) + ".dat"
            os.system("cat "+inp_file_name+" | tr '\n' '  ' >> pop_info.txt")
            os.system("cat "+fit_file_name+" >> pop_info.txt")

        os.system("rm inp_*")
        os.system("rm fit_*")
        os.system("rm block_*")
        rhor = Fits[:, [0]]
        rhomax = Fits[:, [5]]
        vmean = Fits[:, [2]]
        alphaDT = Fits[:, [4]]
        gamma_B = 3.37 * 10 ** 7
        lambda_deg = 2.17 * 10 ** 5
        eta = 0.1
        qfuel = 3.37 * 10 ** 11
        Eps = 560 * (100 / (rhomax+0.001))**1.85 * 10 ** 3
        Ens = 2 * np.pi / (eta * rhomax ** (4 / 3)+0.001) * alphaDT * lambda_deg * rhor ** 3
        phi = rhor / (rhor + 7)
        el = qfuel * 4 / 3 * np.pi * rhor ** 3 / (rhomax+0.001) ** 2 * phi / (Eps + Ens + 0.001)
        pop.ObjV = np.nan_to_num(el)
        pop.CV = np.hstack([Vars[:,[0]]+Vars[:,[1]]+Vars[:,[2]]+Vars[:,[3]]+Vars[:,[4]]+Vars[:,[5]]+Vars[:,[6]]+Vars[:,[7]]+
        Vars[:,[8]]+Vars[:,[9]]+Vars[:,[10]]+Vars[:,[11]]-25])


def runMulti(iPop):
    os.system("./multi " + str(iPop) + " 2>&1 >/dev/null")
