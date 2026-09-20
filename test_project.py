#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 09:56:59 2026

@author: antongirod
"""

#Pytest cs50p


from project import return_share
import pandas as pd

def test_return_share():
    close_share= pd.Series([100, 110, 121])
    return_period, return_day = return_share(close_share)
    assert return_period == 0.21
    assert return_day[0] == 0.10
    assert return_day[1] == 0.10
    

from project import cagr

def test_cagr():
    close_share = pd.Series([100, 150, 200])
    close_benchmark = pd.Series([100, 120, 150])
    cagr_share, close_benchmark =cagr(close_share, close_benchmark)
    
    assert cagr_share == 0.5
    


from project import mean_median

def test_mean_median():
    return_day = pd.Series([0.1, 0.15, 0.2])
    return_day_b = pd.Series([0.1, 0.1, 0.16])
    
    mean_return_share, median_return_share, mean_return_b = mean_median(return_day, return_day_b)
    
    assert mean_return_share == 0.15
    assert mean_return_b == 0.12