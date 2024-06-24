import pandas as pd
import numpy as np
import datetime

def warehouse(size,ret):
  whs_id      = [f'whs_{i}' for i in range(1,size*5+1)] # hashed
  cust_req_id = [f'cust_req_{i%size+1}' for i in range(1,size*5+1)] # hashed

  whs                = pd.DataFrame()
  whs['whs_id']      = whs_id
  whs['cust_req_id'] = cust_req_id

  df = pd.merge(ret,whs,how='left',on=['cust_req_id'])

  whs_price_offs  = []
  whs_price_ords  = []
  whs_quan_avails = []
  whs_avail_diffs = []
  whs_fulfills    = []
  for i in range(0,len(df)):
      if df['ret_avail_diff'][i]>=0:
          whs_price_off  = 0
          whs_quan_avail = 0
          whs_price_ord  = 0
          whs_avail_diff = 0
      else:
          whs_price_off  = int(np.random.uniform(0, df['ret_price_off'][i]/np.abs(df['cust_quan_req'][i])+1, size=1)*(np.abs(df['ret_avail_diff'][i])).item())
          whs_quan_avail = int(np.random.randint(0, 5000, size=1).item())
          whs_avail_diff = whs_quan_avail+df['ret_avail_diff'][i]
          whs_price_ord  = int(np.random.uniform(0, (whs_price_off/np.abs(df['cust_quan_req'][i]))+1, size=1)*(np.abs(whs_avail_diff)).item())

      whs_price_offs.append(whs_price_off)
      whs_quan_avails.append(whs_quan_avail)
      whs_price_ords.append(whs_price_ord)
      whs_avail_diffs.append(whs_avail_diff)

  for i in range(len(df)):
      if whs_avail_diffs[i]>0:
          whs_fulfill = 1
      else:
          whs_fulfill = 0
      whs_fulfills.append(whs_fulfill)

  df['whs_price_off']  = whs_price_offs
  df['whs_quan_avail'] = whs_quan_avails
  df['whs_price_ord']  = whs_price_ords
  df['whs_avail_diff'] = whs_avail_diffs
  df['whs_fulfill']    = whs_fulfills

  return df