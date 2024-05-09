import os
import matplotlib.pyplot as plt
from openfast_toolbox.case_generation import runner
from openfast_toolbox.io import FASTInputFile, FASTOutputFile
from scipy.optimize import minimize

YawErrorStrat = 0
WindDeltaStrat = 1
scriptDir = os.path.dirname(__file__)

def run_openFAST_yaw(YawArgument, YawStrategy):
    fastinFilename = os.path.join(scriptDir, '../openfast_yaw_NSU/r-test/glue-codes/openfast/5MW_Land_DLL_WTurb/5MW_Land_DLL_WTurb.fst')
    openFAST_EXE = os.path.join(scriptDir, '../openfast_yaw_NSU/build/bin/openfast_x64.exe')  
    out = runner.run_cmd([fastinFilename, str(YawStrategy), str(YawArgument[0])], openFAST_EXE, showOutputs=True)
    if out.returncode == 1:
        return 0
    
    fastoutFilename = os.path.join(scriptDir, '../openfast_yaw_NSU/r-test/glue-codes/openfast/5MW_Land_DLL_WTurb/5MW_Land_DLL_WTurb.outb')
    df = FASTOutputFile(fastoutFilename).toDataFrame()
    Power = sum(df['GenPwr_[kW]'])
    return Power

if __name__ == '__main__':
    res = minimize(run_openFAST_yaw, 0.1, args=0, method='Nelder-Mead')
    print(res.x, res.success, res.message)