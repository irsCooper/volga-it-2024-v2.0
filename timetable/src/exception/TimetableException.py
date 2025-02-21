from fastapi import HTTPException, status

class TimetableNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetabe not found"
        )