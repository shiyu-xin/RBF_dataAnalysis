# -*- coding: utf-8 -*-

import pandas as pd

#yyyy-mm-dd
beginDate = '2008-01-01'
endDate = '2022-02-01'

siteNo = '11467000'


#15 min
url = f'https://waterdata.usgs.gov/nwis/dv?cb_00010=on&format=rdb&site_no={siteNo}&legacy=&referred_module=sw&period=&begin_date={beginDate}&end_date={endDate}'


df = pd.read_csv(url, comment='#', sep='\t')
df = df[1:]
df = df[['datetime','11513_00010_00001','11514_00010_00002','234389_00010_00003']]
df.columns = ['datetime','max','min','mean']
df = df.set_index('datetime')

#df.to_csv(r'T:\sxin\JFA\Production Facility\Temperature\USGS_hacienda_daily.csv')

url_15min=r'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00010=on&format=rdb&site_no=11467000&legacy=&referred_module=sw&period=&begin_date=2017-02-01&end_date=2020-01-01'

df_15min = pd.read_csv(url_15min, comment='#', header = None, sep='\t')
df_15min = df_15min[2:]
df_15min = df_15min.iloc[:,[2,4]]
df_15min.columns = ['datetime','temp (c)']



df_hourly = df_15min[df_15min['datetime'].apply(lambda x:x[-2:])=='00']

df_15min = df_15min.set_index('datetime')

#df_15min.to_csv(r'T:\sxin\JFA\Production Facility\Temperature\USGS_hacienda_15min.csv')
df_hourly.to_csv(r'T:\sxin\JFA\Production Facility\Temperature\USGS_hacienda_hourly.csv')

