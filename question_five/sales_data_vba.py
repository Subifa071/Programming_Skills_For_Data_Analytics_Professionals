# STEP 1: CREATE EXCEL DATA FILE
import pandas as pd
import numpy as np
import random
from datetime import datetime

print("=" * 70)
print("CREATING EXCEL FILE FOR QUESTION 5")
print("=" * 70)

# Set random seed for consistent results
np.random.seed(42)

# Create 25 products
data = []
categories = ['Electronics', 'Furniture', 'Apparel', 'Food', 'Stationery']
regions = ['Asia', 'Europe', 'Africa', 'North America', 'South America']

for i in range(25):
    category = categories[i // 5]  # 5 products per category
    region = regions[i % 5]        # Distribute across regions
    
    product_name = f"{category[:3]}_Prod{(i % 5) + 1:02d}"
    units_sold = random.randint(50, 800)
    unit_price = round(random.uniform(20, 150), 2)
    manufacturing_cost = round(random.uniform(5, 100), 2)
    
    data.append({
        'Product': product_name,
        'Category': category,
        'Region': region,
        'Units Sold': units_sold,
        'Unit Price (£)': unit_price,
        'Manufacturing Cost (£)': manufacturing_cost,
        'Revenue (£)': '',  # Will calculate in Excel
        'Discount (£)': '', # Will calculate in Excel  
        'Profit (£)': ''    # Will calculate in Excel
    })

# Create DataFrame
df = pd.DataFrame(data)

# Show what we created
print("\n✓ Created 25 products:")
print(f"  - 5 categories: {', '.join(categories)}")
print(f"  - 5 regions: {', '.join(regions)}")
print(f"  - Each category has 5 products")

print("\n✓ Sample data (first 5 products):")
print("-" * 80)
for i in range(5):
    p = data[i]
    print(f"{p['Product']:12} | {p['Category']:12} | {p['Region']:15} | "
        f"{p['Units Sold']:4} units | £{p['Unit Price (£)']:7.2f} | £{p['Manufacturing Cost (£)']:7.2f}")

print("\n✓ Business Rule:")
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
Code for Excel (Macro Execution)

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