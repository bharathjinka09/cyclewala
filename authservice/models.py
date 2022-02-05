import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone

from django.db.models.deletion import CASCADE
from authservice.manager import UserManager

from utils.choices import GenderType


class User(AbstractBaseUser, PermissionsMixin):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    is_email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GenderType.choices,null=True, blank=True, validators=[GenderType.validator])
    dob = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=18, null=True, blank=True, validators=[MinLengthValidator(8)])
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __unicode(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)

        if not self.first_name:
            full_name = self.name or ''

        return full_name.strip()
    
    @property
    def cleaned_name(self):
        return self.get_full_name()

    def mark_email_verified(self):
        self.is_email_verified = True
        if self.signup_at is None:
            self.signup_at = timezone.now()
        self.email_verified_at = timezone.now()

    def mark_phone_verified(self):
        if not self.phone_number:
            return None
        if self.phone_verified_at:
            return None
        self.phone_verified_at =  timezone.now()
        self.save()


    @property
    def encoded_email(self):
        email = self.email
        return f"{email[:2]}xxxxxx{email[-3:]}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.name and self.first_name:
            self.name = self.first_name
            if self.last_name:
                self.name = self.first_name + " " + self.last_name
        return super(User, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)