import pandas as pd
import numpy as np
import random # Python's built-in random number generator

print("=" * 70)
print("CREATING EXCEL FILE FOR VBA")
print("=" * 70)

# Fix the random seed so results are reproducible every run
np.random.seed(42)

# Generate mock sales data for 25 products across 5 categories and 5 regions.
# This dataset is intended for export to Excel, where additional calculations
# (Revenue, Discount, Profit) will be handled by VBA.
data = [] 
categories = ['Electronics', 'Furniture', 'Apparel', 'Food', 'Stationery']
regions = ['Asia', 'Europe', 'Africa', 'North America', 'South America']

for i in range(25):
    # Assign each product to a category (5 products per category)
    category = categories[i // 5]  

    # Rotate regions to evenly distribute products among all 5 regions 
    region = regions[i % 5]        
    
    product_name = f"{category[:3]}_Prod{(i % 5) + 1:02d}" # Generate short product codes

    units_sold = random.randint(50, 800) # Randomly assign units sold
    unit_price = round(random.uniform(20, 150), 2) # Random unit price between £20 and £150
    manufacturing_cost = round(random.uniform(5, 100), 2) # Random manufacturing cost between £5 and £100
    
    data.append({
        'Product': product_name,
        'Category': category,
        'Region': region,
        'Units Sold': units_sold,
        'Unit Price (£)': unit_price,
        'Manufacturing Cost (£)': manufacturing_cost,
        'Revenue (£)': '',  # Placeholder: to be calculated in Excel
        'Discount (£)': '', # Placeholder: to be calculated in Excel
        'Profit (£)': ''    # Placeholder: to be calculated in Excel
    })

# Create a dataframe from the product data
df = pd.DataFrame(data)

# Summary printout of created data
print("\n Created 25 products:")
print(f"  - 5 categories: {', '.join(categories)}")
print(f"  - 5 regions: {', '.join(regions)}")
print(f"  - Each category has 5 products")

print("\n Sample data (first 5 products):")
print("-" * 80)
for i in range(5):
    p = data[i]
    print(f"{p['Product']:12} | {p['Category']:12} | {p['Region']:15} | "
        f"{p['Units Sold']:4} units | £{p['Unit Price (£)']:7.2f} | £{p['Manufacturing Cost (£)']:7.2f}")

print("\n Business Rule:")
print("  - Discount: 10% of Revenue if Units Sold > 400")
print(f"  - Products qualifying for discount: {sum([1 for d in data if d['Units Sold'] > 400])}")

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. Copy this data into Excel (see table below)")
print("2. Save Excel file as 'Sales_Report.xlsx'")
print("3. Follow Step 2 instructions for VBA code")

print("\n" + "=" * 70)
print("COMPLETE DATA TABLE (copy this to Excel):")
print("=" * 70)
print("Product|Category|Region|Units Sold|Unit Price (£)|Manufacturing Cost (£)|Revenue (£)|Discount (£)|Profit (£)")
print("-" * 100)

for item in data:
    print(f"{item['Product']}|{item['Category']}|{item['Region']}|"
        f"{item['Units Sold']}|{item['Unit Price (£)']}|{item['Manufacturing Cost (£)']}|||")

print("\n" + "=" * 70)
print("READY FOR EXCEL SETUP!")
print("=" * 70)

""" 
VBA Code for Excel (Macro Execution)

Sub Calculate_Sales_Report()

    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long

    Dim unitsSold As Double
    Dim unitPrice As Double
    Dim manufacturingCost As Double

    Dim revenue As Double
    Dim totalCost As Double
    Dim discount As Double
    Dim profit As Double

    Set ws = ThisWorkbook.Sheets(1)
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row

    For i = 2 To lastRow

        unitsSold = ws.Cells(i, 4).Value
        unitPrice = ws.Cells(i, 5).Value
        manufacturingCost = ws.Cells(i, 6).Value

        revenue = unitsSold * unitPrice
        totalCost = unitsSold * manufacturingCost

        If unitsSold > 400 Then
            discount = revenue * 0.1
        Else
            discount = 0
        End If

        profit = revenue - totalCost - discount

        ws.Cells(i, 7).Value = revenue
        ws.Cells(i, 8).Value = discount
        ws.Cells(i, 9).Value = profit

    Next i

    MsgBox "Sales report calculated successfully!"

End Sub

"""