# Quantitative Finance Library

This repository contains a comprehensive implementation of various quantitative finance methodologies including Information-driven Bars, Cumulative Sum Filter, Triple Barriers Method, Meta-labeling, Sample Weighting and Sequential Weighted Bagging.

## Financial Data Structures

The library features a range of data structures customary to financial analysis. These include regular bars, imbalance bars, run bars, and the Cumulative Sum Filter. The analysis procedures comprise tests of normality, stationarity, and serial correlation.

- Normality tests utilize Kolmogorov-Smirnov (KS) and Jarque-Bera tests, as Shapiro-Wilk test is deemed less accurate for extensive datasets.
- Stationarity tests employ the Augmented Dickey-Fuller (ADF) test.
- Autocorrelation Function (ACF) Plots are used to represent the log returns.

**ACF Plot for Log Returns (Tick Frequency):**
![ACF Plot for Log Returns (Tick Frequency)](/plots/acf.png)

**ACF Plot for Log Returns (Daily Frequency):**
![ACF Plot for Log Returns (Daily Frequency)](/plots/events/acf.png)

Significant correlations were observed between Binance cash net flow data, balances count, and Bitcoin log return after the application of Cumulative Sum Filter.

### Normality Improvement
After applying the Cumulative Sum Filter, an improvement in sample normality was observed. The following plots illustrate this enhancement:

![Normality Improvement](/plots/events/log_price_normal.png)
![Normality Improvement](/plots/events/price_cusum_normal.png)

## Labeling and Meta-Labeling

The implementation includes a procedure for labeling whether a sample reaches profit-taking, stop-loss levels, or expiry using the Triple Barrier method. The primary model is used to select a side for each sample, and meta-labeling is employed to determine the bet size.

![Model Scores](plots/labeling/scores.png)

The image above depicts the Precision, Recall, and F1 scores for both primary and secondary models. As anticipated, the F1 scores increase for the secondary model.

![Return Series](plots/labeling/return_series.png)

The return series based on prediction on test data may contain overlapping samples due to the Triple Barriers method. However, the concurrency of the sampling is found to be low, and after adjusting the concurrency and test data boundaries to match sample weight boundaries, the return series now looks like this:

![Adjusted Return Series](plots/labeling/return_series_concurrency_fixed_boundary_adjusted.png)

Please note that any return series displayed above is not the actual return series as each sample might overlap with each other.

After increasing the max_depth of the secondary model to 10, the return series looks like this:

![Enhanced Return Series](plots/labeling/return.png)

Please note, this strategy would not be profitable if a commission of 0.1% is considered.

### Sample Weighting and Bagging

Sample weights are computed using the following formula:
- Sum of returns,
- Divided by concurrency in terms of tick over the period from the start of sample to profit-taking/stop-loss/expiry,
- Multiplied by the cumulative uniqueness decay factor.

Weighted bootstrapping is then performed with these sample weights. Initially, sequential bootstrapping was used, but due to high memory consumption, the process was switched to bagging. Bagging is conducted with six models, each with 1,000 trees and a maximum depth of 10, as the average weighting is around 0.17.

![Return Series with Bagging](plots/labeling/return_bagging.png)

With bagging, the return series shows a slight increase in the mean return, although not sufficient to cover commissions.

### Summary

The primary model is a simple cross moving average model with a 100-ticks vs 1000-ticks window, while the secondary model is a Random Forest model with 1,000 trees and a maximum depth of 10.

While no considerations were made for commissions, given the simplicity of both models, it is notable that they can generate any profit at all.