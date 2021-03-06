from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        """Normalize the email address by lowercasing the domain part of the it.  """
        user = self.model(email=email, name=name)

        user.set_password(password)
        """password is encrypted we want to make sure the password is converted to a hash"""
        user.save(using=self._db)
        """this is the standard Django basically the standard"""
        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    """determines if the user is a staff user which is used to determine if they should have access to the Django admin and things like that"""

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user """
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """ Return string representation of our user"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE
        # we need to provide is the on delete argument so type on delete it tells Dja
        # ngo or it tells the database what to do if the remote field is deleted
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    # create a new feed item automatically add the date timestamp that the item was created

    def __str__(self):
        """Return the model as a string"""
        return  self.status_text

    # when we convert class ProfileFeedItem(models.Model): to a string
    # we want to see the status text value that is associated to the model


