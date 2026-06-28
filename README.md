# adaptive-market-regime-classification
A Python-based systematic trading strategy that dynamically adjusts market exposure using volatility, drawdown, and trend signals. It classifies market regimes and allocates exposure accordingly. Backtested on SPY, JPM and Meta and evaluated using Sharpe ratio and maximum drawdown against a buy-and-hold benchmark.

---

## Overview

Traditional strategies often use fixed exposure regardless of market conditions. This project instead builds a regime-based approach where exposure is adjusted dynamically depending on market risk and trend characteristics.

The model is backtested on historical SPY data and evaluated against a buy-and-hold benchmark.

---

## Methodology

The strategy uses three main signals:

- **Volatility (Rolling Std of Returns):** Identifies high-risk vs low-risk market conditions  
- **Drawdown:** Measures downside risk relative to recent peaks  
- **Trend Signal (Moving Average Slope):** Captures directional momentum  

Based on these features, the model classifies market regimes and assigns exposure levels dynamically (low / medium / high).

---

## Backtesting

The strategy is tested using historical SPY,JPM and Meta price data and compared against a buy-and-hold strategy. In terms of maximum drawdown and sharpe ratio, the strategy performed much better than the buy-and-hold benchmark signifying a safer and more predictable return.

### Metrics Used:
- Cumulative Returns  
- Sharpe Ratio  
- Maximum Drawdown  

---

## Key Features

- Rolling volatility and drawdown computation  
- Adaptive threshold-based regime detection  
- Dynamic exposure allocation  
- Benchmark comparison with buy-and-hold  
- Risk-adjusted performance evaluation  

---

## Limitations

- Parameters are heuristically chosen (not optimized) and can further be improvised by training the model with machine learning techniques
- Strategy is exploratory, not production-ready  

---

## Technologies Used

- Python  
- Pandas  
- NumPy  
- Matplotlib  
- yfinance  

---

## Conclusion

This project explores how adaptive risk-based exposure can improve portfolio behavior under changing market conditions, with a focus on robustness and risk-adjusted performance rather than pure return maximization.
