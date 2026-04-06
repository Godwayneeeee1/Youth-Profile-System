from django.contrib import admin
from .models import Youth, Barangay

@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Youth)
class YouthAdmin(admin.ModelAdmin):
    # We must use fields that actually exist in the new model
    list_display = ('name', 'sex', 'age', 'barangay', 'education_level', 'work_status')
    list_filter = ('barangay', 'sex', 'education_level', 'is_osy', 'is_pwd', 'is_ip')
    search_fields = ('name',)