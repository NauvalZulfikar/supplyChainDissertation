import pandas as pd
import numpy as np
import datetime
import hashlib

# customer
# customer
def customer(size):
    cust_ordDate   = [i for i in pd.to_datetime(np.random.randint(19723 , 19723+365, size=size), unit='D')]
    month          = [cust_ordDate[i].month for i in range(len(cust_ordDate))]
    cust_id        = [f'cust_{i}' for i in range(1,size+1)] # hashed
    cust_req_id    = [f'cust_req_{i}' for i in range(1,size+1)] # hashed
    prod_name      = [f'product_{i}' for i in np.random.randint(1, 26, size=size)]
    cust_quan_req  = [i for i in np.random.randint(0,5000, size=size)]
    cust_price_ord = [i for i in np.random.uniform(0,2.5, size=size)]
    cust_duedates  = [pd.to_datetime(datetime.date.fromordinal(i.date().toordinal() + np.random.randint(6,7*2))) for i in cust_ordDate]

    cust                   = pd.DataFrame()
    cust['cust_ordDate']   = cust_ordDate
    cust['month']          = month
    cust['cust_id']        = cust_id
    cust['cust_req_id']    = cust_req_id
    cust['prod_name']      = prod_name
    cust['cust_quan_req']  = cust_quan_req
    cust['cust_price_ord'] = cust_price_ord
    cust['cust_fulfill']   = 1
    cust['cust_duedate']  = cust_duedates

    return cust
