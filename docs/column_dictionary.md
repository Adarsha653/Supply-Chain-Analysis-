# DataCo Supply Chain Dataset — Column Dictionary

**File:** `Dataset/DataCoSupplyChainDataset.csv`  
**Rows:** ~180,519 order line items  
**Date range:** 2015 – 2018  
**Encoding:** `latin-1` (required when loading in Python)

Each row = **one order line item** (one product within one order).

---

## Quick reference by group

| Group | Columns |
|-------|---------|
| Payment | `Type` |
| Shipping & delivery | `Days for shipping (real)`, `Days for shipment (scheduled)`, `Delivery Status`, `Late_delivery_risk`, `shipping date (DateOrders)`, `Shipping Mode` |
| Financial | `Sales`, `Order Item Total`, `Order Profit Per Order`, `Benefit per order`, `Sales per customer`, `Order Item Discount`, `Order Item Discount Rate`, `Order Item Profit Ratio` |
| Product | `Product Name`, `Product Price`, `Order Item Product Price`, `Order Item Quantity`, `Product Card Id`, `Product Category Id`, `Category Id`, `Category Name`, `Department Id`, `Department Name`, `Product Description`, `Product Image`, `Product Status`, `Order Item Cardprod Id` |
| Customer | `Customer Id`, `Customer Fname`, `Customer Lname`, `Customer Email`, `Customer Password`, `Customer Segment`, `Customer City`, `Customer State`, `Customer Country`, `Customer Street`, `Customer Zipcode` |
| Order | `Order Id`, `Order Item Id`, `Order Customer Id`, `order date (DateOrders)`, `Order Status` |
| Geography | `Market`, `Order Region`, `Order Country`, `Order State`, `Order City`, `Order Zipcode`, `Latitude`, `Longitude` |

---

## Payment

### `Type`
**Payment method** — how the customer paid for the order.

| Value | Meaning |
|-------|---------|
| `DEBIT` | Debit card — funds taken directly from the customer's bank account. Usually `COMPLETE` orders. |
| `CASH` | Cash payment. In this dataset, all cash orders are `CLOSED`. |
| `TRANSFER` | Bank transfer — customer sends money bank-to-bank. Often `PENDING` or `PROCESSING`. |
| `PAYMENT` | Generic electronic/card payment. Often `PENDING_PAYMENT` or `PAYMENT_REVIEW`. |

**Example:** `DEBIT`  
**Use in analytics:** Relate payment type to order completion, fraud, and late delivery.

---

## Shipping & delivery

### `Days for shipping (real)`
Actual number of days from order to delivery.

**Example:** `3`  
**Use:** Compare against scheduled days to measure delays.

### `Days for shipment (scheduled)`
Promised or planned number of days for shipment/delivery.

**Example:** `4`  
**Use:** `real - scheduled` = delay in days.

### `Delivery Status`
Outcome of the delivery process.

| Value | Meaning |
|-------|---------|
| `Late delivery` | Order arrived later than expected |
| `Shipping on time` | Delivered within expected window |
| `Advance shipping` | Shipped earlier than expected |
| `Shipping canceled` | Shipment was canceled |

**Example:** `Advance shipping`

### `Late_delivery_risk`
Binary flag predicting or recording late delivery risk.

| Value | Meaning |
|-------|---------|
| `1` | Late delivery risk flagged |
| `0` | No late delivery risk |

**Example:** `0`  
**Use:** Key KPI — ~55% of rows are flagged `1` in this dataset.

### `shipping date (DateOrders)`
Date and time when the order was shipped.

**Example:** `2/3/2018 22:56`  
**Format:** `M/D/YYYY H:MM`

### `Shipping Mode`
Speed tier selected for delivery.

| Value | Meaning |
|-------|---------|
| `Standard Class` | Standard shipping (slowest, cheapest) |
| `Second Class` | Medium speed |
| `First Class` | Fast shipping |
| `Same Day` | Same-day delivery |

