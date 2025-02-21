from fastapi import HTTPException, status

class DatabaseException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Exception: Cannot insert data into table"
        )

class UnknowanDatabaseException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unknowan Exception: Cannot insert data into table"
        )


class ConflictUniqueAttribute(HTTPException):
    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Conflict Exc: {detail}"
        )