# app/utils/roles.py
from fastapi import HTTPException


def require_role(*allowed_roles):

    def checker(user):

        if user.role_id not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return True

    return checker


def require_admin(user):

    if user.role_id not in [3, 4]:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return True


def require_superadmin(user):

    if user.role_id != 4:
        raise HTTPException(
            status_code=403,
            detail="SuperAdmin access required"
        )

    return True