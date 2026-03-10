# 🎨 Luxury Edition - Visual Reference Guide

## Registration Page Tier Cards

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CHOOSE YOUR PLAN (⚡ Luxury Edition Active)            │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   🚫 BLOCKED │  │ ⚡ ACTIVE     │  │   🔒 LOCKED  │  │   🔒 LOCKED  │
│              │  │   EDITION     │  │              │  │              │
│   🎯 FREE    │  │              │  │              │  │              │
│              │  │   🏆 LUXURY   │  │   🥈 LUXURY  │  │   🥇 PREMIUM │
│  NOT         │  │              │  │              │  │              │
│  AVAILABLE   │  │   R99/month  │  │   R249/month │  │   R499/month │
│              │  │              │  │              │  │              │
│ "This is THE │  │ ✓ 2 Users    │  │ ✓ 10 Users   │  │ ✓ Unlimited  │
│  FINISHER    │  │ ✓ Auto-Create│  │ ✓ API Access │  │ ✓ White-Label│
│  LUXURY       │  │ ✓ Reporting  │  │ ✓ Custom Dev │  │ ✓ Dedicated  │
│  Edition"    │  │ ✓ Priority   │  │              │  │   Support    │
│              │  │              │  │              │  │              │
│              │  │ ✨ RECOMMENDED│  │ Coming Q2    │  │ Coming Q2    │
│              │  │              │  │   2026       │  │   2026       │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
  Cursor: ❌       Cursor: ✅         Cursor: ❌         Cursor: ❌
  Opacity: 70%    Gold Border       Opacity: 70%      Opacity: 70%
```

---

## When User Clicks FREE Tier:

```
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️ The FREE tier is not available in THE FINISHER LUXURY         │
│    Edition. Choose the LUXURY plan (R99/month) to unlock         │
│    2-user access, advanced features, and priority support!      │
│                                                                  │
│    [Message disappears after 8 seconds]                         │
└─────────────────────────────────────────────────────────────────┘
  Red border-left | Shake animation | Auto-dismiss
```

---

## When User Clicks LUXURY Tier:

```
┌─────────────────────────────────────────────────────────────────┐
│ 🏆 Luxury Edition SELECTED: Perfect choice! You'll get 2-user    │
│    access, advanced features, and priority support. Payment     │
│    link will be provided after account creation.                │
└─────────────────────────────────────────────────────────────────┘
  Green background | Success styling | Stays visible
```

---

## When User Clicks LUXURY/PREMIUM:

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔒 The LUXURY tier is coming in Q2 2026! For now, start with    │
│    our Luxury Edition (R99/month) to access all current features.│
│                                                                  │
│    [Message disappears after 6 seconds]                         │
└─────────────────────────────────────────────────────────────────┘
  Red border-left | Auto-dismiss
```

---

## Post-Registration Payment Dialog:

```javascript
┌────────────────────────────────────────────────┐
│          🏆 Luxury Edition ACTIVATED!           │
│                                                │
│  Your account has been created successfully!   │
│                                                │
│      💳 Next Step: Complete Payment            │
│              (R99/month)                       │
│                                                │
│  Click OK to proceed to secure payment, or     │
│  Cancel to access your dashboard first.        │
│                                                │
│  Note: Some features require active            │
│        subscription.                           │
│                                                │
│         [  OK  ]     [Cancel]                  │
└────────────────────────────────────────────────┘
```

---

## Dashboard Welcome Section (LUXURY Tier Active):

### Desktop View:
```
┌──────────────────────────────────────────────────────────────────────┐
│  Welcome to THE FINISHER LUXURY! 🏆              ┌────────────────┐  │
│  "Don't just chase leads — finish every         │  🏆  LUXURY     │  │
│   relationship strong."                         │     R99/month  │  │
│                                                  └────────────────┘  │
├──────────────────────────────────────────────────────────────────────┤
│  ⚡ Luxury Edition ACTIVE: 2-User Access | Advanced Reporting |      │
│     Company Auto-Creation | Priority Support                        │
└──────────────────────────────────────────────────────────────────────┘
     Green banner with left border-left (4px solid green)
```

### Mobile View:
```
┌─────────────────────────────────┐
│  Welcome to THE FINISHER LUXURY! │
│             🏆                  │
│  "Don't just chase leads..."    │
│                                 │
│  ┌───────────────────────────┐ │
│  │  🏆  LUXURY                │ │
│  │      R99/month            │ │
│  └───────────────────────────┘ │
│                                 │
│  ⚡ Luxury Edition ACTIVE:       │
│  2-User Access | Advanced       │
│  Reporting | Company Auto-      │
│  Creation | Priority Support    │
└─────────────────────────────────┘
       Stacked layout
```

---

## Dashboard Welcome Section (FREE Tier - Safety Net):

```
┌──────────────────────────────────────────────────────────────────────┐
│  Welcome to THE FINISHER LUXURY! 🏆              ┌────────────────┐  │
│  "Don't just chase leads — finish every         │  🎯  CLASSIC   │  │
│   relationship strong."                         │     Free       │  │
│                                                  └────────────────┘  │
├──────────────────────────────────────────────────────────────────────┤
│  ⚠️ You're on a FREE tier in THE FINISHER LUXURY Edition.            │
│     Upgrade to LUXURY (R99/month) to unlock all features!            │
│                                                     [Upgrade Now]    │
└──────────────────────────────────────────────────────────────────────┘
     Yellow warning banner with upgrade button
```

---

## Color Scheme:

