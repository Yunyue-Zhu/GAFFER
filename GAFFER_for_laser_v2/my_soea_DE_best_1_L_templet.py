import time
import numpy as np
import geatpy as ea

class my_soea_DE_best_1_L_templet(ea.soea_DE_best_1_L_templet):

    best = np.zeros([1, 28])

    def stat(self, pop):


        """
        描述:
            该函数用于分析、记录和打印当代种群的信息。
            该函数会在terminated()函数里被调用。

        输入参数:
            pop : class <Population> - 种群对象。

        输出参数:
            无输出参数。

        """


        # 进行进化记录
        feasible = np.where(np.all(pop.CV <= 0, 1))[0] if pop.CV is not None else np.arange(pop.sizes)  # 找到满足约束条件的个体的下标
        if len(feasible) > 0:
            feasiblePop = pop[feasible]
            bestIndi = feasiblePop[np.argmax(feasiblePop.FitnV)]  # 获取最优个体
            if self.BestIndi.sizes == 0:
                self.BestIndi = bestIndi  # 初始化global best individual
            else:
                delta = (self.BestIndi.ObjV - bestIndi.ObjV) * self.problem.maxormins if \
                    self.problem.maxormins is not None else self.BestIndi.ObjV - bestIndi.ObjV
                # 更新“进化停滞”计数器
                if np.abs(delta) < self.trappedValue:
                    self.trappedCount += 1
                else:
                    self.trappedCount = 0
                # 更新global best individual
                if delta > 0:
                    self.BestIndi = bestIndi
            # 更新trace
            self.trace['f_best'].append(bestIndi.ObjV[0][0])
            self.trace['f_avg'].append(np.mean(feasiblePop.ObjV))
            temp = np.append(bestIndi.Phen, bestIndi.ObjV, axis=1)
            self.best = np.append(self.best, temp, axis=0)
            if self.logTras != 0 and self.currentGen % self.logTras == 0:
                self.logging(feasiblePop)  # 记录日志
                if self.verbose:
                    self.display()  # 打印日志
            self.draw(self.BestIndi)  # 展示输出
