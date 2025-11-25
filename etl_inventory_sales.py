import pandas as pd

def load_data():
    """Load inventory and sales CSV files into pandas DataFrames."""
    inventory = pd.read_csv("inventory.csv")
    sales = pd.read_csv("sales.csv")
    return inventory, sales

def clean_data(inventory, sales):
    """Basic cleaning: handle data types and missing values."""
    # Ensure numeric columns are correct types
    numeric_cols_inventory = ["unit_cost", "stock_on_hand", "reorder_level"]
    for col in numeric_cols_inventory:
        inventory[col] = pd.to_numeric(inventory[col], errors="coerce")

    numeric_cols_sales = ["quantity", "unit_price"]
    for col in numeric_cols_sales:
        sales[col] = pd.to_numeric(sales[col], errors="coerce")

    # Convert sale_date to datetime
    sales["sale_date"] = pd.to_datetime(sales["sale_date"], errors="coerce")

    # Drop rows with missing product_id or quantity in sales
    sales = sales.dropna(subset=["product_id", "quantity"])

    # Drop rows with missing product_id in inventory
    inventory = inventory.dropna(subset=["product_id"])

    return inventory, sales

def transform_data(inventory, sales):
    """Join inventory and sales, and create some useful metrics."""
    # Merge sales with inventory on product_id
    merged = sales.merge(inventory, on="product_id", how="left")

    # Calculate revenue and cost and profit
    merged["revenue"] = merged["quantity"] * merged["unit_price"]
    merged["cost"] = merged["quantity"] * merged["unit_cost"]
    merged["profit"] = merged["revenue"] - merged["cost"]

    return merged

def create_aggregations(merged):
    """Create simple summary tables that will be useful later in SQL/Tableau."""
    # Total sales by product
    sales_by_product = (
        merged.groupby(["product_id", "product_name"], as_index=False)
        .agg(
            total_quantity_sold=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
        )
    )

    # Low stock products (after sales)
    inventory_status = merged.groupby(
        ["product_id", "product_name", "stock_on_hand", "reorder_level"],
        as_index=False
    )["quantity"].sum()

    inventory_status.rename(columns={"quantity": "total_quantity_sold"}, inplace=True)

    # Estimated stock after all recorded sales
    inventory_status["estimated_stock_after_sales"] = (
        inventory_status["stock_on_hand"] - inventory_status["total_quantity_sold"]
    )

    return sales_by_product, inventory_status

def save_outputs(merged, sales_by_product, inventory_status):
    """Save cleaned and aggregated datasets to new CSV files."""
    merged.to_csv("clean_sales_inventory.csv", index=False)
    sales_by_product.to_csv("agg_sales_by_product.csv", index=False)
    inventory_status.to_csv("inventory_status.csv", index=False)
    print("✅ Files saved:")
    print(" - clean_sales_inventory.csv")
    print(" - agg_sales_by_product.csv")
    print(" - inventory_status.csv")

def main():
    inventory, sales = load_data()
    inventory, sales = clean_data(inventory, sales)
    merged = transform_data(inventory, sales)
    sales_by_product, inventory_status = create_aggregations(merged)
    save_outputs(merged, sales_by_product, inventory_status)

if __name__ == "__main__":
    main()
