""" 
- Open and OpenFAST binary file
- Convert it to a pandas dataframe
- Plot a given output channel
"""
import os
import matplotlib.pyplot as plt
from openfast_toolbox.case_generation import runner
from openfast_toolbox.io import FASTInputFile, FASTOutputFile

YawErrorStrat = 0
WindDeltaStrat = 1

YawStrat = YawErrorStrat
YawArg = 0.1
# Get current directory so this script can be called from any location
scriptDir = os.path.dirname(__file__)

fastinFilename = os.path.join(scriptDir, '../openfast_yaw_NSU/r-test/glue-codes/openfast/5MW_Land_DLL_WTurb/5MW_Land_DLL_WTurb.fst')
yawParamsFilename = os.path.join(scriptDir, '../openfast_yaw_NSU/build/bin/yaw_control_params.dat"')
openFAST_EXE = os.path.join(scriptDir, '../openfast_yaw_NSU/build/bin/openfast_x64.exe')  
runner.run_cmd([fastinFilename, str(YawStrat), str(YawArg)], openFAST_EXE, showOutputs=True)

fastoutFilename = os.path.join(scriptDir, '../openfast_yaw_NSU/r-test/glue-codes/openfast/5MW_Land_DLL_WTurb/5MW_Land_DLL_WTurb.outb')
df = FASTOutputFile(fastoutFilename).toDataFrame()
print(df.keys())
time  = df['Time_[s]']
Power = df['GenPwr_[kW]']
plt.plot(time, Power)
plt.xlabel('Time [s]')
plt.ylabel('GenPwr [kW]')
print(sum(Power))

if __name__ == '__main__':
    plt.show()