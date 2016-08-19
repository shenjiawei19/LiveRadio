# -*- coding: utf-8 -*-
from django.db import models


# 监控系统
class System(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='系统编号')
    # linux,windows,
    name = models.CharField(max_length=30, verbose_name='系统名')

    Linux = 'Linux'
    Windows = 'Windows'
    SYSTEM_CHOICES = (
        (Linux, 'Linux'),
        (Windows, 'Windows'),
    )
    year_in_school = models.CharField(
        max_length=2,
        choices=SYSTEM_CHOICES,
        default=Linux,
    )
    class Meta:
        verbose_name_plural = '系统名'

    def __unicode__(self):
        return self.name


# 监控组
class Monitor_group(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='系统编号')
    #
    name = models.CharField(max_length=30, verbose_name='监控组类')

    class Meta:
        verbose_name_plural = '监控组类'

    def __unicode__(self):
        return self.name


# 监控业务组
class Monitor_group(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='系统编号')
    #
    name = models.CharField(max_length=30, verbose_name='监控组类')

    class Meta:
        verbose_name_plural = '监控组类'

    def __unicode__(self):
        return self.name


# 监控人员
class AbstractBaseUser(models.Model):
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    is_active = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __init__(self, *args, **kwargs):
        super(AbstractBaseUser, self).__init__(*args, **kwargs)
        # Stores the raw password if set_password() is called so that it can
        # be passed to password_changed() after the model is saved.
        self._password = None

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        super(AbstractBaseUser, self).save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_full_name(self):
        raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_full_name() method')

    def get_short_name(self):
        raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_short_name() method.')

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()
