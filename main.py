import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# CREATE OUTPUT FOLDER
# ---------------------------
os.makedirs("outputs", exist_ok=True)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("data/raw_data.csv")

print("\nOriginal Data:")
print(df.head())

# ---------------------------
# FIX DATA TYPES
# ---------------------------
if "sales" in df.columns:
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

if "profit" in df.columns:
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce")

# ---------------------------
# CLEAN DATA
# ---------------------------
df = df.drop_duplicates()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna("Unknown")
    else:
        df[col] = df[col].fillna(df[col].mean())

df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

print("\nCleaned Data:")
print(df.head())

# ---------------------------
# SAVE CLEAN DATA (CSV ONLY)
# ---------------------------
df.to_csv("outputs/cleaned_data.csv", index=False)

# ---------------------------
# REPORT GENERATION
# ---------------------------
if "category" in df.columns and "sales" in df.columns:
    summary = df.groupby("category")["sales"].sum().reset_index()

elif "region" in df.columns and "sales" in df.columns:
    summary = df.groupby("region")["sales"].sum().reset_index()

else:
    summary = df.select_dtypes(include="number").sum().reset_index()
    summary.columns = ["metric", "value"]

print("\nSummary Report:")
print(summary)

# ---------------------------
# SAVE REPORT (CSV INSTEAD OF EXCEL)
# ---------------------------
summary.to_csv("outputs/report.csv", index=False)

# ---------------------------
# VISUALIZATION
# ---------------------------
plt.figure(figsize=(8,5))

plt.bar(summary.iloc[:,0].astype(str), summary.iloc[:,1])

plt.title("Automated Data Report")
plt.xlabel("Category")
plt.ylabel("Values")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("outputs/chart.png")
plt.show()

print("\n✅ PROJECT COMPLETED SUCCESSFULLY ")
print("Check 'outputs' folder for results.")