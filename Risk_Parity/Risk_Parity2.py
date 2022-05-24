import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import linalg
from scipy.optimize import minimize
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')


json_obj = {"000300.SH": [5613.758, 5672.154, 5699.147, 5731.757, 5696.45, 5505.717, 5365.624, 5414.468, 5145.734, 4753.868,4975.111, 5027.213, 5077.429, 4731.883, 4762.083, 4710.652, 4620.401, 4571.945, 4950.124, 4921.829,4816.084, 4880.252, 4813.311, 4910.992, 5020.753, 4908.717, 4876.03, 4702.241, 4519.783, 4515.533],
"399905.SZ": [5356.482, 5382.326, 5376.797, 5445.102, 5487.088, 5412.911, 5270.956, 5317.448, 5097.226,4661.826,4911.761, 5080.926, 5096.69, 4740.501, 4839.4, 4851.178, 4663.415, 4456.396, 4820.387, 4838.918,4813.581, 4910.358, 4886.016, 5043.144, 5133.361, 5089.439, 5153.601, 5029.198, 4869.654, 4868.814],
"HSCEI.HI": [16139.46, 16027.69, 15833.75, 15480.1, 14999.9, 14016.12, 14481.41, 14561.32, 13531.45, 11911.91,13279.53, 12933.2, 14015.75, 13319.49, 13379.18, 12755.41, 12485.07, 13284.74, 14120.84, 14040.68,12949.38, 13550.99, 13843.52, 13630.25, 13972.94, 13552.82, 13561.88, 13336.89, 13202.98, 13326.84],
"NDX.GI": [1949.2, 1953.64, 1912.81, 1949.15, 1894.09, 1872.29, 1842.1, 1844.09, 1844.09, 1795.61, 1789.53,1826.92, 1789.17, 1805.08, 1807.67, 1808.51, 1841.42, 1855.27, 1828.8, 1773.49, 1823, 1787.59, 1780.38,1780.38, 1764.81, 1787.45, 1766.3, 1773.44, 1785.46, 1791.31]}

dict1 = {i: tuple(v) for i, v in json_obj.items()}
data_df = pd.DataFrame.from_dict(dict1)
data_df.head()


def calculate_cov_matrix(df):
    """计算协方差矩阵"""
    returns_df = (df-df.shift(1))/df.shift(1)         # 简单收益率
    returns_df.dropna(axis='index', inplace=True)     # 删除空数据,交易日填值
    one_cov_matrix = returns_df.cov() * df.shape[0]   # 计算协方差矩阵，
    return np.matrix(one_cov_matrix)


#风险预算模型

# 标准风险平价下的风险贡献
def calculate_risk_contribution(weight, one_cov_matrix):
    weight = np.matrix(weight) 
    sigma = np.sqrt(weight * one_cov_matrix * np.matrix(weight).T)      # 组合风险波动率
    MRC = one_cov_matrix * weight.T / sigma      # 边际风险贡献(MRC)
    RC = np.multiply(MRC, weight.T)              # 风险贡献(RC)
    return RC


# 计算组合风险
def risk_budget_objective(weight, parameters):
    
    one_cov_matrix = parameters[0]     # 协方差矩阵
    
    RC_target_ratio = parameters[1]    # 组合资产的风险贡献率
    sigma_portfolio = np.sqrt(weight * one_cov_matrix * np.matrix(weight).T)     # 组合风险波动率
    RC_target = np.asmatrix(np.multiply(sigma_portfolio, RC_target_ratio))       # 目标风险贡献
    
    RC_real = calculate_risk_contribution(weight, one_cov_matrix)           # 每次迭代以后最新的真实风险贡献，随迭代而改变
    
    sum_squared_error = sum(np.square(RC_real - RC_target.T))[0,0] 
    return sum_squared_error


# 根据资产预期目标风险贡献度来计算各资产的权重
def calculate_portfolio_weight(one_cov_matrix, risk_budget_objective):
    '''
    约束条件的类型只有'eq'和'ineq'两种
    eq表示约束方程的返回结果为0
    ineq表示约束方程的返回结果为非负数
    '''
    num = data_df.shape[1]
    weight = np.array([1.0 / num for _ in range(num)])        # 初始资产权重,默认初始权重相同
    bounds = tuple((0, 1) for _ in range(num))                # 可选变量的界限，取值范围(0,1)
    cons = ({'type': 'eq', 'fun': lambda x: sum(x) - 1},)     # 约束条件，权重和为1，eq表示约束方程的返回结果为0
    RC_set_ratio = np.array([1.0 / num for _ in range(num)])  # 风险贡献度，风险平价下每个资产的目标风险贡献度相等
    
    optv = minimize(risk_budget_objective,                    # 目标函数
                        weight,                               # 权重初始迭代点
                        args=[one_cov_matrix, RC_set_ratio],  # 目标函数参数
                        method='SLSQP',                       # 求解方法，SLSQP：约束最小化函数中的一种
                        bounds=bounds,                        
                        constraints=cons,
                        options={'xtol':1e-2,'disp':True})    # 容忍精度，是否打印
    
    return optv.x


one_cov_matrix = calculate_cov_matrix(data_df)

print(calculate_portfolio_weight(one_cov_matrix,risk_budget_objective))

