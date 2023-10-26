from django.contrib import admin
from .models import Registration


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'phone_number', 'country', 'university', 'major', 'course', 'isPay')
    list_filter = ('isPay', 'country', 'university')
    search_fields = ('name', 'surname', 'email', 'university')
    ordering = ('name', 'surname', 'email', 'phone_number', 'country', 'university', 'major', 'course', 'isPay')


admin.site.register(Registration, RegistrationAdmin)
