import streamlit as st
import pandas as pd
import os

# File to store the inventory
data_file = "inventory.csv"

# Initialize inventory if file doesn't exist
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Item Name", "Quantity", "Max Quantity", "Threshold"])
    df.to_csv(data_file, index=False)

# Load inventory
df = pd.read_csv(data_file)

# Sidebar Navigation
page = st.sidebar.selectbox("Select Page", ["Inventory", "Grocery List"])

if page == "Inventory":
    st.title("🗃️ Food Storage Inventory")

    st.subheader("Add or Update an Item")
    name = st.text_input("Item Name")
    quantity = st.number_input("Current Quantity", min_value=0, value=0)
    max_quantity = st.number_input("Max Quantity", min_value=1, value=1)
    threshold = st.number_input("Threshold", min_value=0, value=0)

    if st.button("Add / Update Item"):
        if name.strip():
            df = df[df['Item Name'] != name]  # Remove duplicates
            df = df.append({
                "Item Name": name,
                "Quantity": quantity,
                "Max Quantity": max_quantity,
                "Threshold": threshold
            }, ignore_index=True)
            df.to_csv(data_file, index=False)
            st.success(f"'{name}' has been added/updated!")
        else:
            st.error("Please enter an item name.")

    st.subheader("Current Inventory")
    st.table(df)

elif page == "Grocery List":
    st.title("🛒 Grocery List")

    if df.empty:
        st.info("Inventory is empty. Add items on the Inventory page.")
    else:
        grocery_items = []
        for _, row in df.iterrows():
            if row['Quantity'] <= row['Threshold']:
                to_buy = row['Max Quantity'] - row['Quantity']
                grocery_items.append(f"- {row['Item Name']}: Buy {to_buy} (Current: {int(row['Quantity'])} / Max: {int(row['Max Quantity'])})")

        if grocery_items:
            st.write("### Items to Restock:")
            for item in grocery_items:
                st.write(item)
        else:
            st.success("✅ All stocked up!")
