from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# For admin users
class MyAccountManager(BaseUserManager):
    
    # Create normal user
    def create_user(self, 
    				name, 
    				username, 
                    phone_number,
    				password=None):

        if not username:
            raise ValueError('User must have an username')
        
        if not phone_number:
            raise ValueError('User must have an phone number')

        user = self.model(
            username = username,
            phone_number = phone_number,
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create superuser
    def create_superuser(self, 
    					name, 
                        phone_number,
    					username, 
    					password):

        user = self.create_user(
            username = username,
            password = password,
            phone_number = phone_number,
            name = name,
        )

        # Give all privileges for superuser
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# For non-admin users
class Account(AbstractBaseUser):

	# These fields can be modified as needed
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone_number = models.IntegerField(unique=True)
    is_spam = models.BooleanField(default=False)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserToken (models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username
