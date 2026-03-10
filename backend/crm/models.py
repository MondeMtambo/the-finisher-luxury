from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, datetime
import phonenumbers
from phonenumbers import NumberParseException
import random

class UserProfile(models.Model):
    """
    User profile for THE FINISHER LUXURY.
    LUXURY edition: Maximum 10 users with all premium features
    Roles: admin, manager, supervisor, user
    """
    TIER_CHOICES = [
        ('luxury', 'FINISHER LUXURY'),
    ]
    
    ROLE_CHOICES = [
        ('admin', 'CEO / Administrator'),
        ('executive', 'Executive'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('user', 'Standard Employee'),
    ]
    
    INDUSTRY_CHOICES = [
        ('it', 'Information Technology'),
        ('retail', 'Retail & E-commerce'),
        ('healthcare', 'Healthcare & Medical'),
        ('manufacturing', 'Manufacturing'),
        ('finance', 'Finance & Banking'),
        ('real_estate', 'Real Estate'),
        ('education', 'Education & Training'),
        ('hospitality', 'Hospitality & Tourism'),
        ('construction', 'Construction & Engineering'),
        ('consulting', 'Consulting & Professional Services'),
        ('marketing', 'Marketing & Advertising'),
        ('logistics', 'Logistics & Transportation'),
        ('other', 'Other'),
    ]
    
    COMPANY_SIZE_CHOICES = [
        ('1-5', '1-5 employees'),
        ('6-20', '6-20 employees'),
        ('21-50', '21-50 employees'),
        ('51-200', '51-200 employees'),
        ('200+', '200+ employees'),
    ]
    
    REFERRAL_SOURCE_CHOICES = [
        ('google', 'Google Search'),
        ('social_media', 'Social Media'),
        ('referral', 'Friend/Colleague Referral'),
        ('advertisement', 'Advertisement'),
        ('blog', 'Blog/Article'),
        ('event', 'Event/Conference'),
        ('other', 'Other'),
    ]
    
    COUNTRY_CHOICES = [
        ('ZA', 'South Africa'),
        ('US', 'United States'),
        ('GB', 'United Kingdom'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('Other', 'Other'),
    ]
    
    EXPECTED_CONTACTS_CHOICES = [
        ('0-100', '0-100 contacts'),
        ('100-500', '100-500 contacts'),
        ('500-2000', '500-2000 contacts'),
        ('2000+', '2000+ contacts'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='luxury')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True, help_text="User's company/business name")

    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, blank=True, help_text="Industry/Business type")
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES, blank=True, help_text="Number of employees")
    referral_source = models.CharField(max_length=50, choices=REFERRAL_SOURCE_CHOICES, blank=True, help_text="How did you hear about us?")
    business_website = models.URLField(max_length=200, blank=True, help_text="Company website URL")
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='ZA', help_text="Country/Region")
    intended_use_case = models.TextField(blank=True, help_text="Why do you need a CRM? What's your use case?")
    current_crm = models.CharField(max_length=100, blank=True, help_text="Current CRM system (if migrating)")
    expected_contacts = models.CharField(max_length=20, choices=EXPECTED_CONTACTS_CHOICES, blank=True, help_text="Expected number of contacts")

    marketing_consent = models.BooleanField(default=False, help_text="User agreed to receive marketing communications")
    terms_accepted_at = models.DateTimeField(blank=True, null=True, help_text="When user accepted Terms & Conditions")

    job_title = models.CharField(max_length=100, blank=True, help_text="Employee's job title/position")
    department = models.CharField(max_length=100, blank=True, help_text="Department or team")
    division = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='employees',
                                 help_text="Organizational division/department (ADMP)")
    employee_id = models.CharField(max_length=50, blank=True, help_text="Internal employee ID")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Date of birth")
    address = models.TextField(blank=True, help_text="Physical address")
    emergency_contact_name = models.CharField(max_length=100, blank=True, help_text="Emergency contact person")
    emergency_contact_phone = models.CharField(max_length=20, blank=True, help_text="Emergency contact number")
    start_date = models.DateField(blank=True, null=True, help_text="Employment start date")
    notes = models.TextField(blank=True, help_text="Additional notes about employee")

    requires_password_reset = models.BooleanField(default=False, help_text="Force user to change password at next login")

    registration_ip = models.GenericIPAddressField(blank=True, null=True, help_text="IP address used during registration")
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, help_text="Most recent login IP address")
    is_banned = models.BooleanField(default=False, help_text="Ban user if unpaid or violation")
    ban_reason = models.TextField(blank=True, help_text="Reason for ban (e.g., 'Unpaid subscription', 'Terms violation')")
    banned_at = models.DateTimeField(blank=True, null=True)

    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('trial', 'Trial Period'),
    ], default='pending')
    trial_ends_at = models.DateTimeField(blank=True, null=True, help_text="14-day trial period end date")

    can_add_employees = models.BooleanField(default=False, help_text="Delegated permission: employee can add new employees (requires admin OTP)")

    reports_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='direct_reports',
                                   help_text="Direct supervisor/manager this employee reports to")
    onboarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='employees_onboarded',
                                     help_text="Who onboarded this employee into the system")
    onboarded_at = models.DateTimeField(null=True, blank=True, help_text="When this employee was onboarded")
    is_offboarded = models.BooleanField(default=False, help_text="Whether this employee has been offboarded")
    offboarded_at = models.DateTimeField(null=True, blank=True, help_text="When this employee was offboarded")

    mfa_enabled = models.BooleanField(default=True, help_text="Whether MFA is enabled for this user")
    mfa_code = models.CharField(max_length=6, blank=True, null=True, help_text="Current OTP code (6 digits)")
    mfa_code_created_at = models.DateTimeField(null=True, blank=True, help_text="When the OTP code was generated")
    mfa_code_attempts = models.IntegerField(default=0, help_text="Failed MFA attempts counter")
    mfa_verified_at = models.DateTimeField(null=True, blank=True, help_text="Last successful MFA verification time")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - THE FINISHER LUXURY ({self.role})"
    
    @property
    def is_luxury_tier(self):
        return self.tier == 'luxury'
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.user.is_superuser
    
    @property
    def can_access(self):
        """Check if user can access the system (not banned, payment valid)"""

        if self.user.is_superuser or self.user.is_staff or self.is_admin:
            return True
        
        if self.is_banned:
            return False
        if self.payment_status in ['paid', 'trial']:
            return True
        return False
    
    @property
    def days_until_trial_end(self):
        """Calculate days remaining in trial"""
        if not self.trial_ends_at:
            return 0
        delta = self.trial_ends_at - timezone.now()
        return max(0, delta.days)
    
    def ban_user(self, reason="Unpaid subscription"):
        """Ban a user with reason"""
        self.is_banned = True
        self.ban_reason = reason
        self.banned_at = timezone.now()
        self.user.is_active = False  # Also deactivate Django user
        self.save()
        self.user.save()
    
    def unban_user(self):
        """Unban a user"""
        self.is_banned = False
        self.ban_reason = ""
        self.banned_at = None
        self.user.is_active = True
        self.save()
        self.user.save()

    @property
    def is_executive(self):
        return self.role in ['admin', 'executive'] or self.user.is_superuser

    @property
    def is_manager(self):
        return self.role in ['admin', 'executive', 'manager'] or self.user.is_superuser

    @property
    def is_supervisor(self):
        return self.role in ['admin', 'executive', 'manager', 'supervisor'] or self.user.is_superuser

    @property
    def can_onboard(self):
        """CEO/Admin, Executives, and Managers can onboard employees."""
        return self.role in ['admin', 'executive', 'manager'] or self.user.is_superuser

    @property
    def onboarding_allowed_roles(self):
        """Return which roles this user can onboard"""
        hierarchy = {
            'admin': ['executive', 'manager', 'supervisor', 'user'],
            'executive': ['manager', 'supervisor', 'user'],
            'manager': ['supervisor', 'user'],
        }
        if self.user.is_superuser:
            return ['admin', 'executive', 'manager', 'supervisor', 'user']
        return hierarchy.get(self.role, [])

    @property
    def can_stop_deal_timers(self):

        return self.is_manager

    @property
    def can_delete_deals(self):

        return self.is_manager

    @property
    def can_manage_users(self):

        return self.is_admin

    @property
    def max_companies(self):

        return 999999

    @property
    def max_users(self):
        from .tier_limits import LUXURY_TIER_LIMITS
        return int(LUXURY_TIER_LIMITS.get('max_users', 50))


