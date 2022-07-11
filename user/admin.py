from django.contrib import admin
# Register your models here.
from user.models import User, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserProfileInline(admin.StackedInline):
    model = UserProfile

    
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'nickname', 'email', 'birth')
    list_display_links = ('username', )
    list_filter = ('username', )
    search_fields = ('username', 'email', )

    fieldsets = (
        ("info", {'fields': ('username', 'password', 'email', 'nickname', 'birth', 'join_date',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', )}),)

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date', )
        else:
            return ('join_date', )
    inlines = (
        UserProfileInline,
    )

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)