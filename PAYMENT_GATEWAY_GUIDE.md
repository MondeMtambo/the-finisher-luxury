# 💳 Payment Gateway Integration Guide - Luxury Edition

## Overview
This guide shows how to replace the current payment placeholder with a real payment gateway for THE FINISHER LUXURY Edition (R99/month subscriptions).

---

## 🇿🇦 Recommended Payment Gateways for South Africa

### Option 1: PayFast (Recommended for ZA)
- ✅ Most popular in South Africa
- ✅ Accepts all major SA cards & EFT
- ✅ Simple recurring billing
- ✅ Low transaction fees (2.9% + R2.00)
- ✅ No monthly fees
- 📚 Docs: https://www.payfast.co.za/developers/

### Option 2: Stripe
- ✅ International standard
- ✅ Excellent developer experience
- ✅ Advanced subscription management
- ✅ Webhooks for events
- ⚠️ Higher fees for ZA transactions
- 📚 Docs: https://stripe.com/docs

### Option 3: Peach Payments
- ✅ African-focused
- ✅ Good SA support
- ✅ Multiple payment methods
- ⚠️ More complex setup
- 📚 Docs: https://www.peachpayments.com/developers/

---

## 🚀 Implementation Plan (PayFast Example)

### Phase 1: Backend Setup

#### 1.1 Install Dependencies
```bash
cd backend
pip install payfast-python
pip install django-payfast
```

#### 1.2 Update `backend/requirements.txt`
```txt
# Add to requirements.txt:
payfast-python==1.0.0
django-payfast==0.3.0
```

#### 1.3 Configure Django Settings
**File**: `backend/finisher_api/settings.py`

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'payfast',
]

# PayFast Configuration
PAYFAST_MERCHANT_ID = os.environ.get('PAYFAST_MERCHANT_ID', '10000100')  # Sandbox
PAYFAST_MERCHANT_KEY = os.environ.get('PAYFAST_MERCHANT_KEY', '46f0cd694581a')  # Sandbox
PAYFAST_PASSPHRASE = os.environ.get('PAYFAST_PASSPHRASE', 'jt7NOE43FZPn')  # For security
PAYFAST_USE_SANDBOX = os.environ.get('PAYFAST_USE_SANDBOX', 'True') == 'True'

PAYFAST_BASE_URL = (
    'https://sandbox.payfast.co.za/eng/process' 
    if PAYFAST_USE_SANDBOX 
    else 'https://www.payfast.co.za/eng/process'
)

# Subscription Plans
SPORT_TIER_PRICE = 99.00  # R99/month
LUXURY_TIER_PRICE = 249.00  # R249/month
PREMIUM_TIER_PRICE = 499.00  # R499/month
```

#### 1.4 Create Subscription Model
**File**: `backend/crm/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    tier = models.CharField(max_length=20, choices=[
        ('free', 'Free'),
        ('luxury', 'Sport'),
        ('luxury', 'Luxury'),
        ('premium', 'Premium'),
    ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # PayFast fields
    payfast_token = models.CharField(max_length=255, blank=True, null=True)
    payfast_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Billing dates
    start_date = models.DateTimeField(auto_now_add=True)
    next_billing_date = models.DateField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    
    # Amounts
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='ZAR')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.tier} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']


class PaymentTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('subscription', 'Subscription Payment'),
        ('upgrade', 'Tier Upgrade'),
        ('refund', 'Refund'),
    ]
    
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # PayFast fields
    payfast_payment_id = models.CharField(max_length=255, unique=True)
    payfast_token = models.CharField(max_length=255, blank=True, null=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)  # complete, cancelled, failed
    
    payment_date = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.subscription.user.email} - R{self.amount} - {self.status}"
