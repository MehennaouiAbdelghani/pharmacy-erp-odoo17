# Pharmacy Stock Lot Management

**Author:** Abdelghani Mehennaoui  
**Version:** 17.0.1.0.0

## Features

- **Expiry Date Tracking:** Automatic expiry detection for all pharmaceutical lots
- **FIFO Enforcement:** First In, First Out strategy mandatory for all drugs
- **Alert Management:** Configurable alert thresholds (default: 180 days)
- **Expired Lot Blocking:** Cannot sell or transfer expired products
- **Visual Indicators:** Color-coded alert status (OK/Warning/Expired)

## Installation

Requires: `pharmacy_core`, `stock`

Install after pharmacy_core (#2 in sequence)

## Key Constraints

1. ✅ **Expiry Date Mandatory:** All drug lots must have expiration date
2. 🚫 **Expired Lots Blocked:** Cannot process moves with expired lots
3. 🔄 **FIFO Auto-Enabled:** Removal strategy automatically set to FIFO
4. 🔒 **FIFO Protected:** Cannot change from FIFO for drug categories

## Usage

### View Lots by Expiry Status
**Pharmacy > Lots & Expiry > All Lots**

Filters available:
- Expired
- Near Expiry
- OK

### Alert Status Colors
- 🟢 **Green (OK):** More than threshold days remaining
- 🟡 **Yellow (Warning):** Within alert threshold
- 🔴 **Red (Expired):** Past expiration date

## Technical Details

### Models Extended
- `stock.lot`: Expiry tracking, alert status
- `stock.move.line`: Expiry validation, blocking logic
- `product.template`: FIFO enforcement

### Performance Optimizations
- Indexed fields: `expired`, `is_drug_lot`
- Stored computed fields for faster filtering
- Database-level constraints for data integrity

**© 2026 Abdelghani Mehennaoui**
