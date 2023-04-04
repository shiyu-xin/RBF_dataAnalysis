# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 14:10:22 2022

@author: sxin
"""

import glob
import pandas as pd
import datetime
import os

#Establish input/output file paths and current timestamp 
importNums = pd.read_excel(r'T:\sxin\JFA\Production Facility\WISKI Caisson Upload Import Numbers.xlsx')
filepath = r'T:\sxin\JFA\Production Facility\Caisson Data\DailyAverages\*.csv'
outfolder= r'T:\sxin\JFA\Production Facility\WISKI_ready'
printtime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


#Retrieve data and save as dataFrame
files = glob.glob(filepath)

tempList = []
for file in files:
    tempList.append(pd.read_csv(file, usecols=('TagName','DateTime','Value')))
    
df = pd.concat(tempList)
df = df[df['Value']!='(null)']

df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Value'] = pd.to_numeric(df['Value'])

df = pd.merge(df, importNums, on='TagName', how='inner')

#Replace SCADA pump 9 flows with calculated pump 9 flowS
pump9filepath = r'T:\sxin\Transmission System\Production Operation Analysis\pump9Flow.csv'
pump9Flow = pd.read_csv(pump9filepath)
pump9Flow = pump9Flow.rename(columns={'mean':'Value'})
df_update = pd.concat([df, pump9Flow])
df_update = df_update[df_update['TagName']!='S05.S05_A_Pump9_Flow']
df_update['TagName'] = df_update['TagName'].fillna('S05.S05_A_Pump9_Flow')
df_update['Import Number'] = df_update['Import Number'].fillna('Caisson5_pump9')

  
#Convert data to ZRXP format from dataFrame
imptNumList = importNums['Import Number'].tolist()
for i in range(0,len(imptNumList)):
    imptNum = imptNumList[i]    
    tempdf = df_update.loc[df_update['Import Number']==imptNum]
    tempdf = tempdf[['DateTime', 'Value']]
    tempdf['DateTime'] = pd.to_datetime(tempdf['DateTime'])
    tempdf['DateTime'] = tempdf['DateTime'].dt.strftime('%Y%m%d%H%M00')
    filename = os.path.join(outfolder,printtime+'_'+imptNum+'.zrxp')
    top = '#REXCHANGE{:}|*|TZUTC-8|*|LAYOUT(timestamp,value,remark)|*|'.format(imptNum)
    with open(filename, 'w') as f:
        f.write(top)
        f.write('\n')
    
    tempdf.to_csv(filename, mode = 'a+',
                  header = None,
                  index= False, sep = ' ')
    