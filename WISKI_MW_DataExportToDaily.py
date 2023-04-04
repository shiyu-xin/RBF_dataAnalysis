# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:25:19 2022

@author: sxin
"""

import pandas as pd
import os

def xlsxFiles(filePath):
    allFiles = os.listdir(filePath)    
    x = [s for s in allFiles if s.endswith('.xlsx')]
    return x


def toDaily(filePath):
    df = pd.read_excel(filePath)
    df_new = df.resample('D', on = 'Timestamp').mean()
    return df_new
 
          
    
readFilePath = 'T:\sxin\Water Quality\Production Facility\Monitoring Well Data'
writeFilePath = 'T:\sxin\Water Quality\Production Facility\Monitoring Well Data\DailyAverages'

xlsxList = xlsxFiles(readFilePath)

for fileName in xlsxList:
    csvName = fileName.split('.')[0] + '.csv'
    dailyData = toDaily(os.path.join(readFilePath,fileName))
    path = os.path.join(writeFilePath, csvName)
    #writer = pd.ExcelWriter(path, engine='xlsxwriter')
    #dailyData.to_excel(writer)
    dailyData.to_csv(path)
    




readFile = 'S:\WRP\sxin\Water Quality\Production Facility\Monitoring Well Data\TW06.xlsx'
df = pd.read_excel(readFile)
df = df.set_index('Timestamp')
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
df_new = df.Value.resample('D').mean()

df_new.to_csv('S:\WRP\sxin\Water Quality\Production Facility\TW06.csv')
    

        



    








































