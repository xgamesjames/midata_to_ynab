import pandas as pd

# read csv into a pandas dataframe
df = pd.read_csv("miDataTransactions.csv")

# remove list series from dataframe as this is the overdraft limit
df = df[:-1]

# convert Date column to datetime type
df["Date"] = pd.to_datetime(df.Date)
# then convert datetime format to YNAB datetime format 
df["Date"] = df["Date"].dt.strftime('%d/%m/%Y')

# Remove the 'Type' and 'Balance' Columns as YNAB doesn't need these (axis=1 is for column lookup)
df = df.drop('Type', axis=1)
df = df.drop('Balance', axis=1)

# Replace miData names with corresponding YNAB names
df.columns = df.columns.str.replace('Merchant/Description', 'Payee')
df.columns = df.columns.str.replace('Debit/Credit', 'Outflow')

# insert empty 'Memo' and 'Inflow columns to match YNAB format (value argument creates empty list)
df.insert(loc=2, column='Memo', value=['' for i in range(df.shape[0])])
df.insert(loc=4, column='Inflow', value=['' for i in range(df.shape[0])])

# iterate over the Outflow values to either remove the negative symbol or move positive values to the Inflow column
for n, outflow in enumerate(df["Outflow"]):
    # if value starts with a negative sign
    if outflow[0]=='-':
        # remove the negative sign from the string
        df["Outflow"][n] = df["Outflow"][n][1:] 
    # else if value is positive
    else:
        # copy value into Inflow column
        df["Inflow"][n] = df["Outflow"][n]
        # and delete the value from the Outflow column
        df["Outflow"][n] = ""

# export the dataframe to csv file
df.to_csv("miDataTransactions_YNAB.csv")



