from rolepermissions.roles import AbstractUserRole


class SystemAdmin(AbstractUserRole):
    """
    Defines custom role permissions for a System Admin.

    Parameters
    ----------

    AbstractUserRole: str
    A base factory object implementing role permission management

    Permissions
    -----------
    >> Can drop database tables.
    >> Can manage project manager accounts, roles, permissions.
    >> Can manage field data saved on the database.
    >> Can manage reports generated.
    """
    available_permissions = {
        'can_drop_tables': True,
        'can_manage_project_managers': True,
        'can_manage_field_data': True,
        'can_manage_reports': True
    }

class ProjectManagement(AbstractUserRole):
    """
    Defines custom role permissions for a Project Manager.

    Parameters
    ----------

    AbstractUserRole: str
    A base factory object implementing role permission management

    Permissions
    -----------
    >> Can manage field personnel accounts.
    >> Can manage donor accounts.
    """
    available_permissions = {
        'can_manage_field_personnel': True,
        'can_manage_donors': True
    }

class DatabaseAdministrator(AbstractUserRole):
    """
    Defines custom role permissions for a Database Administrator.

    Parameters
    ----------

    AbstractUserRole: str
    A base factory object implementing role permission management

    Permissions
    -----------
    >> Can manage field reports saved on the databse.
    >> Can manage all other reports generated.
    >> Can manage api data.
    """
    available_permissions = {
        'can_manage_field_reports': True,
        'can_manage_reports': True,
        'can_manage_api_data': True
    }

class DonorRepresentative(AbstractUserRole):
    """
    Defines custom role permissions for a Donor Representative.

    Parameters
    ----------

    AbstractUserRole: str
    A base factory object implementing role permission management

    Permissions
    -----------
    >> can manage reports generated.
    """
    available_permissions = {
        'can_manage_reports': True
    }

class FieldPersonnel(AbstractUserRole):
    """
    Defines custom role permissions for a Field Personnel.

    Parameters
    ----------

    AbstractUserRole: str
    A base factory object implementing role permission management

    Permissions
    -----------
    >> Can view permissions.
    >> Can collect and save data to the database.
    >> Can create field reports.
    """
    available_permissions = {
        'can_view_permissions': True,
        'can_collect_data': True,
        'can_create_field_reports': True
    }