from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active =models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email
    

class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    visa_requirements = models.ForeignKey('VisaRequirements', on_delete=models.CASCADE, related_name='country_visa_requirements')

    def __str__(self):
        return self.name
    
class VisaType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class VisaRequirements(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    no_visa_required = models.TextField(blank=True, null=True)
    visa_upon_arrival = models.TextField(blank=True, null=True)
    visa_fees_below_100 = models.TextField(blank=True, null=True)
    visa_fees_100_200 = models.TextField(blank=True, null=True)
    visa_fees_200_400 = models.TextField(blank=True, null=True)
    visa_fees_above_400 = models.TextField(blank=True, null=True)
    #store as son string of visa types
    visa_type = models.ForeignKey('VisaType', on_delete=models.CASCADE)
    health_requirements = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Visa requirements for {self.country.name}"


class Date(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)

class TravelPlan(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='user_attributes')
    destination = models.ForeignKey('Country', on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()

class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    # tourists, students, business travelers, expatriates
    profile_type = models.CharField(max_length=255)
    citizenship = models.ManyToManyField('Country', related_name='citizenship')
    country_of_residence = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='residence')
    travel_history = models.ManyToManyField('Country', related_name='travel_history', blank=True)
    travel_destination = models.ManyToManyField('Country', related_name='travel_destination')
    #holiday, education, business, or relocation choose in front-end store only one 
    purpose_of_travel =  models.CharField(max_length=100)
    travel_plans = models.ManyToManyField('TravelPlan', related_name='travel_plan', blank=True)
    preferred_languages = models.TextField(null=True)
    #email, sms, In-App choose in frontend store multiple as son string
    notification_preferences = models.TextField(null=True)
    #individual traveler or a representative from a travel agency, educational consultant, or corporate HR department
    client_type = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.email
    