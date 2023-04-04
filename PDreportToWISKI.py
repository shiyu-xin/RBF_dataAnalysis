import pandas as pd
import datetime
import os

filepath = r'S:\Ops\RiverReport\Production_and_Demand_Report_PHIST01.xlsm'
sheetRemove = ['TOC','Web_Tables','WaterProductionWeb','Sheet1','SCADAConnections',
               'WData','WindsorDiversions','Climate','Web_TablesOld']
imptNumList = ['RDS_pump1','RDS_pump2','RDS_pump3','RDS_totalDiv','RDS_riverLevel']

outfolder = r'T:\sxin\JFA\Production Facility\WISKI_ready'
printtime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

data = pd.read_excel(filepath, sheet_name=None)

for sheet in sheetRemove:
    del data[sheet]

dataAll = pd.concat(data.values())
dataAll = dataAll.iloc[:,:7]
dataAll.columns = ['Date', 'Day', 'RDSp1run','RDSp2run','RDSp3run','TotalDiv','RiverLevel']
dataAll = dataAll.drop(columns='Day')
dataAll['Date'] = pd.to_datetime(dataAll['Date'], errors='coerce')
dataAll = dataAll[dataAll['Date'].notna()]


dataDict = {}
counter = 1
for element in imptNumList:
    dataDict[element] = dataAll.iloc[:,[0,counter]]
    counter +=1 
    


#Convert data to ZRXP format from dataFrame
for i in range(0,len(imptNumList)):
    imptNum = imptNumList[i]    
    tempdf = dataDict[imptNum]
    tempdf['Date'] = pd.to_datetime(tempdf['Date'])
    tempdf['Date'] = tempdf['Date'].dt.strftime('%Y%m%d%H%M00')
    tempdf.iloc[:,1] = pd.to_numeric(tempdf.iloc[:,1], errors='coerce')
    tempdf = tempdf.dropna()
    tempdf.iloc[:,1] = tempdf.iloc[:,1].apply(lambda x: round(x,2))
    tempdf = tempdf.sort_values(by='Date')
    tempdf = tempdf.drop_duplicates(subset='Date')
    filename = os.path.join(outfolder,printtime+'_'+imptNum+'.zrxp')
    top = '#REXCHANGE{:}|*|TZUTC-8|*|LAYOUT(timestamp,value,remark)|*|'.format(imptNum)
    with open(filename, 'w') as f:
        f.write(top)
        f.write('\n')
    
    tempdf.to_csv(filename, mode = 'a+',
                  header = None,
                  index= False, sep = ' ')