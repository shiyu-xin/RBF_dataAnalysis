# -*- coding: utf-8 -*-
import pandas as pd
import datetime

numYear = 20
timeDelta = numYear * 365

start_date = datetime.date.today() - datetime.timedelta(timeDelta)
start_date = start_date.strftime('%Y-%m-%d')

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
#MW93_15 = {'gwe_m': '47107010', 'gwe_t': '47109010'} #No record in WISKI
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



ListOfMWid = [TW01, TW02, TW03, TW06, TW08, TW14, TW15, TW16, TW17, TW18, MW93_14, MW93_16, 
              MW93_17, MW93_18, WC_OW_01C, MMW_B_01, MMW_B_02, GSC_WEL_1,
              GSC_WEL_2, MW_01, LBNL_G2, RDS_MW4, SB_OW_02B]
ListOfMW = ['TW01', 'TW02', 'TW03', 'TW06', 'TW08', 'TW14', 'TW15', 'TW16', 'TW17', 'TW18',
            'MW93_14', 'MW93_16', 'MW93_17', 'MW93_18', 'WC_OW_01C', 'MMW_B_01',
            'MMW_B_02','GSC_WEL_1','GSC_WEL_2','MW_01', 'LBNL_G2', 'RDS_MW4',
            'SB_OW_02B']

#ListOfMWid = [TW01, TW02]
#ListOfMW = ['TW01', 'TW02']

rd = pd.DataFrame(ListOfMW, columns=['Name'])
df = pd.DataFrame()

#df = pd.concat([df, pd.DataFrame([TW01])], ignore_index=True)


for index, well in enumerate(ListOfMWid):
    df = pd.concat([df, pd.DataFrame([well])], ignore_index=True)
    
wellRecord = rd.join(df)
wellRecord['Start Date'] = ''
wellRecord['End Date'] = ''
wellRecord['NumDays'] = ''



for index, well in enumerate(wellRecord['gwe_t']):
    tsID= well
    wellName = wellRecord['Name'][wellRecord['gwe_t']==tsID][index]
    url = f'https://www.kisters.net/sonomacountygroundwater/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=html&ts_id={tsID}&from={start_date}'
    raw_data=pd.read_html(url,skiprows = [0,1,2],header = 0)[0].dropna()
    raw_data['Timestamp'] = raw_data['Timestamp'].apply(lambda x: x[:10])
    raw_data['Timestamp'] = pd.to_datetime(raw_data.Timestamp)
    daily_data = raw_data.drop_duplicates(subset='Timestamp')
    daily_data.set_index('Timestamp', inplace=True)
    
    if index == 0:
        
        summary = daily_data.groupby(by=daily_data.index.year).count()
        summary = summary.rename(columns={'Value': wellName})
    else:    
        tempdf = daily_data.groupby(by=daily_data.index.year).count()
        tempdf = tempdf.rename(columns={'Value': wellName})
        summary = pd.merge(summary, tempdf, left_index=True, right_index=True, how='outer')
        
summary = summary.fillna(value=0, axis=1)
summary = summary.transpose()
                
    #wellRecord['Start Date'].iloc[index] = raw_data['Timestamp'].iloc[0]
    #wellRecord['End Date'].iloc[index] = raw_data['Timestamp'].iloc[len(raw_data)-1]
    #wellRecord['NumDays'].iloc[index] = len(raw_data)

    
#wellRecord['NumDaysTotal'] = (wellRecord['End Date'] - wellRecord['Start Date']).dt.days + 1
#wellRecord['Completion'] = (wellRecord['NumDays']/wellRecord['NumDaysTotal'])
    
#writer = pd.ExcelWriter(r'S:\WRP\sxin\JFA\Production Facility\Site Selection\wellSummmary.xlsx', engine='xlsxwriter')
#writer = pd.ExcelWriter(r'S:\WRP\sxin\JFA\Production Facility\Site Selection\wellStats.xlsx', engine='xlsxwriter')
#for sheet in countRecord.keys():
    #sheetName = wellRecord['Name'].loc[wellRecord['gwe_t']==sheet].iloc[0]
    #countRecord[sheet].to_excel(writer, sheet_name = sheetName)
#writer.save()

#wellRecord.to_excel(r'S:\WRP\sxin\JFA\Production Facility\Site Selection\wellRecord.xlsx')
#summary.to_excel(r'S:\WRP\sxin\JFA\Production Facility\Site Selection\GWE_SummaryByYear.xlsx')