class DeletedUserLog(models.Model):
    """
    Track deleted users to warn admin about re-registration attempts
    """
    username = models.CharField(max_length=150)
    email = models.EmailField()
    registration_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True)
    deleted_at = models.DateTimeField(auto_now_add=True)
    deleted_reason = models.TextField(blank=True, help_text="Why was this user deleted?")

    contact_count = models.IntegerField(default=0)
    company_count = models.IntegerField(default=0)
    deal_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Deleted: {self.username} ({self.email}) - {self.deleted_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-deleted_at']
        verbose_name = "Deleted User Log"
        verbose_name_plural = "Deleted User Logs"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create UserProfile when User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save UserProfile when User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']

        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    is_self_employed = models.BooleanField(default=False, help_text="Mark if the contact operates as self-employed")
    company_direct_line = models.CharField(
        max_length=20,
        blank=True,
        help_text="Direct company line when using a corporate email"
    )
    company_name_manual = models.CharField(
        max_length=200,
        blank=True,
        help_text="Captured company name when no linked company exists"
    )
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contact_date = models.DateTimeField(null=True, blank=True, help_text="Last time contact was engaged")

    class Meta:
        ordering = ['-created_at']

        unique_together = ['user', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def health_score(self):
        """
        Calculate relationship health score (0-100) based on:
        - Days since last contact
        - Number of activities in last 30 days
        - Deal stages and values
        """
        score = 50  # Base score

        last_contact = self.last_contact_date or self.updated_at
        if last_contact:
            days_since = (timezone.now() - last_contact).days
            if days_since < 7:
                score += 20
            elif days_since < 14:
                score += 10
            elif days_since < 30:
                score += 0
            elif days_since < 60:
                score -= 20
            else:
                score -= 40

        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_activities = ActivityLog.objects.filter(
            user=self.user,
            entity_type='contact',
            entity_id=self.id,
            created_at__gte=thirty_days_ago
        ).count()
        score += min(recent_activities * 10, 30)

        active_deals = self.deal_set.filter(
            stage__in=['lead', 'qualified', 'proposal', 'negotiation']
        ).count()
        score += min(active_deals * 10, 20)
        
        return max(0, min(100, score))
    
    @property
    def health_status(self):
        """Return health status emoji and text"""
        score = self.health_score
        if score >= 80:
            return {'icon': '🔥', 'label': 'Hot', 'color': '#4CAF50'}
        elif score >= 60:
            return {'icon': '⚡', 'label': 'Warm', 'color': '#FFD700'}
        elif score >= 40:
            return {'icon': '❄️', 'label': 'Cold', 'color': '#2196F3'}
        else:
            return {'icon': '⚠️', 'label': 'At Risk', 'color': '#f44336'}
    
    @property
    def next_step_suggestion(self):
        """Suggest next action based on health score"""
        score = self.health_score
        last_contact = self.last_contact_date or self.updated_at
        days_since = (timezone.now() - last_contact).days if last_contact else 999
        
        if score >= 80:
            return "Keep momentum - Share updates or close the deal!"
        elif score >= 60:
            return f"Good relationship - Consider scheduling next touchpoint."
        elif score >= 40:
            return f"Needs attention - Last contact {days_since} days ago."
        else:
            return f"⚠️ URGENT: No contact in {days_since} days - Reach out today!"
    
    def clean(self):

        validate_email(self.email)

        if self.phone:
            try:
                parsed = phonenumbers.parse(self.phone, "ZA")  # Default to South Africa
                if not phonenumbers.is_valid_number(parsed):
                    raise ValidationError({'phone': 'Invalid phone number format.'})
            except NumberParseException:
                raise ValidationError({'phone': 'Invalid phone number format.'})

        if self.company_direct_line:
            try:
                parsed_direct = phonenumbers.parse(self.company_direct_line, "ZA")
                if not phonenumbers.is_valid_number(parsed_direct):
                    raise ValidationError({'company_direct_line': 'Invalid phone number format.'})
            except NumberParseException:
                raise ValidationError({'company_direct_line': 'Invalid phone number format.'})

        if not self.is_self_employed and not self.company_direct_line:
            raise ValidationError({'company_direct_line': 'Corporate contacts must include a direct company line.'})

class Deal(models.Model):
    STAGE_CHOICES = [
        ('lead', 'Lead'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals')
    title = models.CharField(max_length=200)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='deals', null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='lead')
    time_spent_hours = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0,
        help_text="Total hours spent on this deal/project"
    )
    timer_running = models.BooleanField(default=False)
    timer_started_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def start_timer(self):
        """Start tracking time for this deal"""
        if not self.timer_running:
            self.timer_running = True
            self.timer_started_at = timezone.now()
            self.save()
    
    def stop_timer(self):
        """Stop tracking and add elapsed time"""
        if self.timer_running and self.timer_started_at:
            elapsed = timezone.now() - self.timer_started_at
            hours = elapsed.total_seconds() / 3600
            self.time_spent_hours += round(hours, 2)
            self.timer_running = False
            self.timer_started_at = None
            self.save()
    
    @property
    def current_timer_hours(self):
        """Get current running timer hours (not yet saved)"""
        if self.timer_running and self.timer_started_at:
            elapsed = timezone.now() - self.timer_started_at
            return round(elapsed.total_seconds() / 3600, 2)
        return 0
    
    @property
    def total_hours_display(self):
        """Display total hours including running timer"""
        total = float(self.time_spent_hours) + self.current_timer_hours
        return round(total, 2)


class ActivityLog(models.Model):
    """
    Track user actions for audit trail.
    FREE tier: Shows last 5 activities
    LUXURY+ tier: Shows full history
    """
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
    ]
    
    ENTITY_CHOICES = [
        ('contact', 'Contact'),
        ('company', 'Company'),
        ('deal', 'Deal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=20, choices=ENTITY_CHOICES)
    entity_id = models.IntegerField()
    entity_name = models.CharField(max_length=255)  # Store name for display even if deleted
    details = models.TextField(blank=True)  # JSON or text description
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} {self.action} {self.entity_type} '{self.entity_name}'"


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('support', 'Support'),
        ('bug', 'Bug'),
        ('feature', 'Feature Request'),
        ('task', 'Task'),
    ]
    DEPARTMENT_CHOICES = [
        ('admin', 'Admin'),
        ('sales', 'Sales'),
        ('support', 'Support'),
        ('operations', 'Operations'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_created')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_assigned')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, default='support')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    started_at = models.DateTimeField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0, help_text="Total duration tracked for this ticket in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket: {self.title} ({self.get_status_display()})"

    def mark_completed(self):
        if self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()

            if self.started_at:
                elapsed = timezone.now() - self.started_at
                self.duration_seconds += int(elapsed.total_seconds())
                self.started_at = None
            self.save()

    def start(self):
        if not self.started_at:
            self.status = 'in_progress'
            self.started_at = timezone.now()
            self.save()

    def stop(self):
        if self.started_at:
            elapsed = timezone.now() - self.started_at
            self.duration_seconds += int(elapsed.total_seconds())
            self.started_at = None
            self.save()


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    entity_type = models.CharField(max_length=50, blank=True)
    entity_id = models.IntegerField(null=True, blank=True)
    meta = models.JSONField(blank=True, null=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
        ]

    def mark_read(self):
        if not self.read_at:
            self.read_at = timezone.now()
            self.save(update_fields=['read_at'])


class PasswordResetOTP(models.Model):
    """
    One-Time Password for secure password reset via email.
    OTP expires after 10 minutes and can only be used once.
    """
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', '-created_at']),
            models.Index(fields=['otp_code', 'is_used']),
        ]
    
    def save(self, *args, **kwargs):

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired
    
    def mark_as_used(self):
        self.is_used = True
        self.used_at = timezone.now()
        self.save()
    
    @staticmethod
    def generate_otp():
        """Generate a random 6-digit OTP"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    def __str__(self):
        status = "Valid" if self.is_valid else ("Used" if self.is_used else "Expired")
        return f"OTP for {self.email} - {status}"


class EmployeeAddOTP(models.Model):
    """
    OTP sent to company admin when a delegated employee tries to add a new employee.
    The admin must confirm the OTP before the employee is created.
    Expires after 10 minutes.
    """
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_add_otps',
                                   help_text="The company admin who must approve")
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_add_requests',
                                     help_text="The delegated employee requesting to add")
    otp_code = models.CharField(max_length=6)
    employee_data = models.JSONField(help_text="Serialized data for the new employee to create upon approval")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired
    
    def mark_as_used(self):
        self.is_used = True
        self.used_at = timezone.now()
        self.save()
    
    @staticmethod
    def generate_otp():
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    def __str__(self):
        status = "Valid" if self.is_valid else ("Used" if self.is_used else "Expired")
        return f"Employee Add OTP for {self.admin_user.username} - {status}"




class Division(models.Model):
    """
    Organizational divisions/departments for structuring employees.
    Linked to a specific company.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    company_name = models.CharField(max_length=200, help_text="Company this division belongs to")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='managed_divisions',
                                help_text="Division manager/head")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['company_name', 'name']
        unique_together = ['name', 'company_name']
    
    def __str__(self):
        return f"{self.name} - {self.company_name}"


