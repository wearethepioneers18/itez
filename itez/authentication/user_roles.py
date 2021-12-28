
from rolepermissions.roles import RolesManager

def user_roles():
    uncleaned_user_roles = RolesManager.get_roles_names()
    cleaned_user_roles = []
    
    for user_role in uncleaned_user_roles:
        splitted_user_role = user_role.split("_")
        cleaned_user_role = " ".join(splitted_user_role).title()
        cleaned_user_roles.append(
            {"key": f"{user_role}", "value": f"{cleaned_user_role}"}
        )
    return cleaned_user_roles
