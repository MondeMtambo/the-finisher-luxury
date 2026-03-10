# 👥 Admin User Management Guide - THE FINISHER LUXURY

## Overview
Comprehensive admin dashboard to monitor all users, track IP addresses, manage payments, and ban non-paying or abusive users.

---

## 🚀 Accessing User Management

### Navigate to Admin Console:
1. Login as admin/superuser
2. Go to **Admin Console** (navbar)
3. Click **"👥 Users"** tab at the top

---

## 📊 Dashboard Overview

### Summary Cards:
```
┌─────────────┬─────────────┬─────────────┐
│ Total Users │ Active      │ Trial       │
│     15      │     12      │      8      │
└─────────────┴─────────────┴─────────────┘
┌─────────────┬─────────────┬─────────────┐
│ Paid        │ Overdue     │ Banned      │
│      4      │      2      │      1      │
└─────────────┴─────────────┴─────────────┘
```

### What Each Means:
- **Total Users**: All registered accounts
- **Active**: Users who can access (not banned, payment valid)
- **Trial**: Users in 14-day trial period
- **Paid**: Users with active paid subscriptions
- **Overdue**: Users with overdue payments (consider banning)
- **Banned**: Users blocked from access

---

## 👤 User Table Columns

| Column | Description |
|--------|-------------|
| **User** | Full name, username, admin/staff badges |
| **Email** | User's email address |
| **Company** | Business name (if provided) |
| **Joined** | Registration date |
| **Registration IP** | IP address used during signup |
| **Last Login IP** | Most recent login IP address |
| **Payment** | Payment status (Pending/Trial/Paid/Overdue) |
| **Status** | Active/Inactive/Banned |
| **Activity** | Total items created (contacts + companies + deals) |
| **Actions** | Ban/Unban/Payment buttons |

---

## 🚫 Banning Users

### When to Ban:
1. **Unpaid subscription** - Trial ended, no payment
2. **Payment overdue** - Multiple missed payments
3. **Terms violation** - Breaking ToS
4. **Fraudulent activity** - Suspected fraud
5. **Platform abuse** - Excessive usage or abuse

### How to Ban:
1. Find user in table
2. Click **"🚫 Ban"** button
3. Select reason from dropdown:
   - Unpaid subscription
   - Payment overdue
   - Terms of service violation
   - Fraudulent activity
   - Abuse of platform
   - Other (custom reason)
4. Click **"Confirm Ban"**

### What Happens When Banned:
- ✅ User immediately logged out
- ✅ Account marked as inactive
- ✅ Login attempts blocked with ban message
- ✅ All access denied
- ✅ Ban reason stored in database
- ✅ IP addresses preserved for tracking

### Ban Message User Sees:
```
🚫 Account Banned

Your account has been banned.
Reason: Unpaid subscription

Contact: support@thefinisher.co.za
```

---

## ✅ Unbanning Users

### When to Unban:
- User made payment
- Issue resolved
- Ban was mistake

### How to Unban:
1. Find banned user (red background row)
2. Click **"✅ Unban"** button
3. Confirm action
4. User can login immediately

---

## 💳 Payment Status Management

### Payment Statuses:

| Status | Icon | Meaning | Action |
|--------|------|---------|--------|
| **Pending** | ⏳ | Awaiting payment | Contact user |
| **Trial** | ⏱️ | 14-day trial active | Monitor trial end |
| **Paid** | ✅ | Active subscription | No action |
| **Overdue** | ⚠️ | Payment overdue | Ban if not resolved |

### How to Update Payment Status:
1. Click **💳** button next to user
2. Select new status:
   - Pending Payment
   - Trial Period (14 days)
   - Paid ✅
   - Overdue ⚠️
3. Click **"Update Status"**

### Trial Period Details:
- **Duration**: 14 days from registration
- **Full access** during trial
- **Days remaining** shown in payment column
- **Auto-expires** after 14 days → status becomes "Overdue"

---

## 🌐 IP Address Tracking

### Why Track IPs?
- Detect multiple accounts from same IP
- Block banned IPs
- Fraud prevention
- Geographic insights
- Abuse detection

### IP Columns:
1. **Registration IP**: IP used during signup
2. **Last Login IP**: Most recent login IP

### Use Cases:

#### Multiple Accounts Detection:
```sql
-- Find users with same IP:
Registration IP: 197.242.150.10
Users:
  - john@example.com
  - jane@example.com
  - test@example.com

⚠️ Possible multi-accounting!
```

#### IP Banning:
If user banned, note their IPs:
- Registration IP: `197.242.150.10`
- Last Login IP: `197.242.150.15`

Watch for new signups from these IPs!

---

## 📈 Activity Metrics

### What's Tracked:
- **Contacts**: Number of contacts created
- **Companies**: Number of companies created
- **Deals**: Number of deals created
- **Total Activity**: Sum of all three

### Activity Breakdown Example:
```
Total: 47
15c · 8co · 24d

15 contacts
8 companies
24 deals
```

### Using Activity Data:

**High Activity** (50+):
- ✅ Engaged user
- ✅ Good candidate for paid tier
- ✅ Likely to renew subscription

**Medium Activity** (10-50):
- 📊 Regular user
- 📊 Monitor engagement
- 📊 May need follow-up