class AssetCategory(models.Model):
    """
    Categories for organizing assets (e.g., IT Equipment, Vehicles, Furniture, etc.)
    """
    CATEGORY_TYPES = [
        ('it_equipment', 'IT Equipment'),
        ('office_furniture', 'Office Furniture'),
        ('vehicles', 'Vehicles'),
        ('machinery', 'Machinery & Tools'),
        ('property', 'Property & Buildings'),
        ('software', 'Software Licenses'),
        ('communication', 'Communication Devices'),
        ('other', 'Other Assets'),
    ]
    
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPES, default='other')
    description = models.TextField(blank=True)
    company_name = models.CharField(max_length=200, help_text="Company this category belongs to")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['company_name', 'name']
        unique_together = ['name', 'company_name']
        verbose_name_plural = 'Asset Categories'
    
    def __str__(self):
        return f"{self.name} ({self.company_name})"


class Asset(models.Model):
    """
    Main asset tracking model for ADMP.
    Tracks company assets, equipment, and property with full lifecycle management.
    """
    STATUS_CHOICES = [
        ('active', 'Active/In Use'),
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired/Disposed'),
        ('lost', 'Lost/Stolen'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged'),
    ]

    asset_tag = models.CharField(max_length=100, unique=True, 
                                 help_text="Unique asset identifier/tag")
    name = models.CharField(max_length=200, help_text="Asset name/description")
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, 
                                 related_name='assets')

    serial_number = models.CharField(max_length=200, blank=True, 
                                    help_text="Manufacturer serial number")
    model = models.CharField(max_length=200, blank=True, 
                            help_text="Model number/name")
    manufacturer = models.CharField(max_length=200, blank=True)

    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                       help_text="Original purchase cost")
    current_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                       help_text="Current estimated value")
    warranty_expiry = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_assets',
                                   help_text="Employee this asset is assigned to")
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='assets',
                                help_text="Division this asset belongs to")
    location = models.CharField(max_length=300, blank=True,
                               help_text="Physical location (building/room/desk)")

    company_name = models.CharField(max_length=200, help_text="Company that owns this asset")

    notes = models.TextField(blank=True, help_text="Additional notes, maintenance history, etc.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_assets')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company_name', 'status']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['asset_tag']),
        ]
    
    def __str__(self):
        return f"{self.asset_tag} - {self.name}"
    
    @property
    def is_assigned(self):
        return self.assigned_to is not None
    
    @property
    def depreciation(self):
        """Calculate depreciation if both costs are available"""
        if self.purchase_cost and self.current_value:
            return self.purchase_cost - self.current_value
        return None
    
    @property
    def warranty_status(self):
        """Check warranty status"""
        if not self.warranty_expiry:
            return 'unknown'
        if timezone.now().date() < self.warranty_expiry:
            return 'valid'
        return 'expired'




