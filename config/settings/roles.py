from rolepermissions.roles import AbstractUserRole


class SystemAdmin(AbstractUserRole):
    available_permissions = {
        'drop_tables': True,
        'can_manage_project_managers': True,
        'can_manage_field_data': True,
        'can_manage_reports': True
    }

class ProjectManagement(AbstractUserRole):
    available_permissions = {
        'can_view_content': True,
        'can_manage_field_personnel': True,
        'can_manage_donors': True
    }

class DatabaseAdministrator(AbstractUserRole):
    available_permissions = {
        'can_view_content': True,
        'can_manage_field_reports': True,
        'can_manage_reports': True,
        'can_manage_api_data': True
    }

class DonorRepresentative(AbstractUserRole):
    available_permissions = {
        'can_view_content': True,
        'can_manage_reports': True
    }

class FieldPersonnel(AbstractUserRole):
    available_permissions = {
        'can_view_permissions': True,
        'can_collect_data': True,
        'can_create_field_reports': True
    }