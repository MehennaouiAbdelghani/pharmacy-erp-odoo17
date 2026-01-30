# Pharmacy Sales Management

**Author:** Abdelghani Mehennaoui  
**Version:** 17.0.1.0.0

## Features

- **Auto-Lot Selection:** Automatically selects lot with nearest expiry (FIFO)
- **Negative Stock Prevention:** Cannot sell more than available quantity
- **Profit Tracking:** Per-line and total profit calculation
- **Margin Analysis:** Profit margin percentage tracking

## Installation

Requires: `pharmacy_core`, `pharmacy_stock_lot`, `sale_management`, `sale_stock`

Install as #4 in sequence

## Key Features

🔄 **Automatic FIFO:** System auto-selects lots with nearest expiry  
🚫 **Stock Validation:** Cannot oversell pharmaceutical products  
💰 **Profit Tracking:** Real-time cost vs. sale price analysis  
🔒 **Mandatory Lot Linking:** All sales linked to specific lots

## Workflow

1. Create sale order with drug product
2. System checks stock availability
3. On confirmation, auto-assigns lot with nearest expiry
4. Profit calculated automatically
5. Cannot process if stock insufficient or lot expired

**© 2026 Abdelghani Mehennaoui**