class OnboardingLog(models.Model):
    """
    Audit log for employee onboarding and offboarding events.
    Tracks who was onboarded/offboarded, by whom, and when.
    """
    ACTION_CHOICES = [
        ('onboard', 'Onboarded'),
        ('offboard', 'Offboarded'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name='onboarding_history',
                                 help_text="The employee that was onboarded/offboarded")
    employee_name = models.CharField(max_length=200, help_text="Stored name (persists after deletion)")
    employee_email = models.EmailField(help_text="Stored email (persists after deletion)")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                     related_name='onboarding_actions_performed',
                                     help_text="Who performed the onboarding/offboarding")
    performed_by_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    role_assigned = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    reason = models.TextField(blank=True, help_text="Reason for offboarding")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Onboarding Log"
        verbose_name_plural = "Onboarding Logs"
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.employee_name} by {self.performed_by_name}"


class OffboardingRequest(models.Model):
    """
    Offboarding request from company CEO/executive.
    Only system administrators (programmers) can APPROVE and execute offboarding.
    Company admins can REQUEST but NOT directly delete employees.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved & Processed'),
        ('rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='offboarding_requests',
                                 help_text="Employee to be offboarded")
    employee_name = models.CharField(max_length=200)
    employee_email = models.EmailField()
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                     related_name='offboarding_requests_made',
                                     help_text="CEO/Executive who requested offboarding")
    requested_by_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    reason = models.TextField(help_text="Reason for offboarding this employee")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='offboarding_processed',
                                     help_text="System admin who processed the request")
    processed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, help_text="System admin notes on the decision")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Offboarding Request"
        verbose_name_plural = "Offboarding Requests"
    
    def __str__(self):
        return f"Offboard {self.employee_name} - {self.get_status_display()}"




class Product(models.Model):
    """Product/service catalog for building quotes and deals."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, blank=True, help_text="Stock Keeping Unit / Product Code")
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Unit price in ZAR")
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Cost price for margin calculation")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00, help_text="VAT rate (default 15% for SA)")
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True, help_text="Product category (e.g. Software, Service, Hardware)")
    unit = models.CharField(max_length=50, default='each', help_text="Unit of measure (each, hour, month, licence)")
    company_name = models.CharField(max_length=200, help_text="Company that owns this product")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        unique_together = ['company_name', 'sku']

    def __str__(self):
        return f"{self.name} - R{self.price}"

    @property
    def margin(self):
        if self.cost and self.price:
            return ((self.price - self.cost) / self.price * 100)
        return None

    @property
    def price_incl_tax(self):
        return round(self.price * (1 + self.tax_rate / 100), 2)


