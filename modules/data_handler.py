import pandas as pd
import re

df = pd.read_csv("data/BFS_Share_Price.csv")
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df.set_index('Date', inplace=True)

def extract_months(query):
matches = re.findall(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-\s]?\d{2,4}", query, re.I)
parsed = []
for m in matches:
try:
parsed.append(pd.to_datetime(m, format='%b-%y'))
except:
continue
return parsed

def handle_stock_query(query):
dates = extract_months(query)
if not dates:
return "❌ Please mention a valid month/year like 'Jan-25'."

python
Copy
Edit
if len(dates) == 1:
    month_period = dates[0].to_period("M")
    df_month = df[df.index.to_period("M") == month_period]
elif len(dates) == 2:
    df_month = df[(df.index >= dates[0]) & (df.index <= dates[1])]
else:
    return "❌ Please provide at most two date ranges."

if df_month.empty:
    return "📉 No stock data found in that period."

query_lower = query.lower()
if "highest" in query_lower:
    val = df_month['Close'].max()
    return f"📈 Highest closing price: ₹{val:.2f}"
elif "lowest" in query_lower:
    val = df_month['Close'].min()
    return f"📉 Lowest closing price: ₹{val:.2f}"
elif "average" in query_lower:
    val = df_month['Close'].mean()
    return f"📊 Average closing price: ₹{val:.2f}"
elif "compare" in query_lower:
    return df_month['Close'].resample('M').mean().to_frame().to_markdown()
else:
    return "✅ Please ask for highest, lowest, average, or compare stock price."