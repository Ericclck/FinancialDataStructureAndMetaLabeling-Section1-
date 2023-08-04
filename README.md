# Advanced Quantitative Finance Methods Implementation

This repository presents a comprehensive assortment of implementations for key methodologies in quantitative finance. Our focus spans across several techniques, including Information-driven Bars, Cumulative Sum Filter, Triple Barriers Method, Meta-labeling, Sample Weighting, and Sequential Weighted Bagging. The objective is to provide a detailed approach to understanding and implementing these methods while analyzing their performance and relevance.

Two set of data is used, Binance cash flow and bitcoin Balance count is used for Cumulative Sum Filter,
and bitcoin tick data is used for other methods.

## Financial Data Structures & Statistical Analysis

Our library offers a diverse set of data structures that are essential in financial analysis. This collection incorporates regular bars, imbalance bars, run bars, and the Cumulative Sum Filter. Additionally, we feature numerous analytical procedures such as tests of normality, stationarity, and serial correlation.

Our approach to normality testing involves the use of Kolmogorov-Smirnov (KS) and Jarque-Bera tests, as we find the Shapiro-Wilk test less accurate for larger datasets. For stationarity testing, we employ the Augmented Dickey-Fuller (ADF) test. Autocorrelation Function (ACF) Plots serve to represent the log returns.

Notably, we observed significant correlations between Binance cash net flow data, balances count, and Bitcoin log return after applying the Cumulative Sum Filter. Furthermore, the application of this filter resulted in an enhanced sample normality.

## Labeling Techniques & Meta-Labeling

Our methodology includes a systematic procedure for labeling whether a sample reaches profit-taking, stop-loss levels, or expiry using the Triple Barrier method. Furthermore, we utilize the primary model to select a side for each sample, and meta-labeling is implemented to determine the bet size.

Our results show an increase in F1 scores for the secondary model, as expected. However, it's crucial to note that any return series illustrated might contain overlapping samples due to the Triple Barriers method.

## Sample Weighting & Bagging

We compute sample weights using a method that considers the sum of returns, concurrency in terms of tick over the period from the start of the sample to profit-taking/stop-loss/expiry, and multiplies by the cumulative uniqueness decay factor.

Subsequently, bagging is conducted with six models, each featuring 1,000 trees and a maximum depth of 10, considering the average weighting is around 0.17.

Despite showing a slight increase in mean return with bagging, the return series is not sufficient to cover commissions. The model's high trading volume in a day (overlapping trading windows) leads to significant losses due to commissions.

## Data Consolidation & Challenges

To reduce the number of trades and consequently the commissions, we have consolidated 5 days of tick data into one sample. This approach, however, created challenges with the Triple Barriers method, specifically with the horizontal and vertical barriers. After addressing these issues, the mean return improved but remained insufficient to cover commissions.

In the case of a longer interval, our results suggest that the current strategy may not be safe or that the model may not be adequately trained due to data scarcity.

## Conclusion

Our primary model utilizes a straightforward cross moving average model with specific tick windows, while the secondary model employs a Random Forest model with a maximum depth and number of trees. It's noteworthy that, despite the simplicity of these models and the absence of commission considerations, they can still manage to generate profits. However, the results emphasize the importance of proper data handling, model selection, and hyperparameter tuning in quantitative finance.