**Low Activity** (0-10):
- ⚠️ Trial user testing
- ⚠️ May not convert
- ⚠️ Risk of churn

**Zero Activity**:
- 🚫 Dead account
- 🚫 Consider cleanup
- 🚫 May be spam signup

---

## 🎯 Common Admin Tasks

### 1. Daily User Review
```
Morning Routine:
1. Check "Overdue" count
2. Review trial users ending today
3. Check for suspicious IPs
4. Follow up with high-activity users
```

### 2. Weekly Payment Collection
```
Every Monday:
1. Filter by payment_status = "Overdue"
2. Send payment reminder emails
3. Ban if > 7 days overdue
4. Update payment status for paid users
```

### 3. Monthly IP Audit
```
End of Month:
1. Export IP addresses
2. Check for duplicate IPs
3. Investigate multi-accounting
4. Block suspicious IP ranges
```

### 4. Fraud Prevention
```
Watch for:
- Multiple signups same IP
- Fake company names
- Disposable email addresses
- Zero activity after signup
- Rapid account creation patterns
```

---

## 🔐 Security Best Practices

### Do's:
✅ Ban unpaid users after grace period (7 days)
✅ Monitor IP addresses for patterns
✅ Keep ban reasons documented
✅ Review trial expirations daily
✅ Track payment status changes
✅ Investigate suspicious activity immediately

### Don'ts:
❌ Don't ban without valid reason
❌ Don't share user IPs publicly
❌ Don't ignore overdue payments
❌ Don't unban without payment confirmation
❌ Don't allow multiple trials same IP

---

## 🛠️ Technical Details

### Backend API Endpoints:

#### Get All Users:
```http
GET /api/admin/users/
Authorization: Bearer <admin_token>

Response:
{
  "users": [...],
  "summary": {
    "total_users": 15,
    "active_users": 12,
    "banned_users": 1,
    ...
  }
}
```

#### Ban User:
```http
POST /api/admin/users/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "action": "ban",
  "user_id": 5,
  "reason": "Unpaid subscription"
}
```

#### Unban User:
```http
POST /api/admin/users/
Authorization: Bearer <admin_token>

{
  "action": "unban",
  "user_id": 5
}
```

#### Update Payment:
```http
POST /api/admin/users/
Authorization: Bearer <admin_token>

{
  "action": "update_payment",
  "user_id": 5,
  "payment_status": "paid"
}
```

### Database Fields:

```python
UserProfile:
  - registration_ip: GenericIPAddressField
  - last_login_ip: GenericIPAddressField
  - is_banned: BooleanField
  - ban_reason: TextField
  - banned_at: DateTimeField
  - payment_status: CharField (pending/trial/paid/overdue)
  - trial_ends_at: DateTimeField
```

---

## 📱 Mobile View

User management is fully responsive:
- Summary cards stack vertically
- Table scrolls horizontally
- Touch-friendly buttons
- Modals adapt to screen size

---

## 🚨 Troubleshooting

### "User can still login after ban"
**Solution**: Check that:
1. `is_banned = True` in database
2. `is_active = False` on User model
3. User clears browser cache
4. JWT token expired (force logout)

### "IP showing as null"
**Solution**:
1. Check proxy/firewall settings
2. Ensure `HTTP_X_FORWARDED_FOR` passed through
3. Verify `REMOTE_ADDR` in request META
4. May need nginx/apache IP forwarding config

### "Payment status not updating"
**Solution**:
1. Check admin permissions (superuser/staff)
2. Verify user has profile
3. Check API response for errors
4. Refresh page after update

---

## 📊 Reporting

### Export User Data:
Currently manual (via admin interface).

### Future Features:
- CSV export of user list
- IP address reports
- Payment collection reports
- Activity analytics dashboard
- Automated ban emails
- Payment reminder automation

---

## 💡 Pro Tips

### 1. Grace Period for Overdue:
Don't ban immediately when trial ends. Give 3-7 days grace period.

### 2. Payment Reminders:
Send reminder 3 days before trial ends, then on expiry day, then 3 days after.

### 3. IP Tracking:
Keep spreadsheet of banned IPs to quickly identify repeat offenders.

### 4. Activity Thresholds:
- High value: 50+ activity = likely to pay
- Medium: 10-50 = follow up needed
- Low: <10 = may not convert

### 5. Trial Strategy:
14-day trial gives users time to see value. Monitor at 7 days and 14 days for engagement.

---

## 🎯 Success Metrics

Track these KPIs:
- **Trial → Paid conversion**: Target 20%+
- **Overdue → Paid recovery**: Target 50%+
- **Active user retention**: Target 90%+
- **Banned users**: Keep under 5%
- **Average activity per user**: Monitor trends

---

## 📞 Support

**Admin Questions?**
- Email: admin@thefinisher.co.za
- Docs: /docs/admin-guide

**User Support:**
- Email: support@thefinisher.co.za
- Response time: 24 hours

---

## 🔄 Changelog

**v1.0 - December 2024**
- Initial user management system
- IP tracking and ban functionality
- Payment status management
- Trial period automation
- Activity metrics dashboard

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Access Level**: Admin/Superuser Only  
**Status**: Production Ready ✅

