# Quantitative Finance #

This repository includes the implementation of Chapters 2 and 3 from the book "Advances in Financial Machine Learning".

## Chapter 2: Financial Data Structures ##
The implementation includes regular bars, imbalance bars, run bars, and the cumulative sum filter. The analysis includes tests of normality, stationarity, and serial correlation.

Normality tests are based on the Kolmogorov-Smirnov (KS) and Jarque-Bera tests, as the Shapiro-Wilk test is not accurate for large samples.
Stationarity tests are based on the Augmented Dickey-Fuller (ADF) test.
Autocorrelation Function (ACF) Plots
The following ACF plots represent the log returns.

ACF Plot for Log Returns (Tick Frequency):
![Alt text for image](/plots/acf.png)

ACF Plot for Log Returns (Daily Frequency):
![Alt text for image](/plots/events/acf.png)

Cumulative Sum Filter created statistically significant correlations between Binance cash net flow data, balances count, and Bitcoin log return.

### Normality Improvement ###
![Alt text for image](/plots/events/log_price_normal.png)
![Alt text for image](/plots/events/price_cusum_normal.png)
After applying the Cumulative Sum Filter, the normality of the sample improved. The following plots demonstrate the improvement:

## Chapter 3: Labeling and Meta-Labeling ##
The implementation includes labeling whether a sample reaches profit-taking, stop-loss levels, or expiry using the Triple Barrier method. It uses the primary model to pick a side for each sample and meta-labeling to determine the bet size.

![Alt text for image](plots/labeling/return_series.png)<br>

The example above shows a return series based on prediction on test data, containing overlapping samples due to the Triple Barriers method.

### Summary ###
The primary model is a simple cross moving average model with a *100-ticks vs 1000-ticks* window, <br>
while the secondary model is a Random Forest model with *1000 trees and a maximum depth of 5*. <br>
The performance of these models is surprising, <br>
considering that they can **generate profit** even when commissions are taken into account.