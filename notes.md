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


    # Display graph
    plot_inventory(filtered_df)