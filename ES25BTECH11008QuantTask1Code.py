import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# DOWNLOAD DATA(A# DOWNLOAD DATA (The strategy was also tested on JPM and META by changing the ticker symbol)

data = yf.download(
    "SPY",
    start="2014-01-01",
    end="2026-05-14",
    auto_adjust=True
)

df = pd.DataFrame(index=data.index)
df['Close'] = data['Close'].to_numpy().flatten()

# RETURNS


df['Returns'] = df['Close'].pct_change()

# VOLATILITY


df['Volatility'] = (
    df['Returns']
    .rolling(window=30)
    .std()
    * np.sqrt(252)
)

# MOVING AVERAGES

df['MA_10'] = df['Close'].rolling(window=10).mean()
df['MA_50'] = df['Close'].rolling(window=50).mean()

df['Slope'] = (
    (df['MA_10'] - df['MA_50'])
    / df['MA_50']
)

# ROLLING MAX/MIN


df['Rolling_Max'] = df['Close'].rolling(window=252).max()
df['Rolling_Min'] = df['Close'].rolling(window=252).min()


# DRAWDOWN


df['Drawdown'] = (
    (df['Close'] - df['Rolling_Max'])
    / df['Rolling_Max']
)


# RANGE POSITION


df['Range_Position'] = (
    (df['Close'] - df['Rolling_Min'])
    /
    (df['Rolling_Max'] - df['Rolling_Min'])
)


# ADAPTIVE THRESHOLDS


df['Vol_Upper'] = df['Volatility'].rolling(252).quantile(0.85)
df['Vol_Lower'] = df['Volatility'].rolling(252).quantile(0.40)
df['DD_Q15'] = df['Drawdown'].rolling(252).quantile(0.15)


# STRATEGY


exposure = []

for i in range(len(df)):

    vol = df['Volatility'].iloc[i]
    vol_upper = df['Vol_Upper'].iloc[i]
    vol_lower = df['Vol_Lower'].iloc[i]

    dd = df['Drawdown'].iloc[i]
    dd_q15 = df['DD_Q15'].iloc[i]

    range_pos = df['Range_Position'].iloc[i]
    slope = df['Slope'].iloc[i]

    # Handle NaNs
    if (
        np.isnan(vol)
        or np.isnan(vol_upper)
        or np.isnan(vol_lower)
        or np.isnan(dd)
        or np.isnan(dd_q15)
        or np.isnan(range_pos)
        or np.isnan(slope)
    ):
        exposure.append(0.3)
        continue


    # HIGH VOLATILITY REGIME


    if vol > vol_upper:

        signal = 0.3


    # LOW VOLATILITY TREND-FOLLOWING REGIME


    elif vol < vol_lower:

        if range_pos > 0.60 and slope > 0:

            signal = 1.0

        else:

            signal = 0.6


    # MODERATE VOLATILITY REGIME


    else:

        if (
            dd < dd_q15
            and range_pos < 0.60
        ):

            signal = 1.0

        else:

            signal = 0.6

    exposure.append(signal)

df['Exposure'] = exposure


# STRATEGY RETURNS


df['Strategy_Returns'] = df['Exposure'].shift(1) * df['Returns']
df['Strategy_Returns'] = df['Strategy_Returns'].fillna(0)


# BENCHMARK AND STRATEGY CURVES


df['Buy_Hold_Curve'] = (1 + df['Returns']).cumprod()
df['Strategy_Curve'] = (1 + df['Strategy_Returns']).cumprod()


# DRAWDOWNS


strategy_peak = df['Strategy_Curve'].cummax()
df['Strategy_Drawdown'] = (df['Strategy_Curve'] - strategy_peak) / strategy_peak

bh_peak = df['Buy_Hold_Curve'].cummax()
df['BH_Drawdown'] = (df['Buy_Hold_Curve'] - bh_peak) / bh_peak


# METRICS


strategy_return = df['Strategy_Curve'].iloc[-1] - 1
buyhold_return = df['Buy_Hold_Curve'].iloc[-1] - 1

strategy_maxdd = df['Strategy_Drawdown'].min()
buyhold_maxdd = df['BH_Drawdown'].min()

strategy_sharpe = (
    df['Strategy_Returns'].mean() /
    df['Strategy_Returns'].std()
) * np.sqrt(252)

buyhold_sharpe = (
    df['Returns'].mean() /
    df['Returns'].std()
) * np.sqrt(252)


# RESULTS


print("\n============== PERFORMANCE ==============\n")

print(f"Strategy Return: {strategy_return:.2%}")
print(f"Buy & Hold Return: {buyhold_return:.2%}\n")

print(f"Strategy Max Drawdown: {strategy_maxdd:.2%}")
print(f"Buy & Hold Max Drawdown: {buyhold_maxdd:.2%}\n")

print(f"Strategy Sharpe Ratio: {strategy_sharpe:.2f}")
print(f"Buy & Hold Sharpe Ratio: {buyhold_sharpe:.2f}")

print("\n=========================================\n")


# GRAPH 1: EQUITY CURVES


plt.figure(figsize=(16, 8))

plt.plot(df.index, df['Buy_Hold_Curve'], label='Buy & Hold')
plt.plot(df.index, df['Strategy_Curve'], label='Adaptive Strategy')

plt.title('Strategy vs Buy & Hold')
plt.xlabel('Date')
plt.ylabel('Portfolio Growth')
plt.legend()
plt.grid()
plt.show()


# GRAPH 2: VOLATILITY


plt.figure(figsize=(16, 6))

plt.plot(df.index, df['Volatility'], label='Volatility')
plt.plot(df.index, df['Vol_Upper'], linestyle='--', label='Upper Threshold')
plt.plot(df.index, df['Vol_Lower'], linestyle='--', label='Lower Threshold')

plt.title('Adaptive Volatility Thresholds')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.grid()
plt.show()


# GRAPH 3: DRAWDOWN


plt.figure(figsize=(16, 6))

plt.plot(df.index, df['Drawdown'], label='Drawdown')
plt.plot(df.index, df['DD_Q15'], linestyle='--', label='15th Percentile Threshold')

plt.title('Adaptive Drawdown Threshold')
plt.xlabel('Date')
plt.ylabel('Drawdown')
plt.legend()
plt.grid()
plt.show()


# GRAPH 4: EXPOSURE


plt.figure(figsize=(16, 6))

plt.plot(df.index, df['Exposure'], label='Exposure')

plt.title('Dynamic Market Exposure')
plt.xlabel('Date')
plt.ylabel('Exposure')
plt.legend()
plt.grid()
plt.show()