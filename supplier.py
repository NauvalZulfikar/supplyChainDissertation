import pandas as pd
import numpy as np
import datetime

def supplier(size,whs):
  spl_id      = [f'spl_{i}' for i in range(1,size*5+1)] # hashed
  cust_req_id = [f'cust_req_{i%size+1}' for i in range(1,size*5+1)] # hashed

  spl                = pd.DataFrame()
  spl['spl_id']      = spl_id
  spl['cust_req_id'] = cust_req_id

  df = pd.merge(whs,spl,how='left',on=['cust_req_id'])

  spl_price_offs  = []
  spl_quan_avails = []
  spl_avail_diffs = []
  spl_fulfills    = []
  for i in range(len(df)):
      if df.whs_avail_diff[i]>=0:
          spl_price_off  = 0
          spl_quan_avail = 0
          spl_avail_diff = 0
      else:
          spl_price_off  = int(np.random.uniform(df['whs_price_off'][i]/np.abs(df['whs_avail_diff'][i])+1, size=1)*(np.abs(df['whs_avail_diff'][i])).item())
          spl_quan_avail = int(np.random.randint(5000, size=1).item())
          spl_avail_diff = spl_quan_avail+df['whs_avail_diff'][i]

      spl_price_offs.append(spl_price_off)
      spl_quan_avails.append(spl_quan_avail)
      spl_avail_diffs.append(spl_avail_diff)

  for i in range(len(df)):
      if spl_avail_diffs[i]>0:
          spl_fulfill     = 1
      else:
          spl_fulfill     = 0
      spl_fulfills.append(spl_fulfill)

  df['spl_price_off']  = spl_price_offs
  df['spl_quan_avail'] = spl_quan_avails
  df['spl_avail_diff'] = spl_avail_diffs
  df['spl_fulfill']    = spl_fulfills

  return df