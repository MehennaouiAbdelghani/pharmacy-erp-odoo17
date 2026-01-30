# Pharmacy Alerts & Notifications

**Author:** Abdelghani Mehennaoui  
**Version:** 17.0.1.0.0

## Features

### Automated Cron Jobs

1. **Daily Expiry Alert (02:00)**
   - Checks all drug lots for near-expiry or expired status
   - Creates activities for pharmacy administrators
   - Alerts for both expired and warning-status lots

2. **Daily Low Stock Alert (02:05)**
   - Monitors stock levels vs. minimum quantity thresholds
   - Creates activities for stock managers  
   - Only alerts when qty ≤ min_qty

3. **Monthly Dead Stock Detection (1st day, 03:00)**
   - Identifies products with no sales in last 180 days
   - Creates activities for administrators
   - Helps identify slow-moving inventory

## Installation

Requires: `pharmacy_core`, `pharmacy_stock_lot`, `mail`

Install as #6 in sequence

## Alert Types

📅 **Expiry Alerts:** Products near expiration or expired  
📦 **Low Stock:** Products below minimum threshold  
💤 **Dead Stock:** No sales in 180 days

## Configuration

All cron jobs are active by default. To modify:
**Settings > Technical > Automation > Scheduled Actions**

**© 2026 Abdelghani Mehennaoui**
