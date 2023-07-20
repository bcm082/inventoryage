import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




# Create a dropdown list with the following options past 7, past 14, past 30 days
st.sidebar.title("Inventory Age")
st.sidebar.subheader("Select the number of days to view")
days = st.sidebar.selectbox("Days", ["Past 7", "Past 14", "Past 21","Past 30"])

# Convert inveroty.txt to csv
inventory = pd.read_csv('inventory.txt', sep='\t')
# drop columns from inventory 3, and 6 to 10
cols_to_drop = [inventory.columns[3]] + inventory.columns[7:12].tolist()
inventory.drop(cols_to_drop, axis=1, inplace=True)
# rename the column Seller-sku to sku, Asin1 to asin, Item-name to Title, Quantity to in_stock, Price to price, Open-Date to listed_date
inventory.rename(columns={'seller-sku':'sku', 'asin1':'asin', 'item-name':'title', 'quantity':'in_stock', 'price':'price', 'open-date':'listed_date'}, inplace=True)
# adjust listed_date column to only display date
inventory['listed_date'] = inventory['listed_date'].str[:10]
# save inventory to csv
inventory.to_csv('inventory.csv', index=False)

# read past day files
past7 = pd.read_csv("past7.csv")
past14 = pd.read_csv("past14.csv")
past21 = pd.read_csv("past21.csv")
past30 = pd.read_csv("past30.csv")

# drop the columns 4 to 16 and 21
past7.drop(past7.columns[4:20].to_list() + [past7.columns[21]], axis=1, inplace=True)
past14.drop(past14.columns[4:20].to_list() + [past14.columns[21]], axis=1, inplace=True)
past21.drop(past21.columns[4:20].to_list() + [past21.columns[21]], axis=1, inplace=True)
past30.drop(past30.columns[4:20].to_list() + [past30.columns[21]], axis=1, inplace=True)

# rename the column (Parent) ASIN to parent_asin, (Child) ASIN to child_asin, Total Order Items to total_sold
past7.rename(columns={'(Parent) ASIN':'parent_asin', '(Child) ASIN':'child_asin', 'Total Order Items':'total_sold', 'SKU':'sku'}, inplace=True)
past14.rename(columns={'(Parent) ASIN':'parent_asin', '(Child) ASIN':'child_asin', 'Total Order Items':'total_sold', 'SKU':'sku'}, inplace=True)
past21.rename(columns={'(Parent) ASIN':'parent_asin', '(Child) ASIN':'child_asin', 'Total Order Items':'total_sold', 'SKU':'sku'}, inplace=True)
past30.rename(columns={'(Parent) ASIN':'parent_asin', '(Child) ASIN':'child_asin', 'Total Order Items':'total_sold', 'SKU':'sku'}, inplace=True)


# Merge inventory.csv with past7.csv
past7 = pd.merge(inventory, past7, on="sku", how="left")
# Merge inventory.csv with past14.csv
past14 = pd.merge(inventory, past14, on="sku", how="left")
# Merge inventory.csv with past21.csv
past21 = pd.merge(inventory, past21, on="sku", how="left")
# Merge inventory.csv with past30.csv
past30 = pd.merge(inventory, past30, on="sku", how="left")

# Drop child_asin column, parent_asin column, and hide the index colum for all dataframes
past7 = past7.drop(columns=["child_asin", "parent_asin"])
past14 = past14.drop(columns=["child_asin", "parent_asin"])
past21 = past21.drop(columns=["child_asin", "parent_asin"])
past30 = past30.drop(columns=["child_asin", "parent_asin"])

# set index to sku column for all dataframes
past7 = past7.set_index("sku")
past14 = past14.set_index("sku")
past21 = past21.set_index("sku")
past30 = past30.set_index("sku")

# Create a function to export the DataFrame to a CSV file
def export_df(df):
    """Export the DataFrame to a CSV file."""
    csv_file = df.to_csv(index=False)
    return st.download_button(label="Export DataFrame", data=csv_file, file_name="download.csv", mime="text/csv", key=None)

