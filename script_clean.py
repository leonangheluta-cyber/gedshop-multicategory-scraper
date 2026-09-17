# %%
import pandas as pd
df=pd.read_json("work.json")
df2=pd.read_json("gadget.json")
df3=pd.read_json("sport.json")
df.head()


# %%
print(df.shape, df2.shape, df3.shape)

# %%
print(df["Name"].isna().sum(), df2["Name"].isna().sum(), df3["Name"].isna().sum())

# %%
print(df["Item Code"].isna().sum(), df2["Item Code"].isna().sum(), df3["Item Code"].isna().sum())

# %%
print(df["Material"].isna().sum(), df2["Material"].isna().sum(), df3["Material"].isna().sum())

# %%
print(df["Description"].isna().sum(), df2["Description"].isna().sum(), df3["Description"].isna().sum())

# %%
print(df["Price"].isna().sum(), df2["Price"].isna().sum(), df3["Price"].isna().sum())

# %%
print(df["Price"].head(), df2["Price"].head(), df3["Price"].head())

# %%
df["Price"]=df["Price"].str.replace(",", ".")
df2["Price"]=df2["Price"].str.replace(",", ".")
df3["Price"]=df3["Price"].str.replace(",", ".")

# %%
df["Price"]=df["Price"].str.split("€").str[1]
df2["Price"]=df2["Price"].str.split("€").str[1]
df3["Price"]=df3["Price"].str.split("€").str[1]

# %%
df["Price"]=df["Price"].astype(float)
df2["Price"]=df2["Price"].astype(float)
df3["Price"]=df3["Price"].astype(float)

# %%
print(df["Price"].head(), df2["Price"].head(), df3["Price"].head())

# %%
print(df["Price"].isna().sum(), df2["Price"].isna().sum(), df3["Price"].isna().sum())

# %%
print(df.duplicated().sum(), df2.duplicated().sum(), df3.duplicated().sum())

# %%
print(df.dtypes, df2.dtypes, df3.dtypes)

# %%
df["Category"]="Work"
df2["Category"]="Gadget"
df3["Category"]="Sport"
data_frames=pd.concat([df, df2, df3])
with pd.ExcelWriter("all_categories.xlsx") as writer:
    data_frames.to_excel(writer, sheet_name="ALL PRODUCTS", index=False)
    df.to_excel(writer, sheet_name="WORK", index=False)
    df2.to_excel(writer, sheet_name="GADGET", index=False)
    df3.to_excel(writer, sheet_name="SPORT", index=False)

# %%
data=pd.read_excel("all_categories.xlsx")
data.head()

# %%
sample=data.head()
sample.to_excel("samples_data.xlsx", index=False)

# %%
import matplotlib.pyplot as plt
mean_price=data.groupby("Category")["Price"].mean()
plt.figure(figsize=(10, 6))
plt.bar(mean_price.index, mean_price.values, color="#6c52dfe3")
plt.xlabel("CATEGORIES")
plt.ylabel("MEAN PRICE")
plt.title("MEAN PRICE PER CATEGORY")
plt.savefig("mean_price.png", dpi=150, bbox_inches="tight")
plt.show()


# %%
price_mask=data["Price"].isna()
data["Available"]=price_mask
data["Available"]=data["Available"].replace({True: "No", False: "Yes"})
availability=data.groupby("Category")["Available"].value_counts()
availability_wide=availability.unstack()
availability_wide.plot(kind="bar", figsize=(10, 6))
plt.xticks(rotation=0)
plt.legend(title="Available")
plt.xlabel("CATEGORIES")
plt.ylabel("NUMBER OF PRODUCTS")
plt.title("AVAILABILITY PER CATEGORY")
plt.savefig("availability.png", dpi=150, bbox_inches="tight")


