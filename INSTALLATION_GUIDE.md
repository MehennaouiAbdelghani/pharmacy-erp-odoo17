# Quick Installation Guide
## Pharmacy Management System - Odoo 17

**Author:** Abdelghani Mehennaoui

---

## 📦 Modules Created

All 7 modules have been successfully created in: `c:\odoo17\my_addons\`

```
✅ pharmacy_core          - Base configuration & master data
✅ pharmacy_stock_lot     - Lot tracking & expiry management
✅ pharmacy_purchase      - Controlled purchasing
✅ pharmacy_sales         - Sales with auto-FIFO
✅ pharmacy_pos           - POS integration
✅ pharmacy_alerts        - Automated notifications
✅ pharmacy_reports       - Business reports
```

---

## 🚀 Installation Steps

### Step 1: Restart Odoo Server
```powershell
# If Odoo is running as a service, restart it
# Or restart from Odoo UI
```

### Step 2: Update Apps List
1. Go to **Apps** (Main Menu)
2. Click **Update Apps List** (top-right menu)
3. Confirm update

### Step 3: Install Modules (STRICT ORDER!)

**⚠️ CRITICAL: Install in this exact sequence!**

1. **pharmacy_core**
   - Search "Pharmacy Core"
   - Click "Install"
   - Wait for completion

2. **pharmacy_stock_lot**
   - Search "Pharmacy Stock Lot"
   - Click "Install"
   - Wait for completion

3. **pharmacy_purchase**
   - Search "Pharmacy Purchase"
   - Click "Install"
   - Wait for completion

4. **pharmacy_sales**
   - Search "Pharmacy Sales"
   - Click "Install"
   - Wait for completion

5. **pharmacy_pos** (Optional - if using POS)
   - Search "Pharmacy POS"
   - Click "Install"
   - Wait for completion

6. **pharmacy_alerts**
   - Search "Pharmacy Alerts"
   - Click "Install"
   - Wait for completion

7. **pharmacy_reports**
   - Search "Pharmacy Reports"
   - Click "Install"
   - Wait for completion

---

## ✅ Post-Installation Configuration

### 1. Assign User to Pharmacy Admin Group
1. **Settings** > **Users & Companies** > **Users**
2. Select your user
3. Go to **Permissions** tab
4. Find **Pharmacy** section
5. Check **Pharmacy Administrator**
6. Save

### 2. Create First Drug Category
1. **Pharmacy** menu (should appear in main menu)
2. **Configuration** > **Drug Categories**
3. Click **Create**
4. Enter name (e.g., "Analgesics")
5. Save

### 3. Create First Drug Product
1. **Pharmacy** > **Products** > **All Products**
2. Click **Create**
3. Enable **"Is a Drug"** toggle
4. Fill required fields:
   - Name
   - Drug Type (OTC/Prescription/Narcotic)
   - Scientific Name
   - Category
   - Minimum Quantity
5. Note: Tracking is auto-set to "By Lots" (mandatory)
6. Save

### 4. Verify Cron Jobs Are Active
1. **Settings** > **Technical** > **Automation** > **Scheduled Actions**
2. Search "Pharmacy"
3. Verify these are active:
   - ✅ Pharmacy: Daily Expiry Alert
   - ✅ Pharmacy: Daily Low Stock Alert
   - ✅ Pharmacy: Monthly Dead Stock Detection

---

## 📚 Documentation Files

- **Master Documentation:** `PHARMACY_SYSTEM_DOCUMENTATION.md`
- **Module READMEs:** Each module has a `README.md`
- **Module Summaries:** Each module has a `SUMMARY.md`

---

## 🔑 Key Features

### ✅ Automatic FIFO
- All drugs automatically use FIFO (First In, First Out)
- Nearest expiry date sold first
- Cannot be overridden

### ✅ Expiry Protection
- Cannot sell expired products
- System blocks automatically
- Daily alerts at 02:00

### ✅ Lot Tracking
- Mandatory for all drugs
- Traceability guaranteed
- Expiry date required

### ✅ Profit Tracking
- Real-time profit calculation
- Per-product analysis
- Margin percentages

### ✅ Automated Alerts
- Expiry warnings (180 days default)
- Low stock notifications
- Dead stock detection (180 days no sales)

---

## 🎯 Quick Start Workflow

### Scenario: Receive and Sell a Drug

**1. Create Purchase Order**
- Purchases > Purchase Orders > Create
- Add drug product
- Confirm order

**2. Receive Products**
- Receive shipment
- **IMPORTANT:** Assign lot number and expiry date
- Validate receipt

**3. Sell Product**
- Sales > Sales Orders > Create
- Add drug product
- System auto-selects lot with nearest expiry
- Confirm sale

**4. View Profit**
- Admin can see profit on sale order line
- Real-time calculation

---

## 🛡️ Safety Features

| Feature | Protection |
|---------|-----------|
| Expired Products | ❌ Cannot be sold (blocked) |
| Negative Stock | ❌ Cannot oversell |
| Missing Lot | ❌ Cannot receive without lot |
| Missing Expiry | ❌ Cannot receive without expiry |
| Wrong FIFO | ✅ Auto-corrected by system |

---

## 📞 Access Levels

### Administrator (Pharmacist Owner)
- ✅ Full access to everything
- ✅ Financial reports
- ✅ Configuration

### Sales Staff
- ✅ Create sales
- ✅ Use POS
- ❌ No price modification
- ❌ No purchasing

### Stock Manager
- ✅ Create purchases
- ✅ Receive goods
- ✅ Inventory adjustments
- ❌ No sales
- ❌ No financial reports

---

## 🌍 Languages

All modules support:
- 🇬🇧 English
- 🇫🇷 French
- 🇸🇦 Arabic

To load translations:
1. Settings > Translations > Load a Translation
2. Select language
3. Click Load

---

## ⚠️ Important Notes

1. **Installation Order is MANDATORY**
   - Must follow sequence 1-7
   - Skipping or reordering will cause errors

2. **Cannot Disable Lot Tracking**
   - Lot tracking is permanent for drugs
   - By design for safety

3. **Cannot Sell Expired Products**
   - This is intentional
   - Cannot be overridden
   - Regulatory compliance

4. **FIFO is Automatic**
   - System manages lot selection
   - Oldest expiry sold first
   - Transparent to user

---

## 🐛 Troubleshooting

### Module Not Appearing
- Restart Odoo server
- Update Apps List
- Clear browser cache

### Cannot Install
- Check dependencies are installed
- Follow installation order
- Check Odoo logs

### Pharmacy Menu Not Visible
- Assign user to pharmacy group
- Refresh browser
- Log out and log back in

---

## 📊 Reports Available

After installing all modules, access via:
**Pharmacy > Reports > Generate Reports**

1. **Expired Drugs Loss** - Track financial impact of expiry
2. **Profit per Product** - Analyze profitability
3. **Stock Valuation** - Current inventory value

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Pharmacy menu appears in main menu
- [ ] Can create drug categories
- [ ] Can create products marked as drugs
- [ ] Lot tracking auto-enabled for drugs
- [ ] Can create purchase order with drugs
- [ ] Lot & expiry mandatory on receipt
- [ ] Can create sales order with drugs
- [ ] Profit visible on sale lines (admin)
- [ ] Cron jobs are active
- [ ] Reports accessible

---

## 🎉 Success!

If all checks pass, your Pharmacy Management System is ready to use!

**Next Steps:**
1. Import your existing product catalog
2. Set up drug categories
3. Configure minimum quantities
4. Train staff on workflow
5. Start operations!

---

**Author:** Abdelghani Mehennaoui  
**Version:** 17.0.1.0.0  
**Date:** 2026-01-25

**© 2026 Abdelghani Mehennaoui. All rights reserved.**