### Tier Badge Colors:
```css
FREE (Classic):    Gray gradient    (#e0e0e0 → #bdbdbd)
LUXURY:             Gold gradient    (#FFD700 → #FFA500)  ⭐ DEFAULT
LUXURY:            Dark Gold        (#DAA520 → #B8860B)
PREMIUM:           Bronze-Gold      (#B8860B → #8B6508)
```

### Alert/Banner Colors:
```css
Success (Green):   #d4edda → #c3e6cb  (border: #28a745)
Warning (Yellow):  #fff3cd → #ffeaa7  (border: #ffc107)
Error (Red):       #f8d7da → #f5c6cb  (border: #dc3545)
```

### Interactive States:
```css
Blocked Card:      opacity: 0.7, cursor: not-allowed
Active Card:       border: 3px solid #FFD700, shadow: rgba(255,215,0,0.4)
Hover (allowed):   transform: translateY(-4px), shadow increase
Hover (blocked):   No transform, no shadow change
```

---

## Animations:

### Shake Animation (Blocked Message):
```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}
Duration: 0.5s
```

### Pulse Animation (Unlimited Badge):
```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
Duration: 2s infinite
```

---

## Responsive Breakpoints:

### Mobile (@media max-width: 768px):
- Welcome header: Stack vertically
- Tier badge: Center alignment
- Banners: Stack icon + text
- Font sizes: Reduced by 15-20%
- Tier cards: 2 columns on mobile (if space allows)

### Small Mobile (@media max-width: 480px):
- Tier cards: 1 column
- Stats grid: 2 columns
- Chart containers: height 200px → 180px
- Padding: 1.5rem → 1rem

---

## Icon Reference:

```
🎯  FREE/Classic Tier
🏆  LUXURY Tier (primary)
🥈  LUXURY Tier (future)
🥇  PREMIUM Tier (future)

🚫  Blocked/Not Available
🔒  Locked/Coming Soon
⚡  Active Edition Indicator
✨  Recommended Badge
⚠️  Warning/Alert
💳  Payment Required
```

---

## User Flow Diagram:

```
                    ┌─────────────────┐
                    │  Landing Page   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Registration    │
                    │ (LUXURY default) │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
         Click FREE │                 │ Click LUXURY
                    │                 │
                    ▼                 ▼
         ┌──────────────────┐  ┌──────────────────┐
         │  Show Block Msg  │  │  Show Success    │
         │  (8 sec timeout) │  │  Notice          │
         └──────────────────┘  └─────────┬────────┘
                                          │
                                          ▼
                                 ┌────────────────┐
                                 │ Submit Form    │
                                 │ tier: 'luxury'  │
                                 └────────┬───────┘
                                          │
                                          ▼
                                 ┌────────────────┐
                                 │ Account Created│
                                 │ Store tokens   │
                                 └────────┬───────┘
                                          │
                                          ▼
                                 ┌────────────────┐
                                 │ Payment Dialog │
                                 │ (R99/month)    │
                                 └────┬──────┬────┘
                                      │      │
                           Click OK   │      │ Click Cancel
                                      │      │
                                      ▼      ▼
                            ┌──────────────────┐
                            │   Dashboard      │
                            │ (LUXURY features) │
                            └──────────────────┘
```

---

## Testing Scenarios:

### ✅ Scenario 1: Normal LUXURY Registration
1. Load registration → LUXURY pre-selected (gold border)
2. Fill form → Submit
3. See payment dialog → Click OK or Cancel
4. Redirect to dashboard → See LUXURY tier badge + green banner
5. Mobile: Stack layout properly

### ✅ Scenario 2: User Tries FREE
1. Load registration → LUXURY pre-selected
2. Click FREE card → See blocking message (red, shake animation)
3. Wait 8 seconds → Message disappears
4. LUXURY still selected (cannot select FREE)

### ✅ Scenario 3: User Tries LUXURY
1. Load registration → LUXURY pre-selected
2. Click LUXURY card → See "coming soon" message
3. Wait 6 seconds → Message disappears
4. LUXURY still selected

### ✅ Scenario 4: Mobile Registration
1. Load on mobile (< 768px width)
2. Tier cards stack vertically
3. Blocked overlays visible
4. Touch interactions work
5. Payment dialog readable

### ✅ Scenario 5: Dashboard Load
1. User logs in with tier='luxury'
2. Dashboard reads from localStorage
3. Shows LUXURY badge (top-right)
4. Shows green active banner
5. All features accessible

---

## Feature Access Matrix:

```
Feature                  │ FREE │ LUXURY │ LUXURY │ PREMIUM
─────────────────────────┼──────┼───────┼────────┼─────────
Max Users                │  1   │   2   │   10   │   999
Unlimited Contacts       │  ✓   │   ✓   │   ✓    │    ✓
Company Auto-Creation    │  ✗   │   ✓   │   ✓    │    ✓
Advanced Reporting       │  ✗   │   ✓   │   ✓    │    ✓
Priority Support         │  ✗   │   ✓   │   ✓    │    ✓
API Access               │  ✗   │   ✗   │   ✓    │    ✓
Custom Integrations      │  ✗   │   ✗   │   ✓    │    ✓
White-Label              │  ✗   │   ✗   │   ✗    │    ✓
Dedicated Support        │  ✗   │   ✗   │   ✗    │    ✓
─────────────────────────┴──────┴───────┴────────┴─────────
Status in Luxury Edition: BLOCKED │ ACTIVE │ LOCKED │ LOCKED
```

---

**Last Updated**: December 2024  
**Edition**: Luxury Edition 1.0  
**Purpose**: Visual reference for tier system implementation


