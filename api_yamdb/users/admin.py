from django.contrib import admin
from users.models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role'
    )
    list_editable = ('role',)
    list_filter = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UsersAdmin)
