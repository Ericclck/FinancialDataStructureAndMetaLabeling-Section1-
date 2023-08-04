# Advanced Quantitative Finance Techniques

This repository provides a comprehensive resource for various advanced quantitative finance techniques. The implemented methodologies include Information-driven Bars, Cumulative Sum Filter, Triple Barriers Method, Meta-labeling, Sample Weighting, and Sequential Weighted Bagging. Our data sources comprise of Binance cash flow and Bitcoin balance count for Cumulative Sum Filter, and Bitcoin tick data for other methods.

## Financial Data Structures and Statistical Analysis

This library encompasses a variety of financial data structures, such as regular bars, imbalance bars, run bars, and the Cumulative Sum Filter. The statistical analysis procedures include tests for normality (Kolmogorov-Smirnov (KS) and Jarque-Bera tests), stationarity (Augmented Dickey-Fuller (ADF) test), and serial correlation (Autocorrelation Function (ACF) Plots for log returns).

![ACF Plot for Log Returns (Tick Frequency)](/plots/acf.png)
![ACF Plot for Log Returns (Daily Frequency)](/plots/events/acf.png)

Post-application of the Cumulative Sum Filter, we observed significant correlations between Binance cash net flow data, balances count, and Bitcoin log return. Additionally, there was an evident improvement in sample normality:

![Normality Improvement](/plots/events/log_price_normal.png)
![Normality Improvement](/plots/events/price_cusum_normal.png)

## Trade Labeling, Meta-Labeling, and Predictive Modeling

Our implementation includes a systematic labeling procedure using the Triple Barrier method. The primary model selects a side for each sample, while meta-labeling determines the bet size.

![Model Scores](plots/labeling/scores.png)

The above image displays Precision, Recall, and F1 scores for both primary and secondary models. While an increase in F1 scores for the secondary model was anticipated, the return series may contain overlapping samples due to the Triple Barriers method.

![Return Series](plots/labeling/return_series.png)
![Adjusted Return Series](plots/labeling/return_series_concurrency_fixed_boundary_adjusted.png)

With an increase in the max_depth of the secondary model to 10, the mean return reached 5.56e-7. However, this strategy is unprofitable when considering a 0.1% commission.

![Enhanced Return Mean](plots/labeling/return.png)

## Sample Weighting, Bagging, and Performance Evaluation

We compute sample weights considering the sum of returns, concurrency (in terms of tick over the period from the start of sample to profit-taking/stop-loss/expiry), and the cumulative uniqueness decay factor.

![Return Series with Bagging](plots/labeling/return_bagging.png)

Weighted bootstrapping was initially performed with these sample weights; however, due to high memory consumption, we switched to bagging. Despite showing a slight increase in mean return with bagging, the return series is not sufficient to cover commissions.

## Data Consolidation and Model Calibration

To reduce the number of trades (and consequently the commissions), we consolidated 5 days of tick data into one sample. This approach, however, created challenges with the Triple Barriers method, specifically with the horizontal and vertical barriers. After addressing these issues, the mean return improved but remained insufficient to cover commissions.

![Return Series](plots/labeling/return_100_run.png)
![Return mean](plots/labeling/return_100_run_mean.png)

In the case of a longer interval, our results suggest that the current strategy may not be safe or that the model may not be adequately trained due to data scarcity.

![Return Series](plots/labeling/return_1000_run.png)
![Return mean](plots/labeling/return_1000_run_mean.png)

## Conclusion and Future Directions

Our primary model utilizes a straightforward cross moving average model with specific tick windows, while the secondary model employs a Random Forest model with a maximum depth and number of trees. While no considerations were made for commissions, it's noteworthy that, despite the simplicity of these models, they can still manage to generate profits. However, the results emphasize the importance of proper data handling, model selection, hyperparameter tuning in quantitative finance, and the consideration of trading costs. Future developments will focus on refining these parameters and exploring more robust modeling techniques.