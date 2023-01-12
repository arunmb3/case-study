import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
#calculate the projected divided

df = pd.read_csv("DividendData - Sheet1.csv")

for index in df.index:
    #market cap processing
    mc_col = df.loc[index, 'Market Cap']
    if mc_col[-1] == "T":
        df.loc[index, 'Market Cap'] = float(mc_col[:len(mc_col) -1]) * 1000000000000
    if mc_col[-1] == "B":
        df.loc[index, 'Market Cap'] = float(mc_col[:len(mc_col) -1]) * 1000000000

    #cash on hand processing
    coh_col = df.loc[index, "Cash on Hand"]
    coh_col = coh_col.replace(',', "")
    df.loc[index, "Cash on Hand"] = float(coh_col[1:]) * 1000000

    #net income processing
    ni_col = df.loc[index, "Net Income"]
    ni_col = ni_col.replace(',', "")
    neg = False
    if(ni_col[0] == "-"):
        neg = True
    if(neg):
        df.loc[index, "Net Income"] = (0 - float(ni_col[2:])) * 1000000
    else:
        df.loc[index, "Net Income"] = float(ni_col[1:]) * 1000000

    #free cash flow processing

    fcf_col = df.loc[index, "Free Cash Flow"]
    if(fcf_col[-1] == "B"):
        df.loc[index, 'Free Cash Flow'] = float(fcf_col[:len(fcf_col) -1]) * 1000000000
    else:
        fcf_col = fcf_col.replace(',', "")
        df.loc[index, "Free Cash Flow"] = float(fcf_col) * 1000000

    #yield processing
    yld = df.loc[index, "Yield"][:-1]
    df.loc[index, "Yield"] = float(yld)/100.0


model = LinearRegression()
df['Market Cap'] = df["Market Cap"].astype("float")
df['Net Income'] = df["Net Income"].astype("float")
df['Cash on Hand'] = df["Cash on Hand"].astype("float")
df["Yield"] = df["Yield"].astype("float")

model = model.fit(df[["Market Cap", "Net Income", "Free Cash Flow"]], df["Yield"])




pred_val = model.predict([[1.190000e+12 ,1.395600e+10/4 ,6.254000e+10]])

print("GOOGL Dividend projection: " + str(pred_val*100) + "%")


#error calculations
df["Prediction"] = model.predict(df[["Market Cap", "Net Income", "Free Cash Flow"]])
df["Error"] = df["Prediction"] - df["Yield"]

error_mean = df["Error"].mean() * 100

#print(df.tail(10))
print(error_mean)
over_sum =  o_count = under_sum = u_count = 0
for val in df["Error"]:
    if val > 0:
        o_count+=1
        over_sum+=val
    if val < 0:
        u_count +=1
        under_sum += val

print(o_count, u_count)
avg_over = over_sum/o_count
avg_under = abs(under_sum/u_count)
length = len(df)

print("Over Estimate: " + str(avg_over*100) + ", Under Estimate: " + str(avg_under*100))

print("Estimated range of GOOGL Dividend Yield: (" + str((pred_val - avg_under)*100) + "%, " + str((pred_val + avg_over)*100) + "%)")


