# Pharmacy Core Module

![Pharmacy Core](static/description/icon.png)

## Overview

**Pharmacy Core** is the foundational module for the Pharmacy Management System (Mono-Pharmacie). It provides essential configuration and master data management capabilities for pharmaceutical operations.

**Author:** Abdelghani Mehennaoui  
**Version:** 17.0.1.0.0  
**License:** LGPL-3

---

## Features

### 🏥 Drug Category Management
- Hierarchical category structure for pharmaceutical products
- Parent-child relationships for organized classification
- Product count tracking per category
- Multi-language support (English, French, Arabic)

### 💊 Pharmaceutical Product Extensions
- **Drug Classification:**
  - Over The Counter (OTC)
  - Prescription Required
  - Narcotic/Controlled Substance
- **Product Information:**
  - Scientific/Generic name tracking
  - Pharmacy-specific categorization
  - Minimum stock quantity thresholds
- **Mandatory Lot Tracking:**
  - Automatic enforcement for all pharmaceutical products
  - Required for expiry date management
  - Cannot be disabled once set

### 👥 Role-Based Access Control
- **Pharmacy Administrator:** Full system access
- **Sales Staff:** Sales operations only, no price modifications
- **Stock Manager:** Purchases and inventory adjustments

---

## Installation

### Prerequisites
- Odoo 17.0 or higher
- Modules: `base`, `product`, `uom`

### Installation Steps

1. **Copy Module to Addons Directory:**
   ```bash
   cp -r pharmacy_core /path/to/odoo/addons/
   ```

2. **Update Apps List:**
   - Go to Apps menu
   - Click "Update Apps List"
   - Search for "Pharmacy Core"

3. **Install Module:**
   - Click "Install" button
   - Wait for installation to complete

4. **Configure Access Rights:**
   - Go to Settings > Users & Companies > Groups
   - Assign users to appropriate pharmacy groups

---

## Configuration

### 1. Create Drug Categories
Navigate to: **Pharmacy > Configuration > Drug Categories**

1. Click "Create"
2. Enter category name
3. (Optional) Select parent category for hierarchical organization
4. Save

### 2. Configure Pharmacy Products
Navigate to: **Pharmacy > Products > All Products**

1. Click "Create"
2. Enable "Is a Drug" toggle
3. Select Drug Type (mandatory):
   - OTC
   - Prescription
   - Narcotic
4. Enter scientific name
5. Select pharmacy category
6. Set minimum stock quantity
7. Note: Lot tracking is automatically enabled and cannot be disabled

---

## Usage Guide

### Managing Drug Categories

**Create Category:**
```
Pharmacy > Configuration > Drug Categories > Create
```

**Example Structure:**
```
Analgesics
├── NSAIDs
├── Opioids
└── Acetaminophen
```

### Adding Pharmaceutical Products

1. **Navigate:** Pharmacy > Products > All Products
2. **Create New Product**
3. **Enable Drug Toggle:** Turn on "Is a Drug"
4. **Fill Required Fields:**
   - Name: Commercial name
   - Drug Type: Select classification
   - Scientific Name: Generic name
   - Category: Select pharmacy category
5. **Set Stock Parameters:**
   - Minimum Quantity: Low stock threshold
   - Tracking: Automatically set to "By Lots" (read-only)

### Filtering Products

**Available Filters:**
- Drugs Only
- OTC Drugs
- Prescription Drugs
- Narcotics
- Low Stock (qty ≤ min_qty)

**Group By:**
- Pharmacy Category
- Drug Type

---

## Security

### Access Groups

| Group | Access Rights |
|-------|--------------|
| Pharmacy Administrator | Full CRUD on all pharmacy data |
| Sales Staff | Read-only on categories, sales operations |
| Stock Manager | Manage categories, no financial access |

### Data Constraints

1. **Drug Type Mandatory:** All pharmaceutical products must have a drug type
2. **Lot Tracking Enforced:** Cannot disable lot tracking for drugs
3. **Category Recursion Prevention:** No circular category relationships

---

## Technical Details

### Models

#### `pharmacy.drug.category`
- **Purpose:** Hierarchical drug classification
- **Key Features:**
  - Parent-store optimization for fast tree operations
  - Computed complete name with full path
  - Product count computation
  - Active/archive support

#### `product.template` (Inherited)
- **New Fields:**
  - `is_drug`: Boolean flag
  - `drug_type`: Selection (otc/prescription/narcotic)
  - `scientific_name`: Generic/scientific name
  - `pharmacy_category_id`: Link to drug category
  - `min_qty`: Minimum stock threshold
- **Constraints:**
  - Drug type required when is_drug=True
  - Lot tracking automatically enabled for drugs
  - Cannot disable tracking on drugs

### Performance Optimizations

1. **Database Indexes:**
   - `pharmacy_category_id` on product.template
   - `is_drug` on product.template
   - `name` and `complete_name` on drug categories
   - `parent_path` for hierarchical queries

2. **Parent Store:**
   - Hierarchical categories use `_parent_store` for O(1) tree operations

3. **Computed Fields:**
   - `complete_name` stored with dependencies
   - `product_count` computed on demand

---

## Troubleshooting

### Issue: Cannot Create Product Without Lot Tracking
**Solution:** This is expected behavior. All pharmaceutical products require lot tracking for expiry management. This constraint is mandatory and cannot be bypassed.

### Issue: Drug Type Field Not Showing
**Solution:** Ensure "Is a Drug" toggle is enabled. The pharmacy tab only appears for drug products.

### Issue: Category Not Deletable
**Solution:** Remove all products from the category first, or archive the category instead of deleting.

---

## Roadmap

This module is part of a complete pharmacy system:

1. ✅ **pharmacy_core** - Base configuration (Current)
2. ⏳ pharmacy_stock_lot - Lot & expiry management
3. ⏳ pharmacy_purchase - Controlled purchasing
4. ⏳ pharmacy_sales - Sales with auto-lot selection
5. ⏳ pharmacy_pos - POS integration
6. ⏳ pharmacy_alerts - Notifications & cron jobs
7. ⏳ pharmacy_reports - Business reports

---

## Support & Contribution

**Author:** Abdelghani Mehennaoui  
**Module:** pharmacy_core  
**Version:** 17.0.1.0.0

For issues, suggestions, or contributions, please contact the author.

---

## License

This module is licensed under LGPL-3.

---

**© 2026 Abdelghani Mehennaoui. All rights reserved.**
