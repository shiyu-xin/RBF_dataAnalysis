# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:59:19 2023

@author: sxin
"""

import pandas as pd
import datetime
from matplotlib import pyplot as plt


timeDelta = 7000

start_date = datetime.date.today() - datetime.timedelta(timeDelta)
start_date = start_date.strftime('%Y-%m-%d')


#IDs used to pull data from WISKI


TW01 = {'gwe_m': '47119010', 'gwe_t': '47121010'}
TW02 = {'gwe_m': '47095010', 'gwe_t': '47097010'}
TW03 = {'gwe_m': '47122010', 'gwe_t': '47124010'}
TW06 = {'gwe_m': '47131010', 'gwe_t': '47133010'}
TW08 = {'gwe_m': '47137010', 'gwe_t': '47139010'}
TW14 = {'gwe_m': '47155010', 'gwe_t': '47157010'}
TW15 = {'gwe_m': '47158010', 'gwe_t': '47160010'}
TW16 = {'gwe_m': '47267010', 'gwe_t': '47269010'}
TW17 = {'gwe_m': '47264010', 'gwe_t': '47266010'}
TW18 = {'gwe_m': '47285010', 'gwe_t': '47287010'}
MW93_14 = {'gwe_m': '32996010', 'gwe_t': '32998010', 'temp': '33002010'}
MW93_16 = {'gwe_m': '33003010', 'gwe_t': '33005010', 'temp': '33009010'}
MW93_17 = {'gwe_m': '33010010', 'gwe_t': '33012010', 'temp': '33016010'}
MW93_18 = {'gwe_m': '33017010', 'gwe_t': '33019010', 'temp': '33023010'}
WC_OW_01C = {'gwe_m': '47116010', 'gwe_t': '47118010'}

MMW_B_01 = {'gwe_m': '47306010', 'gwe_t': '47308010'}
MMW_B_02 = {'gwe_m': '47309010', 'gwe_t': '47311010'}
GSC_WEL_1 = {'gwe_m': '47330010', 'gwe_t': '47332010'}
GSC_WEL_2 = {'gwe_m': '47333010', 'gwe_t': '47335010'}
MW_01 = {'gwe_m': '47288010', 'gwe_t': '47290010'}
#PZ_97_2 = {'gwe_m': '', 'gwe_t': ''}
#PZ_97_3 = {'gwe_m': '', 'gwe_t': ''}
LBNL_G2 = {'gwe_m': '47273010', 'gwe_t': '47275010'}
RDS_MW4 = {'gwe_m': '47300010', 'gwe_t': '47302010'}
SB_OW_02B = {'gwe_m': '33114010', 'gwe_t': '33116010', 'temp': '33120010'}



ListOfMWid = [TW01, TW02, TW03, TW08, TW14, TW15, TW16, TW17, MW93_14, MW93_16, 
              MW93_17, MW93_18, WC_OW_01C, MMW_B_01, MMW_B_02, GSC_WEL_1,
              GSC_WEL_2, MW_01, LBNL_G2, RDS_MW4, SB_OW_02B]
ListOfMW = ['TW01', 'TW02', 'TW03', 'TW08', 'TW14', 'TW15', 'TW16', 'TW17', 
            'MW93_14', 'MW93_16', 'MW93_17', 'MW93_18', 'WC_OW_01C', 'MMW_B_01',
            'MMW_B_02','GSC_WEL_1','GSC_WEL_2','MW_01', 'LBNL_G2', 'RDS_MW4',
            'SB_OW_02B']

ListOfMWid = [TW06]
ListOfMW = ['TW06']


Wohler = [MW93_16, MW93_17, MW93_18, MW93_14, TW16, WC_OW_01C, TW18, TW17, TW02,
          TW06, TW08, TW14, TW01, TW03, TW15]

WohlerNames = ['MW93_16', 'MW93_17', 'MW93_18', 'MW93_14', 'TW16', 'WC_OW_01C', 
              'TW18', 'TW17', 'TW02', 'TW06', 'TW08', 'TW14', 'TW01', 'TW03', 'TW15']



def plotter(ax1, x1, x2, y1, y2, a, b):
    out = ax1.plot(x1, y1, ',', markersize = 6, label = 'GWL-transducer (ft)')
    ax1.set_ylim(a,b)
    ax2 = ax1.twinx()
    out = ax2.plot(x2, y2, 'r.', markersize = 2.5, label = 'GWL-manual (ft)')
    ax2.set_ylim(a,b)
    ax1.set_ylabel('GWE-transducer (ft)', fontsize = 8)
    ax2.set_ylabel('GWE-manual (ft)', fontsize=8) 
    return out



for i, well in enumerate(Wohler):
    tsID=Wohler[i].get('gwe_t')
    wellName = WohlerNames[i]
    url = f'https://www.kisters.net/sonomacountygroundwater/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=html&ts_id={tsID}&from={start_date}'
    raw_data=pd.read_html(url,skiprows = [0,1,2],header = 0)[0].dropna()
    raw_data['Timestamp'] = raw_data['Timestamp'].apply(lambda x: x[:10])
    raw_data['Timestamp'] = pd.to_datetime(raw_data.Timestamp)
    raw_data.to_csv(f'T:\sxin\JFA\Production Facility\GWE\{wellName}_raw.csv', index=False)
    
    dailyAverages = raw_data.resample('D', on ='Timestamp')['Value'].mean()
    dailyAverages.to_csv(f'T:\sxin\JFA\Production Facility\GWE\dailyAvg\{wellName}_dailyAverages.csv')
    




































