import streamlit as st
import pandas as pd
import os

# CSV file for saving data
DATA_FILE = 'inventory.csv'

# Load inventory from CSV
def load_inventory():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=['Item Name', 'Quantity', 'Max Quantity', 'Item Type'])

# Save inventory to CSV
def save_inventory(df):
    df.to_csv(DATA_FILE, index=False)

# Add a new item
def add_item(item_name, quantity, max_quantity, item_type):
    df = load_inventory()
    new_item = pd.DataFrame([{
        'Item Name': item_name,
        'Quantity': quantity,
        'Max Quantity': max_quantity,
        'Item Type': item_type
    }])
    df = pd.concat([df, new_item], ignore_index=True)
    save_inventory(df)

# Generate grocery list
def generate_grocery_list(df):
    grocery_list = df[df['Quantity'] < df['Max Quantity']].copy()
    grocery_list['Need to Buy'] = grocery_list['Max Quantity'] - grocery_list['Quantity']
    return grocery_list[['Item Name', 'Item Type', 'Quantity', 'Max Quantity', 'Need to Buy']]

# Streamlit UI
st.title("🧃 Food Storage Tracker")

menu = st.sidebar.radio("Navigate", ["Inventory", "Grocery List"])

if menu == "Inventory":
    st.header("📋 Current Inventory")

    df = load_inventory()
    st.dataframe(df)

    st.subheader("➕ Add New Item")

    item_name = st.text_input("Item Name")
    quantity = st.number_input("Current Quantity", min_value=0, step=1)
    max_quantity = st.number_input("Max Quantity", min_value=1, step=1)

    item_type = st.selectbox("Item Type", [
        "Can", "Package", "Bottle", "Jar", "Bag", "Frozen", "Tub", "Loose/Bulk"
    ])

    if st.button("Add Item"):
        if item_name.strip() != "":
            add_item(item_name.strip(), quantity, max_quantity, item_type)
            st.success(f"Added {item_name} ({item_type}) to inventory!")
        else:
            st.error("Please enter an item name.")

elif menu == "Grocery List":
    st.header("🛒 Grocery List")

    df = load_inventory()
    grocery_list = generate_grocery_list(df)

    if grocery_list.empty:
        st.success("Your stock is full — no need to buy anything! ✅")
    else:
        st.table(grocery_list)

