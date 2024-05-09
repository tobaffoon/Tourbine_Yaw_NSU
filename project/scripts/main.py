""" 
- Open and OpenFAST binary file
- Convert it to a pandas dataframe
- Plot a given output channel
"""
import os
import matplotlib.pyplot as plt
from openfast_toolbox.io import FASTOutputFile

# Get current directory so this script can be called from any location
scriptDir = os.path.dirname(__file__)

fastoutFilename = os.path.join(scriptDir, '../openfast_yaw_NSU/reg_tests/r-test/glue-codes/openfast/5MW_Land_DLL_WTurb/delta-0_3-real1.outb')
df = FASTOutputFile(fastoutFilename).toDataFrame()
print(df.keys())
time  = df['Time_[s]']
Omega = df['GenPwr_[kW]']
plt.plot(time, Omega)
plt.xlabel('Time [s]')
plt.ylabel('GenPwr [kW]')

if __name__ == '__main__':
    plt.show()