**Example:** `Standard Class`  
**Use:** Compare late delivery rate by shipping mode.

---

## Financial / sales

### `Sales`
Revenue amount for this order line item (in dollars).

**Example:** `327.75`

### `Order Item Total`
Total amount for the line after discounts are applied.

**Example:** `314.64`

### `Order Profit Per Order`
Profit earned on this order line. Can be **negative** (loss-making orders).

**Example:** `91.25` or `-249.09`  
**Use:** Profitability analysis by market, product, customer.

### `Benefit per order`
Benefit or margin metric associated with the order.

**Example:** `91.25`

### `Sales per customer`
Sales amount attributed to the customer for this order context.

**Example:** `314.64`  
**Use:** Customer-level revenue analysis.

### `Order Item Discount`
Discount amount in dollars applied to this line item.

**Example:** `13.11`

### `Order Item Discount Rate`
Discount as a decimal fraction (`0.04` = 4% off).

**Example:** `0.04`

### `Order Item Profit Ratio`
Profit margin ratio for the line item (`0.29` ≈ 29% margin).

**Example:** `0.29`

---

## Product

### `Product Name`
Name of the product sold.

**Example:** `Smart watch`

### `Product Price`
List price of the product.

**Example:** `327.75`

### `Order Item Product Price`
Price charged for this product on this specific order line.

**Example:** `327.75`

### `Order Item Quantity`
Number of units ordered for this line item.

**Example:** `1`

### `Product Card Id`
Unique identifier for the product in the catalog.

**Example:** `1360`

### `Product Category Id`
Numeric ID for the product's category.

**Example:** `73`

### `Category Id`
Category identifier (matches `Product Category Id` in most rows).

**Example:** `73`

### `Category Name`
Human-readable product category.

**Example:** `Sporting Goods`  
**Other values:** `Apparel`, `Electronics`, etc.

### `Department Id`
Numeric ID for the store department.

**Example:** `2`

### `Department Name`
Store department the product belongs to.

**Example:** `Fitness`  
**Top departments:** Fan Shop, Apparel, Golf, Footwear, Outdoors, Fitness

### `Product Description`
Text description of the product. **Always null/empty** in this dataset — safe to ignore.

### `Product Image`
URL to the product image.

**Example:** `http://images.acmesports.sports/Smart+watch`

### `Product Status`
Product availability or active status flag.

**Example:** `0`

### `Order Item Cardprod Id`
Product card ID linked to this specific order line.

**Example:** `1360`

---

## Customer (CRM)

### `Customer Id`
Unique identifier for the customer.

**Example:** `20755`  
**Use:** Customer 360, RFM, at-risk customer analysis.

### `Customer Fname`
Customer first name.

**Example:** `Cally`

### `Customer Lname`
Customer last name. A few null values exist.

**Example:** `Holloway`

### `Customer Email`
Customer email address. **Masked** (`XXXXXXXXX`) in this dataset — column is retained in full pipeline.

### `Customer Password`
Customer password. **Masked** (`XXXXXXXXX`) in this dataset — column is retained in full pipeline.

### `Customer Segment`
Customer business segment.

| Value | Meaning |
|-------|---------|
| `Consumer` | Individual / retail customer |
| `Corporate` | Business customer |
| `Home Office` | Small office / home business |

**Example:** `Consumer`

### `Customer City`
City where the customer is located.

**Example:** `Caguas`

### `Customer State`
State or region of the customer.

**Example:** `PR` (Puerto Rico), `CA` (California)

### `Customer Country`
Country where the customer is located.

**Example:** `Puerto Rico`, `EE. UU.` (USA)

### `Customer Street`
Customer street address.

**Example:** `5365 Noble Nectar Island`

### `Customer Zipcode`
Customer postal/ZIP code. A few null values.

**Example:** `725`

---

## Order details

### `Order Id`
Unique identifier for the entire order (one order can have multiple line items).

**Example:** `77202`

