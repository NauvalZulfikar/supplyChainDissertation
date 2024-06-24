import datetime
import pandas as pd
import numpy as np
from customer import customer
from retailer import retailer
from warehouse import warehouse
from supplier import supplier
from dframe import dframe

def data(num):
    size = num

    # customer
    cust = customer(size)

    # retailer
    ret = retailer(size,cust)

    # warehouse
    whs = warehouse(size,ret)

    # supplier
    spl = supplier(size,whs)

    df = dframe(spl)

    return df