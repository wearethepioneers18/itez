from rolepermissions.roles import AbstractUserRole


class SystemAdmin(AbstractUserRole):
    """
    Added custom user roles for system admin as follows.

    System Admin can drop tables.
    
    System Admin can manage project manager accounts.
    
    System Admin can manage field data collected.
    
    System Admin can manage reports generated.
    """
    available_permissions = {
        'can_drop_tables': True,
        'can_manage_project_managers': True,
        'can_manage_field_data': True,
        'can_manage_reports': True
    }

class ProjectManagement(AbstractUserRole):
    """
    Added custom user roles for Project Manager as follows.
    
    Project Manager can view content.
    
    Project Manager can manage field personnel accounts.
    
    Project Manager can manage donor accounts.
    """
    available_permissions = {
        'can_view_content': True,
        'can_manage_field_personnel': True,
        'can_manage_donors': True
    }

class DatabaseAdministrator(AbstractUserRole):
    """
    Added custom user roles for Database Administrator as follows.
    
    Database Administrator can view content.
    
    Database Administrator can manage field reports.
    
    Database Administrator can manage reports.
    
    Database Administrator can manage api data.
    """
    available_permissions = {
        'can_view_content': True,
        'can_manage_field_reports': True,
        'can_manage_reports': True,
        'can_manage_api_data': True
    }

class DonorRepresentative(AbstractUserRole):
    """
    Added custom user roles for Donor Representative as follows.
    
    Donor Representative can view content.

    Donor Representative can manage reports.
    """
    available_permissions = {
        'can_view_content': True,
        'can_manage_reports': True
    }

class FieldPersonnel(AbstractUserRole):
    """
    Added custom user roles for Field Personnel.

    Field Personnel can view permissions.

    Field Personnel can collect data.

    Field Personnel can create field reports. 
    """
    available_permissions = {
        'can_view_permissions': True,
        'can_collect_data': True,
        'can_create_field_reports': True
    }