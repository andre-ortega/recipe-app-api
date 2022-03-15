from django.db import models
# imports user database managers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email:
            raise ValueError('Users must have an email address')
        # Mgmt accesses the model that the manager is for with self.model
        # It is a way of creating a new user model and assigning it to 'user'
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # the self._db is good for saving in multiple databases, good practice
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create and saves a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Extending from AbstractBaseUser and PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
# remove inactive users
    is_active = models.BooleanField(default=True)
# used to create staff users
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
