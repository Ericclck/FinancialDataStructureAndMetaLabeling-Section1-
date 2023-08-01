# Quantative-Finance

This is an implementation of Chapter 2 and 3 of "Advances of Financial Machine Learning"

Chapter 2:
Regular bars, imbalance bars, run bars, cumulative sum filter

With tests of normality, stationarity and serial correlation
Normality tests are based on KS-test and Jarque-Bera tests since Shapiro-Wilk is not accurate for large samples
Stationarity tests are based on ADF

Chapter 3:
Labeling and Meta-labeling

Label whether a sample reaches profit-taking, stop-loss levels or expiry using Triple Barrier method.
Using primary model to pick a side for each sample and Using meta-labeling to find the bet size.

![Alt text for image](/plots/events/acf.png)