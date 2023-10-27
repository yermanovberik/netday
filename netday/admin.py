from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone_number', 'university', 'isPay')
    list_filter = ('isPay', 'country', 'university')
    search_fields = ('name', 'surname', 'email', 'university')
    ordering = ('name', 'surname', 'country', 'university', 'major', 'course', 'isPay')