```

#### 1.5 Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 1.6 Create Payment Views
**File**: `backend/crm/payment_views.py`

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.urls import reverse
import hashlib
import urllib.parse
from datetime import datetime, timedelta
from .models import Subscription, PaymentTransaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """
    Generate PayFast payment URL for user subscription
    """
    user = request.user
    tier = request.data.get('tier', 'luxury')
    
    # Determine amount based on tier
    tier_prices = {
        'luxury': settings.SPORT_TIER_PRICE,
        'luxury': settings.LUXURY_TIER_PRICE,
        'premium': settings.PREMIUM_TIER_PRICE,
    }
    amount = tier_prices.get(tier, settings.SPORT_TIER_PRICE)
    
    # Create or get subscription
    subscription, created = Subscription.objects.get_or_create(
        user=user,
        defaults={
            'tier': tier,
            'amount': amount,
            'status': 'pending',
        }
    )
    
    # PayFast payment data
    payment_data = {
        'merchant_id': settings.PAYFAST_MERCHANT_ID,
        'merchant_key': settings.PAYFAST_MERCHANT_KEY,
        'return_url': f"{settings.FRONTEND_URL}/payment-success",
        'cancel_url': f"{settings.FRONTEND_URL}/payment-cancelled",
        'notify_url': f"{settings.BACKEND_URL}/api/payment/webhook/",
        
        # Item details
        'item_name': f'THE FINISHER LUXURY - {tier.upper()} Tier',
        'item_description': f'{tier.upper()} tier subscription (R{amount}/month)',
        'amount': str(amount),
        
        # Subscription details
        'subscription_type': '1',  # 1 = subscription
        'billing_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'recurring_amount': str(amount),
        'frequency': '3',  # 3 = monthly
        'cycles': '0',  # 0 = until cancelled
        
        # Customer details
        'name_first': user.first_name or 'Customer',
        'name_last': user.last_name or '',
        'email_address': user.email,
        
        # Custom fields
        'custom_str1': str(user.id),
        'custom_str2': tier,
        'custom_int1': subscription.id,
    }
    
    # Generate signature
    signature = generate_payfast_signature(payment_data, settings.PAYFAST_PASSPHRASE)
    payment_data['signature'] = signature
    
    # Generate payment URL
    payment_url = f"{settings.PAYFAST_BASE_URL}?{urllib.parse.urlencode(payment_data)}"
    
    return Response({
        'payment_url': payment_url,
        'subscription_id': subscription.id,
        'amount': amount,
        'tier': tier,
    })


@api_view(['POST'])
def payment_webhook(request):
    """
    Handle PayFast webhook notifications (ITN)
    """
    data = request.POST.dict()
    
    # Verify signature
    signature = data.pop('signature', None)
    calculated_signature = generate_payfast_signature(data, settings.PAYFAST_PASSPHRASE)
    
    if signature != calculated_signature:
        return Response({'error': 'Invalid signature'}, status=400)
    
    # Process payment
    payment_status = data.get('payment_status')
    subscription_id = data.get('custom_int1')
    
    try:
        subscription = Subscription.objects.get(id=subscription_id)
        
        if payment_status == 'COMPLETE':
            subscription.status = 'active'
            subscription.payfast_token = data.get('token')
            subscription.payfast_subscription_id = data.get('m_payment_id')
            subscription.next_billing_date = datetime.now() + timedelta(days=30)
            subscription.save()
            
            # Update user profile tier
            user_profile = subscription.user.userprofile
            user_profile.tier = subscription.tier
            user_profile.save()
            
            # Record transaction
            PaymentTransaction.objects.create(
                subscription=subscription,
                transaction_type='subscription',
                payfast_payment_id=data.get('pf_payment_id'),
                payfast_token=data.get('token'),
                amount=data.get('amount_gross'),
                status='complete',
                metadata=data,
            )
        
        elif payment_status in ['CANCELLED', 'FAILED']:
            subscription.status = 'cancelled'
            subscription.save()
        
        return Response({'status': 'success'})
    
    except Subscription.DoesNotExist:
        return Response({'error': 'Subscription not found'}, status=404)


def generate_payfast_signature(data, passphrase=None):
    """
    Generate MD5 signature for PayFast
    """
    # Remove signature if present
    data = {k: v for k, v in data.items() if k != 'signature'}
    
    # Sort and create parameter string
    sorted_params = sorted(data.items())
    param_string = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params])
    
    # Add passphrase if provided
    if passphrase:
        param_string += f'&passphrase={urllib.parse.quote_plus(passphrase)}'
    
    # Generate MD5 hash
    return hashlib.md5(param_string.encode()).hexdigest()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    """
    Get current user's subscription status
    """
    try:
        subscription = Subscription.objects.get(user=request.user)
        return Response({
            'tier': subscription.tier,
            'status': subscription.status,
            'amount': subscription.amount,
            'next_billing_date': subscription.next_billing_date,
            'transactions': [
                {
                    'date': t.payment_date,
                    'amount': t.amount,
                    'status': t.status,
                }
                for t in subscription.transactions.all()[:5]
            ]
        })
    except Subscription.DoesNotExist:
        return Response({'error': 'No active subscription'}, status=404)
```

