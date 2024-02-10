from django.contrib import admin
from .models import UserAccount, UserProfile, Country, VisaRequirements, VisaType, TravelPlan, VisaTypeDocument

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'visa_requirements']


admin.site.register(UserAccount)
admin.site.register(UserProfile)
admin.site.register(Country, CountryAdmin)
admin.site.register(VisaRequirements)
admin.site.register(VisaType)
admin.site.register(VisaTypeDocument)