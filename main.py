# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# %% load data
fields = ["id", "base_price", "assessed_value"]
df = pd.read_csv('tb_vehicle_valuation.csv', usecols=fields)
print(df.head())

# %% processing
# drop columns with zeros
df = df[(df != 0).all(1)]
df = df.astype('str')
df['bp_first_digit'] = df.base_price.str.extract('(\d)')
df['bp_second_digit'] = df.base_price.str.extract('(\d\d)')
df['av_first_digit'] = df.assessed_value.str.extract('(\d)')
df['av_second_digit'] = df.assessed_value.str.extract('(\d\d)')

# drop nan columns
df.dropna(axis=0, inplace=True)

# replace column with 2nd digit
df.bp_second_digit = df.bp_second_digit.astype('int') % 10
df.av_second_digit = df.av_second_digit.astype('int') % 10

print(df[:10])

# %% Plot Columns
# convert columns to int
df_digits = df[['bp_first_digit', 'bp_second_digit', 'av_first_digit', 'av_second_digit']].astype('int') \
    .reset_index(drop=True)

# get length of dataframe
length, width = df_digits.shape

columns1 = np.array(df_digits.columns[:2])
columns2 = np.array(df_digits.columns[2:])
arr = [columns1, columns2]

fig, axs = plt.subplots(2, 2, figsize=(15, 15))


def plotting(col, i, j):
    plt.sca(axs[i, j])
    df_digits[col].value_counts().apply(lambda x: 100 * x / length) \
        .plot(kind='bar', title=col)
    axs[i, j].yaxis.set_major_formatter(mtick.PercentFormatter())
    # set individual bar labels using above list
    for k in axs[i, j].patches:
        # get_width pulls left or right; get_y pushes up or down
        axs[i, j].text(k.get_x(), k.get_height() + 0.5, round(k.get_height(), 2), color='green')


for i in range(len(arr)):
    for j in range(len(arr)):
        print(f'{i}, {j}')
        plotting(arr[i][j], i, j)

plt.savefig('Initial Benford.png', bbox_inches="tight")

# %%


# print(df.isna().sum())
# print(df.dtypes)
# print(df.bp_first_digit.isna().sum())
# print(df.bp_second_digit.isna().sum())

# df1 = df[df.isna().any(axis=1)]
# print(df1)
