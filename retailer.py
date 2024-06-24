import pandas as pd
import numpy as np
import datetime

def retailer(size,cust):
  ret_id      = [f'ret_{i}' for i in range(1,size*5+1)] # hashed
  cust_req_id = [f'cust_req_{i%size+1}' for i in range(1,size*5+1)] # hashed

  ret                = pd.DataFrame()
  ret['ret_id']      = ret_id
  ret['cust_req_id'] = cust_req_id

  df = pd.merge(cust,ret,how='left',on=['cust_req_id'])

  ret_price_off  = [i for i in np.random.uniform(df['cust_price_ord'], 3, size=size*5)]
  ret_quan_avail = [i for i in np.random.randint(0,5000,size=size*5)]
  ret_avail_diff = [j-i for i,j in zip(df['cust_quan_req'],ret_quan_avail)]

  ret_price_ord  = []
  ret_fulfills   = []
  for i in range(len(ret_id)):
      if ret_avail_diff[i]>=0:
          ret_pri_ord = 0
          ret_fulfill = 1
      else:
          ret_pri_ord = int(np.random.uniform(0, (ret_price_off[i]/np.abs(df['cust_quan_req'][i]))+1, size=1)*(np.abs(ret_avail_diff[i])).item())
          ret_fulfill = 0
      ret_price_ord.append(ret_pri_ord)
      ret_fulfills.append(ret_fulfill)

  df['ret_price_off']  = ret_price_off
  df['ret_quan_avail'] = ret_quan_avail
  df['ret_price_ord']  = ret_price_ord
  df['ret_avail_diff'] = ret_avail_diff
  df['ret_fulfill']    = ret_fulfills

  return df