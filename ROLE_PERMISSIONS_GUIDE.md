# THE FINISHER LUXURY - Role-Based Permissions Guide

## Overview
THE FINISHER LUXURY now includes a comprehensive role-based permission system to protect your CRM data and ensure proper team hierarchy.

## User Roles

### 1. **Administrator** (`admin`)
- **Full System Access**: Can perform any action in the system
- **User Management**: Can add, edit, and remove users
- **Deal Control**: Can start AND stop deal timers
- **Deal Management**: Can create, edit, and delete any deal
- **Data Management**: Full access to all contacts, companies, and activities

**Who should be an Admin?**
- Business owner
- IT administrator
- Senior management with full oversight

### 2. **Manager** (`manager`)
- **Team Oversight**: Can manage deals and monitor progress
- **Deal Control**: Can start AND stop deal timers
- **Deal Management**: Can create, edit, and delete deals
- **Data Management**: Full access to contacts, companies, and activities
- **Limited User Access**: Cannot manage user accounts

**Who should be a Manager?**
- Sales managers
- Department heads
- Team leads who need full deal control

### 3. **Supervisor** (`supervisor`)
- **Team Monitoring**: Can view all data
- **Deal Management**: Can create and edit deals
- **Timer Restriction**: Can START timers but CANNOT stop them
- **Data Access**: Full read access to all data
- **No Deletions**: Cannot delete deals

**Who should be a Supervisor?**
- Team supervisors
- Junior managers
- Quality assurance roles

### 4. **Standard User** (`user`)
- **Basic Access**: Can create and edit their own records
- **Deal Creation**: Can create and edit deals
- **Timer Usage**: Can START timers but CANNOT stop them
- **No Deletions**: Cannot delete deals
- **Standard Operations**: Contact and company management

**Who should be a Standard User?**
- Sales representatives
- Account executives
- General team members

## Permission Matrix

| Action | Admin | Manager | Supervisor | User |
|--------|-------|---------|------------|------|
| Create Contact | ✅ | ✅ | ✅ | ✅ |
| Edit Contact | ✅ | ✅ | ✅ | ✅ |
| Delete Contact | ✅ | ✅ | ✅ | ✅ |
| Create Company | ✅ | ✅ | ✅ | ✅ |
| Edit Company | ✅ | ✅ | ✅ | ✅ |
| Delete Company | ✅ | ✅ | ✅ | ✅ |
| Create Deal | ✅ | ✅ | ✅ | ✅ |
| Edit Deal | ✅ | ✅ | ✅ | ✅ |
| **Delete Deal** | ✅ | ✅ | ❌ | ❌ |
| **Start Deal Timer** | ✅ | ✅ | ✅ | ✅ |
| **Stop Deal Timer** | ✅ | ✅ | ❌ | ❌ |
| View Reports | ✅ | ✅ | ✅ | ✅ |
| Export Data | ✅ | ✅ | ✅ | ✅ |
| **Manage Users** | ✅ | ❌ | ❌ | ❌ |

## Key Features

### 🔒 Deal Timer Protection
**Why can't everyone stop timers?**
- Ensures accurate time tracking
- Prevents accidental time loss
- Maintains data integrity
- Provides audit trail

**How it works:**
1. Any user can START a deal timer
2. Timer runs continuously (never stops on its own)
3. Only Admins and Managers can STOP timers
4. Clear visual indicators show locked features

### 🗑️ Deal Deletion Protection
**Why restricted deletion?**
- Prevents accidental data loss
- Maintains historical records
- Requires management approval
- Protects pipeline integrity

**User Experience:**
- Delete buttons are grayed out for unauthorized users
- Hover tooltips explain permission requirements
- Clear error messages if action attempted
- No confusion about access levels

## Setting User Roles

### For the Admin User
Your admin account is automatically set to `admin` role with full permissions.

### For Additional Users
When the second user registers:
1. They will be assigned `user` role by default
2. An administrator can update their role in the Django admin panel
3. Role changes take effect immediately on next login

### Via Django Admin (for developers)
```python
python manage.py shell

from django.contrib.auth.models import User
from crm.models import UserProfile

# Get user
user = User.objects.get(username='username_here')

# Update role
user.profile.role = 'manager'  # or 'admin', 'supervisor', 'user'
user.profile.save()

print(f"✅ {user.username} role updated to {user.profile.role}")
```

## UI Indicators

### Permission Denial Messages
When a user attempts an unauthorized action:

**Timer Stop (Supervisor/User):**
```
🔒 Access Denied: Only administrators and managers can stop deal timers.

This ensures consistent time tracking across your team.
```

**Deal Deletion (Supervisor/User):**
```
🔒 Access Denied: Only administrators and managers can delete deals.

Contact your system administrator for assistance.
```

### Visual Indicators
- **Disabled Buttons**: Grayed out with reduced opacity
- **Hover Tooltips**: Show lock icon (🔒) with explanation
- **Cursor Changes**: `not-allowed` cursor on disabled buttons

## Frontend Permission Checking

The frontend automatically checks permissions from the user's profile:
```javascript
// In any component
const canStopTimer = this.userPermissions?.can_stop_deal_timers || false
const canDeleteDeals = this.userPermissions?.can_delete_deals || false
```

Permissions are loaded on login and stored in localStorage for fast access.

## Backend Enforcement

While the frontend hides/disables unauthorized actions, the backend also enforces permissions through:
- Django User model `is_superuser` check
- UserProfile role properties
- View-level permission checks (can be added as needed)

## Luxury Edition User Limits

Remember: THE FINISHER LUXURY allows a maximum of **2 users**.

**Team Composition Recommendations:**
1. **Solo + Assistant**: Admin + User
2. **Manager + Sales Rep**: Manager + User
3. **Two Managers**: Manager + Manager
4. **Owner + Manager**: Admin + Manager

Choose roles based on your team's trust and responsibility levels.

## Security Best Practices

1. **Assign Minimum Required Role**: Don't make everyone an admin
2. **Review Roles Regularly**: Ensure roles match current responsibilities
3. **Protect Admin Credentials**: Keep admin password secure
4. **Monitor Activity**: Check activity logs for unusual patterns
5. **Role Transitions**: Update roles when responsibilities change

## Troubleshooting

### "I can't stop a timer"
**Solution**: You need Manager or Admin role. Contact your administrator.

### "Delete button is grayed out"
**Solution**: You need Manager or Admin role to delete deals.

### "How do I check my role?"
**Solution**: Your role is visible in the user profile section (coming soon in UI).

### "Can I upgrade my role?"
**Solution**: Only administrators can change user roles. Contact your admin.

## Future Enhancements (Roadmap)

- User Profile page showing current role
- Role badge in navbar
- Activity log with user roles
- Role-based dashboard customization
- Email notifications for role changes
- Bulk user management (LUXURY/PREMIUM tiers)

---

**THE FINISHER LUXURY** - Premium CRM for Small Teams 🏆

