from django.contrib import admin
from django.contrib.auth.models import Group
from general.models import (
    User,
    Department,
    AcademicYear,
    StudyYear,
    ClassGroup
)

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from rangefilter.filters import DateRangeFilter

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)  # Use 'email' as the username

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

admin.site.unregister(Group)

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "last_activity",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
        "last_activity",
    )
    list_display_links = (
        "first_name",
        "last_name",
        "email",
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
        (
            "Личные данные", {
                "fields": (
                    "last_name",
                    "first_name",
                    "middle_name",
                    "gender",
                    "photo",
                )
            }
        ),
        (
            "Связь с Дневник.РУ", {
                "fields": (
                    "dnevnik_token",
                    "dnevnik_id", 
                )
            }
        ),
    )
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            "Личные данные", {
                "fields": (
                    "last_name",
                    "first_name",
                    "middle_name",
                    "gender",
                    "photo",
                )
            }
        ),
        (
            "Связь с Дневник.РУ", {
                "fields": (
                    "dnevnik_token",
                    "dnevnik_id", 
                )
            }
        ),
        (
            "Статусы", {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            }
        ),
        (
            "Даты", {
                "fields": (
                    "date_joined",
                    "last_login",
                    "last_activity",
                )
            }
        )
    )
    search_fields = (
        "last_name",
        "email",
    )
    list_filter = (
        "is_active",
        "groups",
        ("date_joined", DateRangeFilter),
    )
    # Удалите ordering, если не используете сортировку
    ordering = ('email',)
    exclude = ('username',)

# @admin.register(User)
# class UserModelAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "first_name",
#         "last_name",
#         "email",
#         "is_active",
#         "last_activity",
#     )
#     readonly_fields = (
#         "date_joined",
#         "last_login",
#         "last_activity",
#     )
#     list_display_links = (
#         "first_name",
#         "last_name",
#         "email",
#     )
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (
#             "Личные данные", {
#                 "fields": (
#                     "last_name",
#                     "first_name",
#                     "middle_name",
#                     "gender",
#                     "photo",
#                 )
#             }
#         ),
#         (
#             "Связь с Дневник.РУ", {
#                 "fields": (
#                     "dnevnik_token",
#                     "dnevnik_id", 
#                 )
#             }
#         ),
#         (
#             "Статусы", {
#                 "classes": (
#                     "collapse",
#                 ),
#                 "fields": (
#                     "is_staff",
#                     "is_superuser",
#                     "is_active",
#                 )
#             }
#         ),
#         (
#             "Даты", {
#                 "fields": (
#                     "date_joined",
#                     "last_login",
#                     "last_activity",
#                 )
#             }
#         )
#     )
#     search_fields = (
#         "last_name",
#         "email",
#     )
#     list_filter = (
#         "is_active",
#         "groups",
#         ("date_joined", DateRangeFilter),
#     )

admin.site.register(User, CustomUserAdmin)

@admin.register(Group)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = (
        "name",
    )
    fields = (
        "name",
        "permissions",
    )

@admin.register(Department)
class DepartmentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = (
        "name",
    )
    fields = (
        "name",
        "logo",
        "employees",
    )

@admin.register(AcademicYear)
class AcademicYearModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "date_start",
        "date_end",
    )
    list_display_links = (
        "name",
    )
    fields = (
        "name",
        "date_start",
        "date_end",
    )

@admin.register(StudyYear)
class StudyYearModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number",
        "number_ib",
        "level",
        "program_ib",
    )
    list_display_links = (
        "number",
    )
    fields = (
        "number",
        "number_ib",
        "level",
        "program_ib",
    )

@admin.register(ClassGroup)
class ClassGroupModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "mentor",
        "year_academic",
    )
    list_display_links = (
        "name",
    )
    fields = (
        "year_academic",
        "year_study",
        "letter",
        "dnevnik_id",
        "mentor",
        "psychologist",
        "program_ib"
    )