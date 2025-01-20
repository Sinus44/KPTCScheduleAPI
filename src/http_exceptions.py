from fastapi import HTTPException


class FileNotFoundException(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, 404, "File not found")


class FileWithDateNotFoundException(HTTPException):
    def __init__(self, date):
        HTTPException.__init__(self, 404, f"File with date {date} not found")


class InvalidParameterException(HTTPException):
    def __init__(self, parameter_name):
        HTTPException.__init__(self, 422, f"Invalid {parameter_name}")


class InternalFileNotFoundException(HTTPException):
    def __init__(self, file_id):
        HTTPException.__init__(self, 500, f"Internal exception: file not found {file_id}")


class ScheduleNotFoundException(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, 404, "Schedule not found")


class NotImplementedException(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, 501, "Not implemented")
