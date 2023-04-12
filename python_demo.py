#%%

import pandas as pd
# %%

df = pd.read_csv(r"survey_demo_data.csv")
# %%

df.head()

# %%

df.shape
# %%

df.describe()
# %%

df.columns
# %%

df['age']
# %%

df['gender'].value_counts()
# %%
df['region'].value_counts()
# %%

pd.crosstab(df['gender'], df['region'])
# %%

df.groupby('region').mean()
# %%

import pandas as pd
import matplotlib.pyplot as plt

# Create the DataFrame
data = {'region': ['Midwest', 'Northeast', 'Northwest', 'Southeast', 'Southwest'],
        'age': [47.02, 46.00, 44.62, 45.28, 46.85],
        'gender_encode': [0.50, 0.54, 0.48, 0.53, 0.50],
        'region_encode': [5.0, 1.0, 4.0, 2.0, 3.0],
        'product_satisfaction': [2.45, 2.45, 2.54, 2.59, 2.59],
        'would_buy_again': [3.05, 3.13, 3.07, 2.96, 3.02]}
df = pd.DataFrame(data)

# Group the data by region and calculate the mean age
age_by_region = df.groupby('region')['age'].mean()

# Create the bar chart
age_by_region.plot(kind='bar')

# Customize the chart
plt.title('Average age by region')
plt.xlabel('Region')
plt.ylabel('Average age')

# Show the chart
plt.show()

# %%
# Create the bar chart using seaborn
import seaborn as sns

sns.barplot(x='region', y='age', data=df)

# Customize the chart
plt.title('Average age by region')
plt.xlabel('Region')
plt.ylabel('Average age')

# Rotate x tick labels
plt.xticks(rotation=45)

# Show the chart
plt.show()
# %%

import seaborn as sns
import matplotlib.pyplot as plt

# Create the bar chart using seaborn
sns.set_style("whitegrid")
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='region', y='age', data=df, palette="Blues_r", ci=None)

# Add labels to the end of the bars
for i in ax.containers:
    ax.bar_label(i, label_type='edge', labels=[f'{h.get_height():.1f}' for h in i], padding=5)

# Customize the chart
plt.title('Average age by region', fontsize=16)
plt.xlabel('Region', fontsize=14)
plt.ylabel('Average age', fontsize=14)
plt.xticks(fontsize=12, rotation=0)
plt.yticks(fontsize=12)

# Show the chart
plt.show()

# %%

# Basic data types

# INT, FLOAT, STRING, BOOLEAN
# List, Tuple, Set, Dictionary

#%%
#this is a test
