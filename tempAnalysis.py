# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
import glob



filepath = r'T:\sxin\JFA\Production Facility\Temperature\daily\*.csv'
files = glob.glob(filepath)
tempList = []
for file in files:
    wellName = file[50:]
    wellName = wellName.split('_daily')[0]    
    if wellName == 'USGS_hacienda':
        tempList.append(pd.read_csv(file, names=['Date', wellName+'_max', wellName+'_min', wellName+'_mean'], header=None))
    else:
        tempList.append(pd.read_csv(file, names=['Date', wellName], header=None))
        
for index, df in enumerate(tempList):
    df = df[1:]
    df = df.set_index('Date')
    if index == 0:    
        dfAll = df
    else:
        dfAll = pd.merge(dfAll, df, left_index=True, right_index=True, how='outer')
#allPrevious = pd.concat(tempList)