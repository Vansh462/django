from django.contrib import admin
from .models import Address, Patient, Doctor

# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('line1', 'city', 'state', 'pincode')
    search_fields = ('city', 'state')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_username', 'get_email', 'user_type', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email')
    readonly_fields = ('user_type', 'created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_username', 'user_type', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    readonly_fields = ('user_type', 'created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