# Graphs
def plot_inventory(df):
    # Make sure to not modify the original dataframe
    df = df.copy()
    # Create a new column to calculate the percentage of inventory sold
    df["percent_sold"] = df["total_sold"] / df["in_stock"]
    # Create a new column to calculate the percentage of inventory remaining
    df["percent_remaining"] = 1 - df["percent_sold"]
    # Display the top 20 in a graph
    top10 = df.head(20)
    # Create a bar graph to display the percentage of inventory sold
    fig, ax = plt.subplots()
    ax.barh(top10.index, top10["percent_sold"], color="green")
    ax.set_title("Percentage of Inventory Sold")
    ax.set_xlabel("Percentage")
    ax.set_ylabel("SKU")

    st.pyplot(fig)



# Display df when Past 7 is selected
if days == "Past 7":
    st.title("Past 7 Days")
    st.text("*Data updates every Monday")
    # Create a search bar to search for sku
    search = st.text_input("Search")
    # Filter the data based on the SKU or title entered based on partial match
    if search:
        search = search.lower()
        filtered_df = past7[(past7.index.str.lower().str.contains(search, na=False)) | 
                            (past7['Title'].str.lower().str.contains(search, na=False))]
    else:
        filtered_df = past7
    filtered_df = filtered_df.sort_values(by="total_sold", ascending=False)
    # Reorder the columns to display sku, asin, price, in_stock, total_sold, listed_date, Title
    filtered_df = filtered_df[["asin", "price", "in_stock", "total_sold", "listed_date", "Title"]]

    # Display df
    st.dataframe(filtered_df)

    # Export df to csv
    export_df(filtered_df)

    st.markdown("---")
    st.subheader("Percentage of Inventory Sold (top 20)")

    # Display graph
    plot_inventory(filtered_df)



# Display df when Past 14 is selected
if days == "Past 14":
    st.title("Past 14 Days")
    st.text("*Data updates every Monday")
    search = st.text_input("Search")
    # Filter the data based on the SKU or title entered based on partial match
    if search:
        search = search.lower()
        filtered_df = past14[(past14.index.str.lower().str.contains(search, na=False)) | 
                            (past14['Title'].str.lower().str.contains(search, na=False))]
    else:
        filtered_df = past14
    filtered_df = filtered_df.sort_values(by="total_sold", ascending=False)
    # Reorder the columns to display sku, asin, price, in_stock, total_sold, listed_date, Title
    filtered_df = filtered_df[["asin", "price", "in_stock", "total_sold", "listed_date", "Title"]]
    # Display df
    st.dataframe(filtered_df)

    # Export df to csv
    export_df(filtered_df)
    # Display graph
    plot_inventory(filtered_df)


# Display df when Past 21 is selected
if days == "Past 21":
    st.title("Past 21 Days")
    st.text("*Data updates every Monday")
    search = st.text_input("Search")
    # Filter the data based on the SKU or title entered based on partial match
    if search:
        search = search.lower()
        filtered_df = past21[(past21.index.str.lower().str.contains(search, na=False)) | 
                            (past21['Title'].str.lower().str.contains(search, na=False))]
    else:
        filtered_df = past21
    filtered_df = filtered_df.sort_values(by="total_sold", ascending=False)
    # Reorder the columns to display sku, asin, price, in_stock, total_sold, listed_date, Title
    filtered_df = filtered_df[["asin", "price", "in_stock", "total_sold", "listed_date", "Title"]]
    # Display df
    st.dataframe(filtered_df)

    # Export df to csv
    export_df(filtered_df)
    # Display graph
    plot_inventory(filtered_df)


# Display df when Past 30 is selected
if days == "Past 30":
    st.title("Past 30 Days")
    st.text("*Data updates every Monday")
    search = st.text_input("Search")
    # Filter the data based on the SKU or title entered based on partial match
    if search:
        search = search.lower()
        filtered_df = past30[(past30.index.str.lower().str.contains(search, na=False)) | 
                            (past30['Title'].str.lower().str.contains(search, na=False))]
    else:
        filtered_df = past30
    filtered_df = filtered_df.sort_values(by="total_sold", ascending=False)
    # Reorder the columns to display sku, asin, price, in_stock, total_sold, listed_date, Title
    filtered_df = filtered_df[["asin", "price", "in_stock", "total_sold", "listed_date", "Title"]]
    # Display df
    st.dataframe(filtered_df)

    # Export df to csv
    export_df(filtered_df)
    # Display graph
    plot_inventory(filtered_df)



