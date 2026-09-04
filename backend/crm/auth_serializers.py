"""
Authentication serializers for user registration, login, OTP password reset
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import timedelta
from rest_framework.validators import UniqueValidator
from .models import UserProfile
from .utils import get_client_ip, normalize_company_name

class RegisterSerializer(serializers.ModelSerializer):
    """
    Professional user registration serializer with company details and business intelligence.
    LUXURY Edition: Each user gets their own isolated CRM data.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already registered.")]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    company_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    tier = serializers.ChoiceField(
        choices=['free', 'sport', 'luxury', 'premium'],
        default='luxury',
        required=False
    )
    is_unlisted_company = serializers.BooleanField(required=False, default=False)

    job_title = serializers.CharField(required=True)
    industry = serializers.CharField(required=False, allow_blank=True)
    company_size = serializers.CharField(required=False, allow_blank=True)
    referral_source = serializers.CharField(required=False, allow_blank=True)
    business_website = serializers.URLField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True, default='ZA')
    intended_use_case = serializers.CharField(required=False, allow_blank=True)
    current_crm = serializers.CharField(required=False, allow_blank=True)
    expected_contacts = serializers.CharField(required=False, allow_blank=True)
    marketing_consent = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email', 'first_name', 'last_name', 
            'company_name', 'phone', 'tier', 'is_unlisted_company', 'job_title', 'industry', 'company_size', 
            'referral_source', 'business_website', 'country', 'intended_use_case', 
            'current_crm', 'expected_contacts', 'marketing_consent'
        )
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        email = (attrs.get('email') or '').strip().lower()
        attrs['email'] = email
        if User.objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError({"email": "An account already exists for this email."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        company_name = normalize_company_name(validated_data.pop('company_name', ''))
        phone = validated_data.pop('phone', '')
        tier = validated_data.pop('tier', 'luxury')
        is_unlisted_company = validated_data.pop('is_unlisted_company', False)

        job_title = validated_data.pop('job_title', '')
        industry = validated_data.pop('industry', '')
        company_size = validated_data.pop('company_size', '')
        referral_source = validated_data.pop('referral_source', '')
        business_website = validated_data.pop('business_website', '')
        country = validated_data.pop('country', 'ZA')
        intended_use_case = validated_data.pop('intended_use_case', '')
        current_crm = validated_data.pop('current_crm', '')
        expected_contacts = validated_data.pop('expected_contacts', '')
        marketing_consent = validated_data.pop('marketing_consent', False)

        request = self.context.get('request')
        registration_ip = get_client_ip(request) if request else None
        
        email_as_username = (validated_data['email'] or '').strip().lower()

        user = User.objects.create_user(
            username=email_as_username,
            email=email_as_username,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        if hasattr(user, 'profile'):
            profile = user.profile

            if not company_name or not company_name.strip():
                company_name = f"{user.first_name} {user.last_name} Company".strip()
            profile.company_name = company_name
            profile.phone = phone
            profile.tier = tier
            profile.registration_ip = registration_ip
            profile.last_login_ip = registration_ip

            # Enforce 15-Business VIP Trial Cohort Cap to protect compute resources
            from .models import Organization, OrganizationSubscription
            TRIAL_COHORT_LIMIT = 15
            active_trials_count = Organization.objects.filter(subscription_tier='trial', is_active=True).count()
            if active_trials_count >= TRIAL_COHORT_LIMIT:
                raise serializers.ValidationError({
                    'error': 'The VIP 7-Day Free Trial cohort is currently at maximum capacity (15/15 businesses enrolled). Please contact executive support or join the waitlist for Batch #2.'
                })

            # Provision Tenant Organization with 7-Day VIP Trial
            org, _ = Organization.objects.get_or_create(
                name=company_name,
                defaults={
                    'subscription_tier': 'trial',
                    'trial_start_date': timezone.now(),
                    'trial_end_date': timezone.now() + timedelta(days=7),
                    'is_active': True,
                }
            )
            profile.organization = org
            OrganizationSubscription.objects.get_or_create(
                organization=org,
                defaults={
                    'status': 'trial',
                    'current_period_start': timezone.now(),
                    'current_period_end': timezone.now() + timedelta(days=7),
                }
            )

            profile.payment_status = 'trial'
            profile.trial_ends_at = timezone.now() + timedelta(days=7)

            profile.job_title = job_title
            profile.industry = industry
            profile.company_size = company_size
            profile.referral_source = referral_source
            profile.business_website = business_website
            profile.country = country
            profile.intended_use_case = intended_use_case
            profile.current_crm = current_crm
            profile.expected_contacts = expected_contacts
            profile.marketing_consent = marketing_consent
            profile.terms_accepted_at = timezone.now()  # Record when terms were accepted

            profile.role = 'admin'
            profile.save()

            # Ensure Company object exists for this user and organization
            from .models import Company
            if company_name:
                Company.objects.get_or_create(
                    user=user, 
                    name=company_name,
                    defaults={'organization': org}
                )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    User profile serializer with company info and role.
    """
    company_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    requires_password_reset = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'date_joined',
            'company_name', 'phone', 'tier', 'role', 'permissions', 'job_title', 'department', 'is_staff', 'is_superuser',
            'requires_password_reset'
        )
        read_only_fields = ('id', 'date_joined', 'is_staff', 'is_superuser')
    
    def get_company_name(self, obj):
        return obj.profile.company_name if hasattr(obj, 'profile') else ''
    
    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, 'profile') else ''
    
    def get_tier(self, obj):
        return obj.profile.get_tier_display() if hasattr(obj, 'profile') else 'CLASSIC (Free)'
    
    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return {
                'value': obj.profile.role,
                'display': obj.profile.get_role_display()
            }
        return {'value': 'user', 'display': 'Standard User'}
    
    def get_permissions(self, obj):
        if hasattr(obj, 'profile'):
            return {
                'can_stop_deal_timers': obj.profile.can_stop_deal_timers,
                'can_delete_deals': obj.profile.can_delete_deals,
                'can_manage_users': obj.profile.can_manage_users,
                'is_admin': obj.profile.is_admin,
                'is_manager': obj.profile.is_manager,
                'is_supervisor': obj.profile.is_supervisor
            }
        return {
            'can_stop_deal_timers': False,
            'can_delete_deals': False,
            'can_manage_users': False,
            'is_admin': False,
            'is_manager': False,
            'is_supervisor': False
        }

    def get_job_title(self, obj):
        return getattr(getattr(obj, 'profile', None), 'job_title', '')

    def get_department(self, obj):
        return getattr(getattr(obj, 'profile', None), 'department', '')

    def get_requires_password_reset(self, obj):
        return getattr(getattr(obj, 'profile', None), 'requires_password_reset', False)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Password change serializer for authenticated users.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Request password reset via email.
    """
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Confirm password reset with OTP code.
    """
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)
    password = serializers.CharField(required=True, validators=[validate_password])
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