class LineItem(models.Model):
    """Line item linking a product to a deal (quote/invoice building)."""
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='line_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='line_items')
    description = models.CharField(max_length=300, blank=True, help_text="Override product description for this line")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price per unit (copied from product, can be overridden)")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def subtotal(self):
        base = self.quantity * self.unit_price
        discount = base * (self.discount_percent / 100)
        return round(base - discount, 2)

    @property
    def tax_amount(self):
        return round(self.subtotal * (self.tax_rate / 100), 2)

    @property
    def total(self):
        return round(self.subtotal + self.tax_amount, 2)




class EmailTemplate(models.Model):
    """Reusable email templates with merge fields."""
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome'),
        ('follow_up', 'Follow-Up'),
        ('proposal', 'Proposal'),
        ('thank_you', 'Thank You'),
        ('newsletter', 'Newsletter'),
        ('custom', 'Custom'),
    ]
    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES, default='custom')
    subject = models.CharField(max_length=300)
    body_html = models.TextField(help_text="HTML body. Use {{first_name}}, {{last_name}}, {{company}}, {{email}} as merge fields.")
    company_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='email_templates')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class EmailCampaign(models.Model):
    """Bulk email campaign targeting a segment of contacts."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('paused', 'Paused'),
        ('failed', 'Failed'),
    ]
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    body_html = models.TextField()
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    recipient_filter = models.JSONField(default=dict, blank=True,
        help_text="Filter criteria: {company_id, tags, all}")
    recipient_ids = models.JSONField(default=list, blank=True,
        help_text="Explicit list of contact IDs")
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    open_count = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)
    bounce_count = models.IntegerField(default=0)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    company_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='email_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @property
    def open_rate(self):
        if self.sent_count > 0:
            return round(self.open_count / self.sent_count * 100, 1)
        return 0

    @property
    def click_rate(self):
        if self.sent_count > 0:
            return round(self.click_count / self.sent_count * 100, 1)
        return 0


class CampaignRecipient(models.Model):
    """Per-contact tracking for a campaign."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('bounced', 'Bounced'),
        ('failed', 'Failed'),
    ]
    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, related_name='recipients')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['campaign', 'contact']
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.contact} - {self.campaign.name} ({self.status})"




