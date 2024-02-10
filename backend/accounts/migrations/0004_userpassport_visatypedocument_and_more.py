# Generated by Django 4.2.7 on 2024-02-10 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_visa_fees_100_200_visarequirements_visa_application_eligibility_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPassport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_number', models.CharField(max_length=255)),
                ('passport_place_of_issue', models.CharField(max_length=255)),
                ('country_of_passport', models.CharField(max_length=255)),
                ('passport_date_of_issue', models.DateField()),
                ('passport_expiration_date', models.DateField()),
                ('passport_information_page', models.FileField(upload_to='visa_application_documents/')),
                ('passport_front_cover_page', models.FileField(upload_to='visa_application_documents/')),
            ],
        ),
        migrations.CreateModel(
            name='VisaTypeDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='notification_preferences',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='preferred_languages',
        ),
        migrations.AddField(
            model_name='travelplan',
            name='duration_of_stay_in_days',
            field=models.IntegerField(default=7),
        ),
        migrations.CreateModel(
            name='UserVisaApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('place_of_birth', models.CharField(max_length=255)),
                ('national_identity_number', models.CharField(blank=True, max_length=255, null=True)),
                ('copy_of_national_identity_card', models.FileField(blank=True, null=True, upload_to='visa_application_documents/')),
                ('current_citizenship_passport', models.FileField(upload_to='visa_application_documents/')),
                ('previous_nationality', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone_number', models.CharField(max_length=20)),
                ('full_home_address', models.TextField()),
                ('current_city', models.CharField(max_length=255)),
                ('profession', models.CharField(max_length=255)),
                ('date_of_entry', models.DateField()),
                ('date_of_depature', models.DateField()),
                ('duration_of_stay_in_days', models.IntegerField()),
                ('returning_to_country_of_residence', models.BooleanField(default=True)),
                ('previously_denied_entry_to_destination', models.BooleanField(default=False)),
                ('mothers_full_name', models.CharField(max_length=255)),
                ('fathers_full_name', models.CharField(max_length=255)),
                ('type_of_reference_in_destination', models.CharField(max_length=255)),
                ('user_photograph', models.FileField(upload_to='visa_application_documents/')),
                ('invitation_letter', models.FileField(blank=True, null=True, upload_to='visa_application_documents/')),
                ('bank_statements', models.FileField(blank=True, null=True, upload_to='visa_application_documents/')),
                ('hotel_reservation', models.FileField(blank=True, null=True, upload_to='visa_application_documents/')),
                ('company_registration_certificate', models.FileField(blank=True, null=True, upload_to='visa_application_documents/')),
                ('inviter_staff_id', models.FileField(blank=True, null=True, upload_to='visa_application_documents/')),
                ('previously_issued_visa', models.FileField(blank=True, null=True, upload_to='visa_application_documents/')),
                ('onward_flight_ticket', models.FileField(blank=True, null=True, upload_to='visa_application_documents/')),
                ('application_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50)),
                ('passport', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.userpassport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
                ('visa_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.visatype')),
            ],
        ),
        migrations.AddField(
            model_name='userpassport',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
        ),
        migrations.AddField(
            model_name='visatype',
            name='documents',
            field=models.ManyToManyField(related_name='document', to='accounts.visatypedocument'),
        ),
    ]
