from rest_framework import serializers
from .models import (Contact, Company, Deal, ActivityLog, Ticket, Notification, UserProfile,
                     Asset, AssetCategory, Division, OnboardingLog, OffboardingRequest,
                     Product, LineItem, EmailTemplate, EmailCampaign, CampaignRecipient,
                     Workflow, WorkflowAction, WorkflowLog, DashboardWidget, DashboardLayout)
from django.contrib.auth.models import User
from django.core.validators import validate_email
import phonenumbers
from phonenumbers import NumberParseException


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        if value:
            validate_email(value)
        return value
    
    def validate_phone(self, value):
        if value:
            try:
                parsed = phonenumbers.parse(value, "ZA")
                if not phonenumbers.is_valid_number(parsed):
                    raise serializers.ValidationError("Invalid phone number format.")
            except NumberParseException:
                raise serializers.ValidationError("Invalid phone number format.")
        return value


class ContactSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    health_score = serializers.ReadOnlyField()
    health_status = serializers.ReadOnlyField()
    next_step_suggestion = serializers.ReadOnlyField()

    PERSONAL_EMAIL_DOMAINS = {
        'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com',
        'live.com', 'msn.com', 'aol.com', 'protonmail.com', 'zoho.com',
        'yahoo.co.uk', 'ymail.com', 'googlemail.com'
    }

    class Meta:
        model = Contact
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_self_employed',
            'company_direct_line',
            'company_name_manual',
            'company',
            'company_name',
            'last_contact_date',
            'health_score',
            'health_status',
            'next_step_suggestion',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'company_name',
            'health_score',
            'health_status',
            'next_step_suggestion',
            'created_at',
            'updated_at'
        ]

    def validate_email(self, value):
        validate_email(value)
        user = self.context['request'].user
        instance = self.instance
        if Contact.objects.filter(user=user, email=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("You already have a contact with this email.")
        return value

    def _validate_za_number(self, value):
        if value:
            try:
                parsed = phonenumbers.parse(value, "ZA")
                if not phonenumbers.is_valid_number(parsed):
                    raise serializers.ValidationError("Invalid phone number format.")
            except NumberParseException:
                raise serializers.ValidationError("Invalid phone number format.")
        return value

    def validate_phone(self, value):
        return self._validate_za_number(value)

    def validate_company_direct_line(self, value):
        return self._validate_za_number(value)

    def validate(self, attrs):
        request = self.context['request']
        company = attrs.get('company')

        manual_name_raw = attrs.get('company_name_manual', None)
        if manual_name_raw is None and self.instance:
            manual_name_raw = self.instance.company_name_manual
        if manual_name_raw is None:
            manual_name_raw = ''
        manual_name = manual_name_raw.strip()

        first_name = attrs.get('first_name')
        if first_name is None and self.instance:
            first_name = self.instance.first_name
        last_name = attrs.get('last_name')
        if last_name is None and self.instance:
            last_name = self.instance.last_name

        email = attrs.get('email') or (self.instance.email if self.instance else '')
        is_self_employed = attrs.get('is_self_employed')
        if is_self_employed is None and self.instance:
            is_self_employed = self.instance.is_self_employed
        company_direct_line = attrs.get('company_direct_line')
        if company_direct_line is None and self.instance:
            company_direct_line = self.instance.company_direct_line

        if company and company.user != request.user:
            raise serializers.ValidationError({'company': 'Selected company does not belong to your workspace.'})

        has_existing_manual = bool(self.instance and self.instance.company_name_manual)
        if not manual_name and not has_existing_manual:
            if is_self_employed:
                composed_name = f"{(first_name or '').strip()} {(last_name or '').strip()}".strip()
                manual_name = f"{composed_name} (Self-Employed)" if composed_name else 'Self-Employed'
            else:
                raise serializers.ValidationError({'company_name_manual': 'Please capture the company name for this contact.'})

        if not is_self_employed and email:
            domain = email.split('@')[-1].lower()
            if domain in self.PERSONAL_EMAIL_DOMAINS:
                raise serializers.ValidationError({
                    'email': 'Please use a professional/company email address unless the contact is self-employed.'
                })

        if not is_self_employed and not company_direct_line:
            raise serializers.ValidationError({
                'company_direct_line': 'Corporate contacts must include a direct company line.'
            })

        attrs['company_name_manual'] = manual_name
        attrs['is_self_employed'] = bool(is_self_employed)

        if attrs['is_self_employed'] and company_direct_line is None:
            attrs['company_direct_line'] = ''
        elif company_direct_line is not None:
            attrs['company_direct_line'] = company_direct_line

        return attrs


class DealSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.__str__', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    total_hours_display = serializers.ReadOnlyField()
    current_timer_hours = serializers.ReadOnlyField()
    
    class Meta:
        model = Deal
        fields = [
            'id',
            'title',
            'contact',
            'contact_name',
            'company',
            'company_name',
            'value',
            'stage',
            'time_spent_hours',
            'timer_running',
            'timer_started_at',
            'total_hours_display',
            'current_timer_hours',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'contact_name', 'company_name', 'total_hours_display', 'current_timer_hours', 'created_at', 'updated_at']
    
    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Deal value must be greater than zero.")
        return value

    def validate(self, attrs):
        request = self.context['request']
        contact = attrs.get('contact') or (self.instance.contact if self.instance else None)
        company = attrs.get('company') or (self.instance.company if self.instance else None)

        if contact is None:
            raise serializers.ValidationError({'contact': 'Contact is required for a deal.'})

        if contact.user != request.user:
            raise serializers.ValidationError({'contact': 'Selected contact does not belong to your workspace.'})

        if company is None:
            raise serializers.ValidationError({'company': 'Company is required for a deal.'})

        if company.user != request.user:
            raise serializers.ValidationError({'company': 'Selected company does not belong to your workspace.'})

        if not contact.company:
            raise serializers.ValidationError({'contact': 'Link this contact to a company before creating a deal.'})

        if contact.company != company:
            raise serializers.ValidationError({'company': 'Contact must belong to the selected company.'})

        return attrs


class ActivityLogSerializer(serializers.ModelSerializer):
    """
    Activity log serializer.
    FREE tier: Returns last 5 activities
    LUXURY+ tier: Returns all activities
    """
    class Meta:
        model = ActivityLog
        fields = ['id', 'action', 'entity_type', 'entity_id', 'entity_name', 'details', 'created_at']
        read_only_fields = fields


class TicketSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='deal.contact.__str__', read_only=True)
    company_name = serializers.CharField(source='deal.company.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'deal',
            'contact_name',
            'company_name',
            'created_by',
            'created_by_username',
            'assigned_to',
            'assigned_to_username',
            'priority',
            'category',
            'department',
            'status',
            'started_at',
            'due_at',
            'completed_at',
            'duration_seconds',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'created_by', 'created_by_username', 'assigned_to_username', 'created_at', 'updated_at',
        ]

    def validate(self, attrs):
        request = self.context['request']
        deal = attrs.get('deal') or (self.instance.deal if self.instance else None)
        assigned_to = attrs.get('assigned_to') or (self.instance.assigned_to if self.instance else None)

        if deal and deal.user != request.user and not request.user.is_staff and not request.user.is_superuser:
            raise serializers.ValidationError({'deal': 'Selected deal does not belong to your workspace.'})

        if not assigned_to:
            raise serializers.ValidationError({'assigned_to': 'Please assign the ticket to a user.'})

        user_profile = getattr(request.user, 'profile', None)
        if user_profile and user_profile.is_admin and not request.user.is_superuser and not request.user.is_staff:
            company_name = user_profile.company_name
            assigned_profile = getattr(assigned_to, 'profile', None)
            if not assigned_profile or assigned_profile.company_name != company_name:
                raise serializers.ValidationError({'assigned_to': 'Assigned user must be within your company.'})

        return attrs


