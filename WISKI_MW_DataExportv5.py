# -*- coding: utf-8 -*-

import pandas as pd
import datetime

numYear = 20
timeDelta = numYear * 365

start_date = datetime.date.today() - datetime.timedelta(timeDelta)
start_date = start_date.strftime('%Y-%m-%d')

wiskiRecord = pd.read_excel(r'T:\sxin\JFA\Production Facility\Site Selection\WISKIwellRecord.xlsx', index_col=0, converters={'gwe_t':str,'gwe_m':str,'temp':str})

for index, well in enumerate(wiskiRecord['gwe_t']):
    tsID= well
    if pd.isna(tsID):
        pass
    else:
        wellName = wiskiRecord['Name'][wiskiRecord['gwe_t']==tsID][index]
        url = f'https://www.kisters.net/sonomacountygroundwater/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=html&ts_id={tsID}&from={start_date}'
        raw_data=pd.read_html(url,skiprows = [0,1,2],header = 0)[0].dropna()
        raw_data['Timestamp'] = pd.to_datetime(raw_data.Timestamp)
        raw_data['Timestamp'] = raw_data['Timestamp'].dt.tz_localize(None)
        
        #raw_data.to_csv(f'T:\sxin\JFA\Production Facility\{wellName}_raw.csv', index=False)
        dailyAverages = raw_data.resample('D', on ='Timestamp')['Value'].mean()
        dailyAverages.to_csv(f'T:\sxin\JFA\Production Facility\{wellName}_dailyAverages.csv')
        
        #tsID=ListOfMWid[i].get('gwe_t')
        #url = r'https://www.kisters.net/sonomacountygroundwater/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=html&ts_id='+tsID+'&from='+start_date
        #data=pd.read_html(url,skiprows = [0,1,2],header = 0)[0].dropna()
        #data['Timestamp'] = pd.to_datetime(data.Timestamp)
        #data['hour'] = data['Timestamp'].dt.hour
        #dataExcel = data[['Timestamp','Value']].copy()
        #dataExcel['Timestamp'] = dataExcel['Timestamp'].dt.tz_localize(None)
        #dataExcel.set_index('Timestamp', inplace=True)  
        #data = data[data['hour']==0]
        #data=data.reset_index(drop=True)
        #data=data[['Timestamp','Value']]
