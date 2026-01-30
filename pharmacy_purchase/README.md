# Pharmacy Purchase Management

**Author:** Abdelghani Mehennaoui  
**Version:** 17.0.1.0.0

## Features

- Mandatory lot number on pharmaceutical receipt
- Mandatory expiry date on all drug lots
- Validation blocking without required data
- Visual indicators for drug-containing purchase orders

## Installation

Requires: `pharmacy_core`, `pharmacy_stock_lot`, `purchase`

Install as #3 in sequence

## Key Validations

✅ **Receipt Validation:** Cannot validate incoming shipment without:
  - Lot number for each drug product
  - Expiry date for each lot

🔒 **Purchase Control:** Stock manager only (no sales staff access)

**© 2026 Abdelghani Mehennaoui**
