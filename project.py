#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 18:31:24 2026

@author: antongirod
"""

# V1 pour cs50p



import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def main():
    ticker = input("Ticker: ")
    benchmark = input("Benchmark: ")
    starting = input("Start Period: ")
    ending = input("End Period: ")
    starting_actual, ending_actual ,close_share, close_benchmark, bond_ten_y = dwnl_cleaning(ticker,benchmark,starting,ending)
    return_period,return_day, return_benchmark, return_day_b ,mean_return, median_return, mean_return_b, cagre, cagr_b, variance, standard_deviation, variance_b, annual_sd, std_b, annual_vol_b, covariance, correlation = stats_calc(close_share,close_benchmark, ticker, benchmark)
    sharpe_ratio, sharpe_ratio_b, beta_ss, alpha_ss = risk_calc(bond_ten_y, cagre, annual_sd, cagr_b, annual_vol_b, ticker, benchmark, covariance, variance_b)
    plot_result(close_share, return_day, mean_return, ticker, close_benchmark, return_day_b,  mean_return_b, benchmark)



def dwnl_cleaning(ticker,benchmark,starting,ending):
    share = yf.download(ticker, start=starting, end=ending, auto_adjust=True, multi_level_index=False)
    print(f"Start:\n{share.head(5)}")
    print("----------------------------------------------")
    print(f"End:\n{share.tail(5)}")
    print("----------------------------------------------")
    close_share = share["Close"]

    bench_df = yf.download(benchmark, start=starting,end=ending, auto_adjust= True, multi_level_index=False)
    close_benchmark = bench_df["Close"]
    print("----------------------------------------------")
    bond_ten_y = yf.download("^TNX", start=starting, end=ending, auto_adjust=True, multi_level_index=False)

#timecheck

    expected_starting = pd.to_datetime(starting)
    expected_ending = pd.to_datetime(ending)
    if close_share.index[0] > expected_starting or expected_ending > close_share.index[-1]:
        print(f"Requested data from {starting} to {ending}")
        print(f"Actual data available from {close_share.index[0]} to {close_share.index[-1]}")
        return (close_share.index[0], close_share.index[-1],close_share, close_benchmark, bond_ten_y)
    else:
        return (close_share.index[0], close_share.index[-1],close_share, close_benchmark, bond_ten_y)
    
#-----------------------------------------------------------

def stats_calc(close_share,close_benchmark,ticker, benchmark):
    return_per, return_day = return_share(close_share)
    return_per_b,return_day_b = return_b(close_benchmark)
    mean_return, median_return, mean_return_b = mean_median(return_day, return_day_b)
    cagr_share, cagr_bench = cagr(close_share, close_benchmark)
    variance, standard_dev_share,variance_b, annual_std_share,std_b, annual_std_b = var_std(return_day, mean_return, return_day_b, mean_return_b)
    covariance, correlation = cov_corr(return_day, return_day_b, mean_return, mean_return_b, standard_dev_share,std_b, ticker, benchmark)
    return(return_per, return_day, return_per_b, return_day_b, mean_return, median_return, mean_return_b, cagr_share, cagr_bench, variance, standard_dev_share,variance_b, annual_std_share, std_b, annual_std_b, covariance, correlation)

    


#return period
def return_share(close_share):
    return_period = (close_share.iloc[-1] - close_share.iloc[0])/close_share.iloc[0]
    print(f"the return of the share on the period is: {return_period * 100:.2f}%")
    return_day = close_share.pct_change().dropna()
#    print("----------------------------------------------")
    return (return_period, return_day)

def return_b(close_benchmark):
    return_benchmark = (close_benchmark.iloc[-1] - close_benchmark.iloc[0])/close_benchmark.iloc[0]
    print(f"the return  of the benchmark on the period is: {return_benchmark * 100:.2f}%")
   
    return_day_b = close_benchmark.pct_change().dropna()
    print("----------------------------------------------")
    return (return_benchmark, return_day_b)
    


def mean_median(return_day, return_day_b):

    mean_return_share = np.mean(return_day)
    median_return_share = np.median(return_day)
    mean_return_b = np.mean(return_day_b)
    print(f"\nthe average daily return: {mean_return_share * 100 :.2f}%") 
    print(f"the daily median return: {median_return_share *100:.2f}%")
    print(f"\nthe average daily return for the benchmark: {mean_return_b * 100 :.2f}%")
    return (mean_return_share, median_return_share, mean_return_b)
    

def cagr(close_share, close_benchmark):
    diff_year = close_share.index[-1] - close_share.index[0]
    nb_year = diff_year.days/ 365.25
    cagre = ((close_share.iloc[-1]/close_share.iloc[0])** (1/nb_year) ) - 1
    cagre_b = ((close_benchmark.iloc[-1]/close_benchmark.iloc[0])** (1/nb_year) ) - 1
    print(f"the CAGR is {cagre * 100:.2f}%")
    print(f"the CAGR for the benchmark is {cagre_b * 100:.2f}%")
    print("----------------------------------------------")
    return(cagre, cagre_b)
    

def var_std(return_day, mean_return, return_day_b, mean_return_b):

    tot_sum_v = []
    for n in return_day:
        sum_v = ((n - mean_return) **2)
        tot_sum_v.append(sum_v)
    total_sum_v = sum(tot_sum_v)
    var_share = total_sum_v/( len(return_day) -1)
    print(f"the daily variance is {var_share:.6f}")

    standard_deviation_share = var_share ** 0.5
    var_b = np.var(return_day_b, ddof=1)
    standard_b = np.std(return_day_b, ddof=1)
    print(f"the daily standard deviation is {standard_deviation_share * 100:.2f}%")

    annual_sd = standard_deviation_share * (252 ** 0.5)
    annual_vol_b = standard_b * np.sqrt(252)
    print(f"the annualized volatility is {annual_sd * 100:.2f}%")
    print(f"the annualized volatility of the benchmark is {annual_vol_b * 100:.2f}%")
    print("----------------------------------------------")
    return(var_share, standard_deviation_share, var_b, annual_sd, standard_b, annual_vol_b)
    


def cov_corr(return_day, return_day_b, mean_return, mean_return_b, standard_dev_share, std_b, ticker, benchmark):
    cova = []
    a = 0
    for return_xi_tick, return_yi_b in zip(return_day, return_day_b):
        start_cov_t = (return_xi_tick - mean_return)
        start_cov_b = (return_yi_b - mean_return_b)
        start_cov = start_cov_t * start_cov_b
        cova.append(start_cov)
        a += 1
    cov = (np.sum(cova))/(len(return_day)-1)
    
    corr = cov/(standard_dev_share * std_b)
    print(f"the correlation between {ticker} and {benchmark} is {corr:.2F}")
    print("----------------------------------------------")
    return (cov, corr)

#-----------------------------------------------------
def risk_calc(bond_ten_y, cagre, annual_sd, cagr_b, annual_vol_b, ticker, benchmark, covariance, variance_b):
    last_ten_y = (bond_ten_y["Close"].squeeze().iloc[-1])/ 100
    print(f"10Y Treasury yield: {last_ten_y}")
    sharpe_ratio, sharpe_ratio_b =sharpe_r(last_ten_y, cagre, annual_sd, cagr_b, annual_vol_b, ticker, benchmark)
    beta_ss, alpha_ss = beta_alpha_simple(covariance, variance_b,last_ten_y, cagre, cagr_b, ticker)
    
    return(sharpe_ratio, sharpe_ratio_b, beta_ss, alpha_ss)

def sharpe_r(last_ten_y, cagre, annual_sd, cagr_b, annual_vol_b, ticker, benchmark):


    sharpe_ratio_share = (cagre - last_ten_y)/ annual_sd
    sharpe_ratio_bench = (cagr_b - last_ten_y)/ annual_vol_b
    print(f"the sharpe ratio of {ticker} is :{sharpe_ratio_share:.2f}")
    print(f"the sharpe ratio of {benchmark} is :{sharpe_ratio_bench:.2f}")
    print("----------------------------------------------")
    return(sharpe_ratio_share, sharpe_ratio_bench)
    


def beta_alpha_simple(covariance, variance_b, last_ten_y, cagre, cagr_b, ticker):
    print(f"covariance: {covariance}")
    print(f"benchmark variance: {variance_b}")
    beta_simple_share = (covariance/ variance_b)
    alpha_simple_share = cagre - (last_ten_y + beta_simple_share * (cagr_b - last_ten_y))
    print(f"the beta of {ticker} is :{beta_simple_share:.2f}")
    print(f"the alpha of {ticker} is :{alpha_simple_share * 100:.2f}%")
    print("----------------------------------------------")
    return (beta_simple_share, alpha_simple_share)



def plot_result(close_share, return_day, mean_return, ticker, close_benchmark, return_day_b,  mean_return_b, benchmark):

#daily return for the share
    plt.figure(figsize=(11,4))
    plt.plot(close_share.index[1:],return_day, color="blue")
    plt.axhline(y=mean_return)
    plt.title(f"daily return of {ticker}")
    plt.show()

#daily return for benchmark
    plt.figure(figsize=(11,4))
    plt.plot(close_benchmark.index[1:],return_day_b, color="red")
    plt.axhline(y=mean_return_b)
    plt.title(f"daily return of {benchmark}")
    plt.show()


#compare return
    hund_return_day = (close_share/close_share.iloc[0])* 100
    hund_return_bday = (close_benchmark/close_benchmark.iloc[0])* 100

    plt.figure(figsize=(12,5))
    plt.plot(close_share.index, hund_return_day, color="blue", label=ticker)
    plt.plot(close_benchmark.index, hund_return_bday, color="red", label=benchmark)
    plt.title(f"Return on the period for {ticker} and the benchmark")
    plt.xlabel("Date")
    plt.ylabel("Value (base 100)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()


#distribution of return
    return_hundred = np.array(return_day) * 100
    return_hundred_b = np.array(return_day_b) * 100

    plt.figure(figsize=(12,5))
    plt.hist(return_hundred,label=ticker,bins=50,alpha=0.7,edgecolor="black", color="blue")
    plt.hist(return_hundred_b,label=benchmark,bins=50,alpha=0.8,edgecolor="black", color="red")
    plt.title(f"Distribution daily return of {ticker} vs {benchmark}")
    plt.xlabel("Daily return")
    plt.xlim(-15, 15)
    plt.legend()
    plt.show()


if "__main__" == __name__:
    main()
    




