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
    
class VisaTypeDocument(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class VisaType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    visa_group = models.CharField(max_length=255, blank=True)
    processing_time = models.CharField(max_length=255, default='2-3 Business Days')
    visa_fees = models.TextField(blank=True, null=True)
    documents = models.ManyToManyField('VisaTypeDocument', related_name='document')

    def __str__(self):
        return self.name

class VisaRequirements(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    no_visa_required = models.TextField(blank=True, null=True)
    visa_upon_arrival = models.TextField(blank=True, null=True)
    #store as son string of visa types
    visa_type = models.ForeignKey('VisaType', on_delete=models.CASCADE)
    health_requirements = models.TextField(blank=True, null=True)
    visa_application_eligibility = models.TextField(blank=True, null=True)

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
    duration_of_stay_in_days = models.IntegerField(default=7)

class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    # tourists, students, business travelers, expatriates
    profile_type = models.CharField(max_length=255)
    citizenship = models.ManyToManyField('Country', related_name='citizenship')
    country_of_residence = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='residence')
    #how long they've had their passport for
    passport_validity_requirement = models.CharField(max_length=255, null=True)
    travel_history = models.ManyToManyField('Country', related_name='travel_history', blank=True)
    initial_travel_destination = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='initial_travel_destination', null=True)
    subsequent_travel_destinations = models.ManyToManyField('Country', related_name='subsequent_travel_destinations', blank=True)
    #holiday, education, business, or relocation choose in front-end store only one 
    purpose_of_travel =  models.CharField(max_length=100)
    travel_plans = models.ManyToManyField('TravelPlan', related_name='travel_plan', blank=True)
    #individual traveler or a representative from a travel agency, educational consultant, or corporate HR department
    client_type = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.email
    
#Admin should be able to download visa application form
class UserVisaApplication(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    place_of_birth = models.CharField(max_length=255)
    national_identity_number = models.CharField(max_length=255, blank=True, null=True)
    copy_of_national_identity_card = models.FileField(upload_to='visa_application_documents/', blank=True, null=True)
    passport = models.OneToOneField('UserPassport', on_delete=models.CASCADE)
    current_citizenship_passport = models.FileField(upload_to='visa_application_documents/')
    previous_nationality = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone_number = models.CharField(max_length=20)
    full_home_address = models.TextField()
    current_city = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    date_of_entry = models.DateField()
    date_of_depature = models.DateField()
    duration_of_stay_in_days = models.IntegerField()
    returning_to_country_of_residence = models.BooleanField(default=True)
    previously_denied_entry_to_destination = models.BooleanField(default=False)
    mothers_full_name = models.CharField(max_length=255)
    fathers_full_name = models.CharField(max_length=255)
    type_of_reference_in_destination = models.CharField(max_length=255)
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE)
    user_photograph = models.FileField(upload_to='visa_application_documents/')
    invitation_letter = models.FileField(upload_to='visa_application_documents/', blank=True, null=True)
    bank_statements = models.FileField(upload_to='visa_application_documents/', blank=True, null=True)
    hotel_reservation = models.FileField(upload_to='visa_application_documents/', blank=True, null=True)
    company_registration_certificate = models.FileField(upload_to='visa_application_documents/', blank=True, null=True)
    inviter_staff_id = models.FileField(upload_to='visa_application_documents/', blank=True, null=True)
    previously_issued_visa = models.FileField(upload_to='visa_application_documents/', blank=True, null=True)
    onward_flight_ticket = models.FileField(upload_to='visa_application_documents/', blank=True, null=True)
    consultation_booked = models.BooleanField(default=False)
    consultation_date = models.DateField(null=True, blank=True)
    consultation_time = models.TimeField(null=True, blank=True)
    consultation_location = models.CharField(max_length=255, null=True, blank=True)
    application_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')

    def __str__(self):
        return f"Visa Application for {self.user}"


class UserPassport(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=255)
    passport_place_of_issue = models.CharField(max_length=255)
    country_of_passport = models.CharField(max_length=255)
    passport_date_of_issue = models.DateField()
    passport_expiration_date = models.DateField()
    passport_information_page = models.FileField(upload_to='visa_application_documents/')
    passport_front_cover_page = models.FileField(upload_to='visa_application_documents/')

    def __str__(self):
        return f"Passport: {self.passport_number} - User: {self.user}"