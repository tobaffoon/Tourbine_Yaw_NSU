import os
from openfast_toolbox.case_generation import runner
from openfast_toolbox.io import FASTInputFile, FASTOutputFile
from openfast_toolbox.io.fast_output_file import writeDataFrame
from scipy.optimize import minimize
from numpy import cos, deg2rad

YawErrorStrat = 0
WindDeltaStrat = 1
scriptDir = os.path.dirname(__file__)
ro = 1.225

def calc_ideal_power():
    fastoutFilename = os.path.join(scriptDir, '../openfast/turbine/5MW_Land_DLL_WTurb.outb')
    output = FASTOutputFile(fastoutFilename).toDataFrame()
    A = output['RtArea_[m^2]']
    wspeed = output['Wind1VelX_[m/s]']
    a_ind = 1/3
    yaw_error = abs(output['WindHubAng_[deg]'] - output['YawPzp_[deg]'])
    eta = 0.768
    p_p = 2
    coef_power = 4 * a_ind * ((1 - a_ind) ** 2) * eta * (cos(deg2rad(yaw_error)) ** p_p)
    output['GenPwr_[kW]'] = 1/2 * ro * A * coef_power * (wspeed ** 3)
    output['Axial_Ind'] = a_ind
    output['YawErr_[deg]'] = yaw_error
    output['CoefPwr'] = coef_power

    fastoutNewFilename = os.path.join(scriptDir, '../openfast/turbine/custom_calc.outb')
    writeDataFrame(output, fastoutNewFilename, binary=True)

def run_openFAST_yaw(YawArgument, YawStrategy):
    fastinFilename = os.path.join(scriptDir, '../openfast/turbine/5MW_Land_DLL_WTurb.fst')
    openFAST_EXE = os.path.join(scriptDir, '../openfast/openfast_x64.exe')  
    out = runner.run_cmd([fastinFilename, str(YawStrategy), str(YawArgument[0])], openFAST_EXE, showOutputs=True)
    if out.returncode != 0:
        return 0
    
    calc_ideal_power()
    fastoutFilename = os.path.join(scriptDir, '../openfast/turbine/custom_calc.outb')
    df = FASTOutputFile(fastoutFilename).toDataFrame()
    Power = sum(df['GenPwr_[kW]'])
    return Power

def neg_yaw(YawArgument, YawStrategy):
    return -run_openFAST_yaw(YawArgument, YawStrategy)

if __name__ == '__main__':
    print(run_openFAST_yaw([1.7], 0))
    # arg0 = 0.2
    # strat = YawErrorStrat
    # res_list = []
    # while arg0 <= 1.7:
    #     res = minimize(neg_yaw, arg0, args=strat, method='Nelder-Mead', bounds=[(0, 3)])
    #     if res.success :
    #         res_list.append(("s", arg0, res.x[0], -res.fun))
    #     else:
    #         res_list.append(("f", arg0, res.x[0], -res.fun))
    #     arg0 += 0.5
    # with open("res_new.txt", "w") as fout:
    #     fout.write("Yaw Error: " + str(res_list) + "\n")