#### 1.7 Add URL Routes
**File**: `backend/crm/urls.py`

```python
from django.urls import path
from . import payment_views

urlpatterns = [
    # ... existing urls
    path('payment/initiate/', payment_views.initiate_payment, name='initiate_payment'),
    path('payment/webhook/', payment_views.payment_webhook, name='payment_webhook'),
    path('payment/status/', payment_views.subscription_status, name='subscription_status'),
]
```

---

### Phase 2: Frontend Integration

#### 2.1 Update API Service
**File**: `frontend/src/api/index.js`

```javascript
// Add payment endpoints
export const paymentAPI = {
  initiatePayment: (data) => 
    api.post('/payment/initiate/', data),
  
  getSubscriptionStatus: () => 
    api.get('/payment/status/'),
};
```

#### 2.2 Update Registration Component
**File**: `frontend/src/components/Register.vue`

Replace the placeholder payment code (lines 375-395) with:

```javascript
async handleRegister() {
  this.loading = true
  this.error = ''
  this.success = ''

  try {
    const response = await authAPI.register(this.form)
    
    this.success = response.data.message
    
    // Store tokens
    authService.setTokens(response.data.tokens.access, response.data.tokens.refresh)
    authService.setUser(response.data.user)
    
    // Check if LUXURY tier was selected
    if (this.form.tier === 'luxury') {
      // Initiate payment flow
      const proceedToPayment = confirm(
        '🏆 Luxury Edition ACTIVATED!\n\n' +
        'Your account has been created successfully!\n\n' +
        '💳 Next Step: Complete Payment (R99/month)\n\n' +
        'Click OK to proceed to secure payment, or Cancel to access your dashboard first.\n\n' +
        'Note: Some features require active subscription.'
      )
      
      if (proceedToPayment) {
        try {
          // Call backend to generate payment URL
          const paymentResponse = await paymentAPI.initiatePayment({
            tier: this.form.tier
          })
          
          // Redirect to PayFast payment page
          window.location.href = paymentResponse.data.payment_url
          return // Don't proceed to dashboard yet
        } catch (paymentError) {
          console.error('Payment initiation failed:', paymentError)
          alert('⚠️ Payment setup failed. You can complete payment later from your dashboard.')
        }
      }
    }
    
    // Redirect to dashboard after short delay
    setTimeout(() => {
      this.$router.push('/')
    }, 1500)

  } catch (error) {
    // ... existing error handling
  }
}
```

#### 2.3 Create Payment Success Page
**File**: `frontend/src/components/PaymentSuccess.vue`

```vue
<template>
  <div class="payment-success">
    <div class="success-card">
      <div class="success-icon">✅</div>
      <h2>Payment Successful!</h2>
      <p>Your Luxury Edition subscription is now active.</p>
      
      <div class="subscription-details">
        <h3>Subscription Details:</h3>
        <ul>
          <li><strong>Tier:</strong> LUXURY 🏆</li>
          <li><strong>Amount:</strong> R99/month</li>
          <li><strong>Status:</strong> Active</li>
          <li><strong>Next Billing:</strong> {{ nextBillingDate }}</li>
        </ul>
      </div>
      
      <button @click="goToDashboard" class="dashboard-btn">
        Go to Dashboard
      </button>
    </div>
  </div>
</template>

<script>
import { paymentAPI } from '@/api'

export default {
  name: 'PaymentSuccess',
  data() {
    return {
      nextBillingDate: ''
    }
  },
  async mounted() {
    // Fetch subscription status
    try {
      const response = await paymentAPI.getSubscriptionStatus()
      this.nextBillingDate = new Date(response.data.next_billing_date).toLocaleDateString()
    } catch (error) {
      console.error('Failed to fetch subscription status:', error)
    }
  },
  methods: {
    goToDashboard() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.payment-success {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
}

.success-card {
  background: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 500px;
}

.success-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
}

.success-card h2 {
  color: #28a745;
  margin-bottom: 1rem;
}

.subscription-details {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 10px;
  margin: 2rem 0;
  text-align: left;
}

.subscription-details ul {
  list-style: none;
  padding: 0;
}

.subscription-details li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #e0e0e0;
}

.dashboard-btn {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #1a1a1a;
  border: none;
  padding: 1rem 2rem;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.dashboard-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}
</style>
```

