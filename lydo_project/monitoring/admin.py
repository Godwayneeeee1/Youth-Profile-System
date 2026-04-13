"""Admin registrations for managing LYDO data through Django admin."""
from django.contrib import admin
from .models import Youth, Barangay, UserBarangayAssignment, UserAccessLog

@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    """Basic barangay list display."""
    list_display = ('name',)

@admin.register(Youth)
class YouthAdmin(admin.ModelAdmin):
    # We must use fields that actually exist in the new model
    # Admin list view for quick filtering and search.
    list_display = ('name', 'sex', 'age', 'barangay', 'education_level', 'work_status')
    list_filter = ('barangay', 'sex', 'education_level', 'is_osy', 'is_pwd', 'is_ip')
    search_fields = ('name',)


@admin.register(UserBarangayAssignment)
class UserBarangayAssignmentAdmin(admin.ModelAdmin):
    """Manage which user owns which barangay."""
    list_display = ('user', 'barangay')
    list_filter = ('barangay',)
    search_fields = ('user__username', 'barangay__name')


@admin.register(UserAccessLog)
class UserAccessLogAdmin(admin.ModelAdmin):
    """Audit view of login/logout events."""
    list_display = ('user', 'barangay', 'login_time', 'logout_time')
    list_filter = ('barangay', 'login_time', 'logout_time')
    search_fields = ('user__username', 'barangay__name')
