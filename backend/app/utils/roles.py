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