#### 2.4 Add Payment Routes
**File**: `frontend/src/router/index.js`

```javascript
import PaymentSuccess from '@/components/PaymentSuccess.vue'

const routes = [
  // ... existing routes
  {
    path: '/payment-success',
    name: 'PaymentSuccess',
    component: PaymentSuccess
  },
]
```

---

### Phase 3: Environment Configuration

#### 3.1 Backend Environment Variables
**File**: `backend/.env`

```env
# PayFast Configuration
PAYFAST_MERCHANT_ID=10000100  # Replace with your merchant ID
PAYFAST_MERCHANT_KEY=46f0cd694581a  # Replace with your merchant key
PAYFAST_PASSPHRASE=your_secure_passphrase_here
PAYFAST_USE_SANDBOX=True  # Set to False for production

# URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

#### 3.2 Production Settings
**File**: `backend/finisher_api/settings.py`

```python
# For production deployment:
PAYFAST_USE_SANDBOX = False
BACKEND_URL = 'https://api.thefinisher.co.za'
FRONTEND_URL = 'https://thefinisher.co.za'

# Security
CSRF_TRUSTED_ORIGINS = [
    'https://www.payfast.co.za',
    'https://sandbox.payfast.co.za',
]
```

---

## 🧪 Testing Guide

### Sandbox Testing (PayFast)

#### Test Card Details:
```
Card Number: 4000 0000 0000 0002
Expiry Date: Any future date
CVV: 123
```

#### Test Flow:
1. Register with LUXURY tier
2. Click "Proceed to Payment"
3. Redirected to PayFast sandbox
4. Use test card details
5. Complete payment
6. Redirected back to `/payment-success`
7. Check subscription status in dashboard

---

## 🔐 Security Checklist

- [ ] Use HTTPS in production
- [ ] Validate PayFast signatures
- [ ] Store passphrase securely (environment variables)
- [ ] Implement CSRF protection
- [ ] Validate subscription status on backend before granting access
- [ ] Log all payment transactions
- [ ] Handle webhook retries
- [ ] Implement rate limiting on payment endpoints

---

## 📊 Monitoring & Analytics

### Add Payment Tracking:
```javascript
// In handleRegister success:
if (paymentResponse.data.payment_url) {
  // Track payment initiation
  analytics.track('Payment Initiated', {
    tier: this.form.tier,
    amount: paymentResponse.data.amount
  })
}

// In PaymentSuccess.vue mounted:
analytics.track('Payment Completed', {
  tier: 'luxury',
  amount: 99
})
```

---

## 🚨 Common Issues & Solutions

### Issue 1: Webhook Not Receiving Data
**Solution**: 
- Ensure `notify_url` is publicly accessible
- Use ngrok for local testing: `ngrok http 8000`
- Check firewall settings

### Issue 2: Signature Mismatch
**Solution**:
- Verify passphrase is correct
- Check URL encoding
- Ensure data order matches

### Issue 3: Subscription Not Activating
**Solution**:
- Check webhook logs
- Verify PayFast credentials
- Test with sandbox first

---

## 📚 Additional Resources

- [PayFast API Docs](https://developers.payfast.co.za/)
- [Django PayFast Package](https://github.com/pjdelport/django-payfast)
- [Stripe Django Integration](https://stripe.com/docs/payments/checkout/django)
- [Payment Security Best Practices](https://owasp.org/www-project-top-ten/)

---

**Next Steps**: 
1. Sign up for PayFast merchant account
2. Get merchant credentials
3. Implement the code above
4. Test in sandbox mode
5. Deploy to production

**Need Help?** Contact PayFast support: support@payfast.co.za

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Status**: Ready for Implementation