class NotificationSerializer(serializers.ModelSerializer):
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'recipient_username',
            'title',
            'message',
            'entity_type',
            'entity_id',
            'meta',
            'read_at',
            'created_at',
        ]
        read_only_fields = ['id', 'recipient_username', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employee management (ADMP) - includes full user and profile details"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    full_name = serializers.SerializerMethodField()
    reports_to_name = serializers.SerializerMethodField()
    onboarded_by_name = serializers.SerializerMethodField()
    can_onboard = serializers.ReadOnlyField()
    onboarding_allowed_roles = serializers.ReadOnlyField()
    direct_reports_count = serializers.SerializerMethodField()
    onboarding_status = serializers.SerializerMethodField()
    onboarding_status_label = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'is_active',
            'role',
            'tier',
            'phone',
            'company_name',
            'job_title',
            'department',
            'division',
            'employee_id',
            'date_of_birth',
            'address',
            'emergency_contact_name',
            'emergency_contact_phone',
            'start_date',
            'notes',
            'is_banned',
            'ban_reason',
            'payment_status',
            'can_add_employees',
            'reports_to',
            'reports_to_name',
            'onboarded_by',
            'onboarded_by_name',
            'onboarded_at',
            'is_offboarded',
            'offboarded_at',
            'can_onboard',
            'onboarding_allowed_roles',
            'direct_reports_count',
            'onboarding_status',
            'onboarding_status_label',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'tier', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    
    def get_reports_to_name(self, obj):
        if obj.reports_to:
            return f"{obj.reports_to.first_name} {obj.reports_to.last_name}".strip() or obj.reports_to.username
        return None
    
    def get_onboarded_by_name(self, obj):
        if obj.onboarded_by:
            return f"{obj.onboarded_by.first_name} {obj.onboarded_by.last_name}".strip() or obj.onboarded_by.username
        return None
    
    def get_direct_reports_count(self, obj):
        return UserProfile.objects.filter(reports_to=obj.user, is_offboarded=False).count()

    def get_onboarding_status(self, obj):
        if obj.is_offboarded:
            return 'offboarded'
        if obj.requires_password_reset:
            return 'pending_first_login'
        return 'onboarded'

    def get_onboarding_status_label(self, obj):
        status = self.get_onboarding_status(obj)
        labels = {
            'pending_first_login': 'Pending First Login',
            'onboarded': 'Onboarded',
            'offboarded': 'Offboarded',
        }
        return labels.get(status, 'Onboarded')


class EmployeeCreateSerializer(serializers.Serializer):
    """Serializer for creating new employees"""
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    company_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    job_title = serializers.CharField(max_length=100, required=False, allow_blank=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True)
    employee_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d', '%Y/%m/%d'])
    address = serializers.CharField(required=False, allow_blank=True)
    emergency_contact_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    emergency_contact_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    start_date = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d', '%Y/%m/%d'])
    notes = serializers.CharField(required=False, allow_blank=True)
    division = serializers.PrimaryKeyRelatedField(
        queryset=Division.objects.all(), required=False, allow_null=True
    )
    reports_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    
    def validate_email(self, value):
        normalized = (value or '').strip().lower()
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError("Email already exists")
        validate_email(normalized)
        return normalized
    
    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if User.objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        attrs['username'] = email
        attrs['email'] = email
        return attrs




class OnboardingLogSerializer(serializers.ModelSerializer):
    """Serializer for onboarding/offboarding audit logs"""
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = OnboardingLog
        fields = [
            'id', 'employee', 'employee_name', 'employee_email',
            'action', 'action_display', 'performed_by', 'performed_by_name',
            'company_name', 'role_assigned', 'department', 'reason', 'created_at'
        ]
        read_only_fields = fields


class OffboardingRequestSerializer(serializers.ModelSerializer):
    """Serializer for offboarding requests"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    processed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OffboardingRequest
        fields = [
            'id', 'employee', 'employee_name', 'employee_email',
            'requested_by', 'requested_by_name', 'company_name',
            'reason', 'status', 'status_display',
            'processed_by', 'processed_by_name', 'processed_at',
            'admin_notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_processed_by_name(self, obj):
        if obj.processed_by:
            return f"{obj.processed_by.first_name} {obj.processed_by.last_name}".strip() or obj.processed_by.username
        return None


class OffboardingRequestCreateSerializer(serializers.Serializer):
    """Serializer for creating offboarding requests"""
    employee_id = serializers.IntegerField()
    reason = serializers.CharField(min_length=10)




class DivisionSerializer(serializers.ModelSerializer):
    """Serializer for organizational divisions"""
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True, allow_null=True)
    manager_email = serializers.EmailField(source='manager.email', read_only=True, allow_null=True)
    employee_count = serializers.SerializerMethodField()
    asset_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Division
        fields = ['id', 'name', 'description', 'company_name', 'manager', 'manager_name', 
                 'manager_email', 'employee_count', 'asset_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_employee_count(self, obj):
        return obj.employees.count()
    
    def get_asset_count(self, obj):
        return obj.assets.count()


class AssetCategorySerializer(serializers.ModelSerializer):
    """Serializer for asset categories"""
    asset_count = serializers.SerializerMethodField()
    category_type_display = serializers.CharField(source='get_category_type_display', read_only=True)
    
    class Meta:
        model = AssetCategory
        fields = ['id', 'name', 'category_type', 'category_type_display', 'description', 
                 'company_name', 'asset_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_asset_count(self, obj):
        return obj.assets.count()


class AssetSerializer(serializers.ModelSerializer):
    """Main serializer for assets with full details"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_type = serializers.CharField(source='category.category_type', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True, allow_null=True)
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True, allow_null=True)
    division_name = serializers.CharField(source='division.name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)
    warranty_status = serializers.ReadOnlyField()
    is_assigned = serializers.ReadOnlyField()
    depreciation = serializers.ReadOnlyField()
    
    class Meta:
        model = Asset
        fields = [
            'id', 'asset_tag', 'name', 'category', 'category_name', 'category_type',
            'serial_number', 'model', 'manufacturer',
            'purchase_date', 'purchase_cost', 'current_value', 'warranty_expiry',
            'status', 'status_display', 'condition', 'condition_display',
            'assigned_to', 'assigned_to_name', 'assigned_to_email',
            'division', 'division_name', 'location', 'company_name',
            'notes', 'warranty_status', 'is_assigned', 'depreciation',
            'created_at', 'updated_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def validate_asset_tag(self, value):
        """Ensure asset tag is unique"""
        instance = self.instance
        if Asset.objects.filter(asset_tag=value).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError("Asset tag must be unique")
        return value


class AssetListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for asset list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Asset
        fields = ['id', 'asset_tag', 'name', 'category_name', 'status', 'status_display',
                 'assigned_to_name', 'location', 'created_at']




class ProductSerializer(serializers.ModelSerializer):
    margin = serializers.ReadOnlyField()
    price_incl_tax = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'sku', 'price', 'cost', 'tax_rate',
            'is_active', 'category', 'unit', 'company_name', 'margin',
            'price_incl_tax', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LineItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.ReadOnlyField()
    tax_amount = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()

    class Meta:
        model = LineItem
        fields = [
            'id', 'deal', 'product', 'product_name', 'description',
            'quantity', 'unit_price', 'discount_percent', 'tax_rate',
            'subtotal', 'tax_amount', 'total', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']




class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = [
            'id', 'name', 'template_type', 'subject', 'body_html',
            'company_name', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CampaignRecipientSerializer(serializers.ModelSerializer):
    contact_name = serializers.SerializerMethodField()
    contact_email = serializers.CharField(source='contact.email', read_only=True)

    class Meta:
        model = CampaignRecipient
        fields = ['id', 'contact', 'contact_name', 'contact_email', 'status',
                  'sent_at', 'opened_at', 'clicked_at']

    def get_contact_name(self, obj):
        return f"{obj.contact.first_name} {obj.contact.last_name}"


class EmailCampaignSerializer(serializers.ModelSerializer):
    open_rate = serializers.ReadOnlyField()
    click_rate = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = EmailCampaign
        fields = [
            'id', 'name', 'subject', 'body_html', 'template', 'status',
            'recipient_filter', 'recipient_ids', 'total_recipients',
            'sent_count', 'open_count', 'click_count', 'bounce_count',
            'open_rate', 'click_rate', 'scheduled_at', 'sent_at',
            'company_name', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'sent_count', 'open_count', 'click_count',
                           'bounce_count', 'created_by', 'created_at', 'updated_at']




class WorkflowActionSerializer(serializers.ModelSerializer):
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)

    class Meta:
        model = WorkflowAction
        fields = ['id', 'action_type', 'action_type_display', 'action_config', 'order']


class WorkflowLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowLog
        fields = ['id', 'trigger_entity_type', 'trigger_entity_id',
                  'trigger_entity_name', 'actions_executed', 'status',
                  'error_message', 'created_at']


class WorkflowSerializer(serializers.ModelSerializer):
    actions = WorkflowActionSerializer(many=True, read_only=True)
    trigger_type_display = serializers.CharField(source='get_trigger_type_display', read_only=True)

    class Meta:
        model = Workflow
        fields = [
            'id', 'name', 'description', 'trigger_type', 'trigger_type_display',
            'trigger_config', 'is_active', 'company_name', 'run_count',
            'last_run_at', 'actions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'run_count', 'last_run_at', 'created_at', 'updated_at']




class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = [
            'id', 'widget_type', 'title', 'config', 'position_x',
            'position_y', 'width', 'height', 'is_visible',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardLayout
        fields = ['id', 'name', 'is_default', 'widget_config',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
