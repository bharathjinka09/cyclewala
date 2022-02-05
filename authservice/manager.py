import hashlib
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

class UserManager(BaseUserManager):

    def _create_user(self, email, password,is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def set_default_password(self, id, notify=False):
        try:
            user = self.get(id=id)
        except ObjectDoesNotExist as e:
            raise ValidationError("User not found")

        password = self.make_random_password()
        md5_password = hashlib.md5(password.encode("utf")).hexdigest()
        user.set_password(md5_password)
        user.save()
        return password
