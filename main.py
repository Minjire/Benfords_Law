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
def pre_processing(data_df):
    print(data_df.dtypes)
    print((data_df['base_price'] == 0).any())
    data_df = data_df.astype('str')
    data_df['bp_first_digit'] = data_df.base_price.str.extract('(\d)')
    data_df['bp_second_digit'] = data_df.base_price.str.extract('(\d\d)')
    data_df['bp_third_digit'] = data_df.base_price.str.extract('(\d\d\d)')
    data_df['av_first_digit'] = data_df.assessed_value.str.extract('(\d)')
    data_df['av_second_digit'] = data_df.assessed_value.str.extract('(\d\d)')
    data_df['av_third_digit'] = data_df.assessed_value.str.extract('(\d\d\d)')

    # drop nan columns
    data_df.dropna(axis=0, inplace=True)

    # replace column with 2nd digit
    data_df.bp_second_digit = data_df.bp_second_digit.astype('int') % 10
    data_df.av_second_digit = data_df.av_second_digit.astype('int') % 10
    data_df.bp_third_digit = data_df.bp_third_digit.astype('int') % 10
    data_df.av_third_digit = data_df.av_third_digit.astype('int') % 10

    print(data_df.head())
    data_df = data_df[['bp_first_digit', 'bp_second_digit', 'bp_third_digit', 'av_first_digit',
                       'av_second_digit', 'av_third_digit']].astype('int').reset_index(drop=True)
    return data_df


# %% Plot Columns
def plotting(df, col, i, j, axs):
    # get length of dataframe
    length, width = df.shape

    plt.sca(axs[i, j])
    df[col].value_counts().apply(lambda x: 100 * x / length) \
        .plot(kind='bar', title=col)
    axs[i, j].yaxis.set_major_formatter(mtick.PercentFormatter())
    # set individual bar labels using above list
    for k in axs[i, j].patches:
        # get_width pulls left or right; get_y pushes up or down
        axs[i, j].text(k.get_x(), k.get_height() + 0.5, round(k.get_height(), 5), color='green', rotation=90)


def preplot(df_digits, name):
    # convert columns to int
    df_digits = pre_processing(df_digits)

    # print((df_digits['bp_first_digit'] == 0).any())

    fig, axs = plt.subplots(2, 3, figsize=(15, 15))

    columns1 = np.array(df_digits.columns[:3])
    columns2 = np.array(df_digits.columns[3:])
    arr = [columns1, columns2]
    print(f"Array: {arr}")

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(f'{i}, {j}')
            plotting(df_digits, arr[i][j], i, j, axs)

    fig1 = plt.gcf()
    plt.show()
    fig1.savefig(name, bbox_inches="tight", dpi=100)


# %%
# drop columns with zeros
# df =
preplot(df[(df != 0).all(1)], 'Initial Benford.png')

# %% Refined implementation
print(f"Original Dataframe row count: {len(df.index)}")
base_price = df[(df.astype('int64')[['base_price']] != 0).all(1)]
print(base_price.head())
print(f"Row count of Dataframe without base price 'zero' values: {len(base_price.index)}")
print(f"Dropped 'zero' rows in Dataframe: {len(df.index) - len(base_price.index)}")
# assessed_value = df[df[['assessed_value']].eq(0).all(1)]
assessed_value = df[(df[['assessed_value']] != 0).all(1)]
print(f"Row count of Dataframe without assessed price 'zero' values: {len(assessed_value.index)}")
print(f"Dropped 'zero' rows in Dataframe: {len(df.index) - len(assessed_value.index)}")

# %% PLot new dataframe
# df without zeros in base_price column
preplot(base_price, "No Base Price 'Zero' Values.png")
# df without zeros in base_price column
preplot(assessed_value, "No Assessed Value 'Zero' Values.png")

