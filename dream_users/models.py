import binascii
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

TOKEN_LENGTH = 64
RESET_TOKEN_LENGTH = 10
CONFIRM_EMAIL_TOKEN_LENGTH = 128


class User(AbstractUser):
    TYPE_FREE = 1
    TYPE_PREMIUM = 2
    TYPE_EXPIRED = 3
    TYPE_CHOICES = (
        (TYPE_FREE, 'Free'),
        (TYPE_PREMIUM, 'Premium'),
        (TYPE_EXPIRED, 'Expired'),
    )

    STATUS_WAIT_CONFIRM = 1
    STATUS_CONFIRMED = 2
    STATUS_CHOICES = (
        (STATUS_WAIT_CONFIRM, 'Wait Confirm'),
        (STATUS_CONFIRMED, 'Confirmed'),
    )

    username = models.CharField(_('username'), max_length=150)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    user_type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_FREE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_WAIT_CONFIRM)
    facebook_id = models.CharField(max_length=150, blank=True, null=True, unique=True)
    line_id = models.CharField(max_length=150, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return 'User: {}'.format(self.username)


class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=TOKEN_LENGTH, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        db_table = 'token'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        num_bytes = TOKEN_LENGTH // 2
        return binascii.hexlify(os.urandom(num_bytes)).decode()

    def __str__(self):
        return 'Token (user {}): {}'.format(self.user_id, self.key)


class ResetToken(models.Model):
    reset_token = models.CharField(_("Reset token"), primary_key=True, max_length=RESET_TOKEN_LENGTH)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reset_token',
        on_delete=models.CASCADE, verbose_name=_('user')
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        db_table = 'reset_token'

    def save(self, *args, **kwargs):
        if not self.reset_token:
            self.reset_token = self.generate_reset_token()
        return super(ResetToken, self).save(*args, **kwargs)

    def generate_reset_token(self):
        num_bytes = RESET_TOKEN_LENGTH // 2
        return binascii.hexlify(os.urandom(num_bytes)).decode()

    def __str__(self):
        return 'ResetToken (user {}): {}'.format(self.user_id, self.reset_token)


class ConfirmEmailToken(models.Model):
    token = models.CharField(_("token"), primary_key=True, max_length=CONFIRM_EMAIL_TOKEN_LENGTH)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='confirm_email_token',
        on_delete=models.CASCADE, verbose_name=_('user')
    )
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        db_table = 'confirm_email_token'

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_confirm_email_token()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def generate_confirm_email_token(self):
        num_bytes = CONFIRM_EMAIL_TOKEN_LENGTH // 2
        return binascii.hexlify(os.urandom(num_bytes)).decode()

    def __str__(self):
        return 'ConfirmEmailToken (user {}): {}'.format(self.user, self.token)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_stars = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rating'


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now=True)
    num_date = models.IntegerField(default=1)

    class Meta:
        db_table = 'login_history'