class Workflow(models.Model):
    """Automation workflow: IF trigger THEN action(s)."""
    TRIGGER_CHOICES = [
        ('deal_stage_change', 'Deal Stage Changes'),
        ('deal_created', 'New Deal Created'),
        ('deal_value_above', 'Deal Value Exceeds Threshold'),
        ('contact_created', 'New Contact Added'),
        ('contact_no_activity', 'Contact Inactive For X Days'),
        ('ticket_created', 'New Ticket Created'),
        ('ticket_overdue', 'Ticket Past Due Date'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trigger_type = models.CharField(max_length=30, choices=TRIGGER_CHOICES)
    trigger_config = models.JSONField(default=dict, blank=True,
        help_text="Trigger parameters, e.g. {stage_from: 'lead', stage_to: 'qualified'} or {days: 14}")
    is_active = models.BooleanField(default=True)
    company_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='workflows')
    run_count = models.IntegerField(default=0)
    last_run_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.get_trigger_type_display()})"


class WorkflowAction(models.Model):
    """Single action within a workflow (executed in order)."""
    ACTION_TYPES = [
        ('send_email', 'Send Email'),
        ('create_task', 'Create Task/Ticket'),
        ('notify_user', 'Send Notification'),
        ('change_stage', 'Change Deal Stage'),
        ('assign_user', 'Assign To User'),
        ('add_note', 'Add Note/Activity'),
        ('wait', 'Wait (Delay)'),
    ]
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_config = models.JSONField(default=dict,
        help_text="Action parameters. E.g. {template_id: 1, delay_hours: 24, stage: 'proposal'}")
    order = models.PositiveIntegerField(default=0, help_text="Execution order (0 = first)")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order}: {self.get_action_type_display()}"


