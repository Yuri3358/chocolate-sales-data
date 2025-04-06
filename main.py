import pandas as pd

global_sales = pd.read_csv("chocolatesales.csv")
global_sales_df = pd.DataFrame(global_sales)
products = global_sales_df["Product"]
salesmen = global_sales_df["Sales Person"]
amount = global_sales_df["Amount"].str.replace("$", "").str.replace(",", "").astype(int)
unit_price = round(amount / global_sales_df["Boxes Shipped"], 2)

improved_data = pd.DataFrame({
    "product": products,
    "amount ($)": amount,
    "box shipped": global_sales_df["Boxes Shipped"],
    "price per box": unit_price

})

products_database = improved_data.groupby(["product"]).sum() #elementar dataframe 01

salesmen_data = pd.DataFrame({
    "salesman":salesmen,
    "amount": amount
})

salesmen_database = salesmen_data.groupby(["salesman"]).sum().sort_values(by="amount", ascending=False) #elementar dataframe 02
products_database.reset_index(inplace=True)
salesmen_database.reset_index(inplace=True)

most_shipped_product = products_database.where(products_database["box shipped"] == products_database["box shipped"].max()).dropna()
most_shipped_product["price per box"] = round(most_shipped_product["amount ($)"] / most_shipped_product["box shipped"], 2)
most_valuable_sale = products_database.where(products_database["amount ($)"] == products_database["amount ($)"].max()).dropna()
most_valuable_sale.reset_index(inplace=True)
best_salesman = salesmen_database

dashboard = pd.DataFrame({
    "best salesman": [best_salesman.loc[0, "salesman"]],
    "most shipped": [most_shipped_product.loc[0, "product"]],
    "best sale": [most_valuable_sale.loc[0, "product"]]
})


def show_data(datatype):
    match datatype:
        case "top":
            return dashboard
        case "salesmen":
            return salesmen_database
        case "products":
            return products_database