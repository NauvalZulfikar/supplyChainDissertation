import pandas as pd
import numpy as np
import datetime

def dframe(spl):
  data = spl.sort_values(by=[
    'ret_price_off',
    'whs_price_off',
    'spl_price_off'
    ]).groupby([
        'cust_id'
        ],as_index=False).first()

  trn = pd.DataFrame(columns=[
          "date","cust_id","cust_paid","cust_dlvr",
          "ret_paid","ret_dlvr",
          "whs_paid","whs_dlvr",
          "spl_paid","spl_dlvr"])

  ret_paid_gen  = False
  ret_dlvr_gen  = False
  whs_paid_gen  = False
  whs_dlvr_gen  = False
  spl_paid_gen  = False
  spl_dlvr_gen  = False
  date_index    = 0
  current_index = 0

  date_uniques    = data['cust_ordDate'].copy()
  customer_ids    = data['cust_id'].copy()
  whs_fulfill_ids = data['whs_fulfill'].copy()
  ret_fulfill_ids = data['ret_fulfill'].copy()
  data_length     = len(customer_ids)

  while current_index < data_length:

    date_unique = pd.to_datetime(
      datetime.date.fromordinal(
        date_uniques[current_index].toordinal() + date_index
        )).date()

    current_id = customer_ids[current_index]
    whs_fulfill_id = whs_fulfill_ids[current_index]
    ret_fulfill_id = ret_fulfill_ids[current_index]

    if whs_paid_gen:
      whs_paid = 1
    else:
      whs_paid = np.random.randint(0, 2)
      if whs_paid == 1:
        whs_paid_gen = True

    if whs_paid == 1:
      if ret_paid_gen:
        ret_paid = 1
        spl_paid = 1
        spl_dlvr = 1
      else:
        ret_paid = np.random.randint(0, 2)
        spl_paid = np.random.randint(0, 2)
        spl_dlvr = 0
        if ret_paid == 1:
          ret_paid_gen = True
        if spl_paid == 1:
          spl_paid_gen = True
          spl_dlvr = np.random.randint(0, 2)
          if spl_dlvr == 1:
            spl_dlvr_gen = True        
    else:
      ret_paid = 0
      spl_paid = 0
      spl_dlvr = 0

    if ret_paid == 1 and spl_dlvr == 1:
      cust_paid = np.random.randint(0, 2)
      whs_dlvr  = np.random.randint(0, 2)
    else:
      cust_paid = 0
      whs_dlvr = 0

    if cust_paid == 1 and whs_dlvr == 1:
      ret_dlvr = np.random.randint(0, 2)
      if ret_dlvr == 1:
        cust_dlvr = 1
    else:
      ret_dlvr = 0
      cust_dlvr = 0
    

    new_rec = pd.DataFrame({
      "date"      : [date_unique],
      "cust_id"   : [current_id],
      "cust_paid" : [cust_paid],
      "cust_dlvr" : [cust_dlvr],
      "ret_paid"  : [ret_paid],
      "ret_dlvr"  : [ret_dlvr],
      "whs_paid"  : [whs_paid],
      "whs_dlvr"  : [whs_dlvr],
      "spl_paid"  : [spl_paid],
      "spl_dlvr"  : [spl_dlvr],
    })

    trn = pd.concat([trn, new_rec], ignore_index=True)

    date_index += 1

    if cust_paid == 1 and ret_paid == 1 and ret_dlvr == 1 and whs_paid == 1 and whs_dlvr == 1 and spl_dlvr == 1:
      current_index += 1
      date_index = 0
      ret_paid_gen = False
      ret_dlvr_gen = False
      whs_paid_gen = False
      whs_dlvr_gen = False
      spl_dlvr_gen = False

  data = pd.merge(data,trn,how='left',on=['cust_id'])

  condition1 = (data['whs_fulfill']==1)&(data['spl_dlvr']==1)
  data.loc[condition1, ['spl_dlvr']] = data.loc[condition1, ['spl_dlvr']].replace(1, 0)

  condition6 = (data['whs_fulfill']==1)&(data['spl_paid']==1)
  data.loc[condition6, ['spl_paid']] = data.loc[condition6, ['spl_paid']].replace(1, 0)

  condition2 = (data['ret_fulfill']==1)&(data['whs_paid']==1)
  data.loc[condition2, ['whs_paid']] = data.loc[condition2, ['whs_paid']].replace(1, 0)

  condition3 = (data['ret_fulfill']==1)&(data['whs_dlvr'] == 1)
  data.loc[condition3, ['whs_dlvr']] = data.loc[condition3, ['whs_dlvr']].replace(1, 0)

  condition4 = (data['ret_fulfill']==1)&(data['spl_dlvr'] == 1)
  data.loc[condition4, ['spl_dlvr']] = data.loc[condition4, ['spl_dlvr']].replace(1, 0)

  condition5 = (data['ret_fulfill']==1)&(data['spl_paid']==1)
  data.loc[condition5, ['spl_paid']] = data.loc[condition5, ['spl_paid']].replace(1, 0)

  return data