class WorkflowLog(models.Model):
    """Execution log for workflow runs."""
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='logs')
    trigger_entity_type = models.CharField(max_length=50)
    trigger_entity_id = models.IntegerField()
    trigger_entity_name = models.CharField(max_length=255, blank=True)
    actions_executed = models.JSONField(default=list, help_text="List of action results")
    status = models.CharField(max_length=20, choices=[
        ('success', 'Success'), ('partial', 'Partial'), ('failed', 'Failed')
    ], default='success')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.workflow.name} - {self.status} ({self.created_at})"




class DashboardWidget(models.Model):
    """Custom dashboard widget configuration per user."""
    WIDGET_TYPES = [
        ('stat_card', 'Stat Card'),
        ('pipeline_chart', 'Pipeline Chart'),
        ('revenue_chart', 'Revenue Over Time'),
        ('activity_feed', 'Activity Feed'),
        ('deal_funnel', 'Deal Funnel'),
        ('top_contacts', 'Top Contacts'),
        ('campaign_stats', 'Campaign Stats'),
        ('team_leaderboard', 'Team Leaderboard'),
        ('tasks_due', 'Tasks Due Today'),
        ('recent_deals', 'Recent Deals'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    widget_type = models.CharField(max_length=30, choices=WIDGET_TYPES)
    title = models.CharField(max_length=100)
    config = models.JSONField(default=dict, blank=True,
        help_text="Widget-specific configuration (date range, filters, etc)")
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    width = models.IntegerField(default=1, help_text="Grid columns (1-4)")
    height = models.IntegerField(default=1, help_text="Grid rows (1-3)")
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position_y', 'position_x']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class DashboardLayout(models.Model):
    """Saved dashboard layout preset."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_layouts')
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    widget_config = models.JSONField(default=list,
        help_text="Serialized list of widget configs for this layout")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"