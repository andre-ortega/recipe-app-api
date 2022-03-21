from django.db import models
# imports user database managers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
# Best way to retrive settings from our settings file, used to get our auth
#  user model
from django.conf import settings


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


class Tag(models.Model):
    """ Tag to be used for a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Ingredient to be used in a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Recipe object """
    # Add a foreign key to the auth user model, if we remove that user then
    #  the recipes will be removed as well (cascade)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # Best way to make an optional field (blank=True)
    link = models.CharField(max_length=255, blank=True)

    # Allow many recipes to be assigned to many ingredients
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