### `Order Item Id`
Unique identifier for this specific line item within an order.

**Example:** `180517`  
**Use:** Primary key at line-item grain.

### `Order Customer Id`
Customer ID associated with this order (usually matches `Customer Id`).

**Example:** `20755`

### `order date (DateOrders)`
Date and time when the order was placed.

**Example:** `1/31/2018 22:56`  
**Format:** `M/D/YYYY H:MM`

### `Order Status`
Current lifecycle status of the order.

| Value | Meaning |
|-------|---------|
| `COMPLETE` | Order fulfilled successfully |
| `CLOSED` | Order closed (often cash sales) |
| `PENDING` | Awaiting processing |
| `PROCESSING` | Currently being processed |
| `PENDING_PAYMENT` | Waiting for payment |
| `PAYMENT_REVIEW` | Payment under review |
| `CANCELED` | Order canceled |
| `SUSPECTED_FRAUD` | Flagged as potential fraud |
| `ON_HOLD` | Order on hold |

**Example:** `COMPLETE`  
**Use:** Filter completed orders for delivery analysis; flag `SUSPECTED_FRAUD` for CRM alerts.

---

## Geography (fulfillment / market)

### `Market`
High-level business market region.

| Value | Approx. share |
|-------|----------------|
| `LATAM` | Latin America |
| `Europe` | Europe |
| `Pacific Asia` | Asia-Pacific |
| `USCA` | US & Canada |
| `Africa` | Africa |

**Example:** `Pacific Asia`

### `Order Region`
Sub-region for order fulfillment.

**Example:** `Southeast Asia`, `South Asia`, `Eastern Asia`

### `Order Country`
Country associated with the order fulfillment path.

**Example:** `Indonesia`

### `Order State`
State or province for the order.

**Example:** `Java Occidental`

### `Order City`
City associated with the order.

**Example:** `Bekasi`

### `Order Zipcode`
Postal code for the order. **Mostly null** (~86% missing) — limited use.

### `Latitude`
Geographic latitude for mapping.

**Example:** `18.2514534`  
**Use:** Power BI map visuals.

### `Longitude`
Geographic longitude for mapping.

**Example:** `-66.03705597`  
**Use:** Power BI map visuals.

> **Note:** Customer location (e.g. Puerto Rico) often differs from order fulfillment location (e.g. Indonesia) — this reflects a global supply chain model.

---

## Data handling note

This project **keeps all 53 columns** end-to-end (website, MongoDB, Excel, Databricks).

| Column | Note |
|--------|------|
| `Customer Email` | Masked as `XXXXXXXXX` in source data |
| `Customer Password` | Masked as `XXXXXXXXX` in source data |
| `Product Description` | Empty in source data but column is retained |

For a real production system you would typically exclude raw credentials from analytics stores. Here they are kept for a complete dataset replica.

---

## Key columns for this project

| Analysis | Recommended columns |
|----------|---------------------|
| Late delivery KPI | `Late_delivery_risk`, `Delivery Status`, `Days for shipping (real)`, `Days for shipment (scheduled)`, `Shipping Mode` |
| Profitability | `Sales`, `Order Profit Per Order`, `Order Item Discount Rate`, `Department Name` |
| Geography | `Market`, `Order Region`, `Latitude`, `Longitude` |
| Customer / CRM | `Customer Id`, `Customer Segment`, `Sales per customer`, `Late_delivery_risk` |
| Fraud / risk alerts | `Order Status`, `Late_delivery_risk` |
| Time series | `order date (DateOrders)`, `shipping date (DateOrders)` |

---

## Grain & relationships

```
Customer (Customer Id)
    └── Order (Order Id)          ← one customer, many orders
            └── Order Line Item (Order Item Id)   ← one order, many line items
                    └── Product (Product Card Id / Product Name)
```

**Analytics grain used in this project:** one row per `Order Item Id` (line item level).

---

*Last updated: project Day 2 — Supply Chain Analysis*
