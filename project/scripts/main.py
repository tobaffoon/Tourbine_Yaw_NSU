import os
from openfast_toolbox.case_generation import runner
from openfast_toolbox.io import FASTInputFile, FASTOutputFile
from scipy.optimize import minimize

YawErrorStrat = 0
WindDeltaStrat = 1
scriptDir = os.path.dirname(__file__)

def run_openFAST_yaw(YawArgument, YawStrategy):
    fastinFilename = os.path.join(scriptDir, '../openfast/turbine/5MW_Land_DLL_WTurb.fst')
    openFAST_EXE = os.path.join(scriptDir, '../openfast/openfast_x64.exe')  
    out = runner.run_cmd([fastinFilename, str(YawStrategy), str(YawArgument[0])], openFAST_EXE, showOutputs=True)
    if out.returncode != 0:
        return 0
    
    fastoutFilename = os.path.join(scriptDir, '../openfast_yaw_NSU/r-test/glue-codes/openfast/5MW_Land_DLL_WTurb/5MW_Land_DLL_WTurb.outb')
    df = FASTOutputFile(fastoutFilename).toDataFrame()
    Power = sum(df['GenPwr_[kW]'])
    return Power

def neg_yaw(YawArgument, YawStrategy):
    return -run_openFAST_yaw(YawArgument, YawStrategy)

if __name__ == '__main__':
    arg0 = 0.2
    strat = YawErrorStrat
    res_list = []
    while arg0 <= 1.0:
        res = minimize(neg_yaw, arg0, args=strat, method='Nelder-Mead', bounds=[(0, 3)])
        if res.success :
            res_list.append(("s", arg0, res.x[0], -res.fun))
        else:
            res_list.append(("f", arg0, res.x[0], -res.fun))
        arg0 += 0.1
    with open("res.txt", "w") as fout:
        fout.write("Yaw Error: " + str(res_list) + "\n")