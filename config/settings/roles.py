from django.contrib.auth.admin import UserAdmin
from rolepermissions.roles import (
    AbstractUserRole
)


class SystemAdmin(AbstractUserRole):
    available_permissions = {
        'drop_tables': True,
    }

class ProjectManagement(AbstractUserRole):
    available_permissions = {
        'can_view_content': True
    }

class DatabaseAdministrator(AbstractUserRole):
    available_permissions = {
        'can_view_content': True
    }

class DonorRepresentative(AbstractUserRole):
    available_permissions = {
        'can_view_content': True
    }

class FieldPersonnel(AbstractUserRole):
    available_permissions = {
        'can_view_permissions': True
    }