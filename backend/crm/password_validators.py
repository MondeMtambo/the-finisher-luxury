"""
Custom password validators for THE FINISHER LUXURY.
Enforces strong password policy: 8+ chars, uppercase, lowercase, number, special character.
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercaseValidator:
    """Validate that the password contains at least one uppercase letter."""

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least 1 uppercase letter (A–Z)."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 uppercase letter (A–Z).")


class LowercaseValidator:
    """Validate that the password contains at least one lowercase letter."""

    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("Password must contain at least 1 lowercase letter (a–z)."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 lowercase letter (a–z).")


class NumberValidator:
    """Validate that the password contains at least one digit."""

    def validate(self, password, user=None):
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("Password must contain at least 1 number (0–9)."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 number (0–9).")


class SpecialCharacterValidator:
    """Validate that the password contains at least one special character."""

    def validate(self, password, user=None):
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?`~]', password):
            raise ValidationError(
                _("Password must contain at least 1 special character (!@#$%^&*...)."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 special character (!@#$%^&*...).")
