class InvalidDateRangeException(Exception):
    def __init__(self):
        self.message="The Deployment Start Date cannot be later than the Deployment End Date"
        super().__init__(self.message)

class InvalidGLDateRangeException(Exception):
    def __init__(self):
        self.message="The Go Live Date cannot be before the Deployment End Date"
        super().__init__(self.message)

class MissingFieldException(Exception):
    def __init__(self,field_names):
        self.field_name=field_names
        fields_str=", ".join(field_names)
        self.message=f"The following fields are missing or invalid: '{fields_str}'"
        super().__init__(self.message)

class NoLogsFoundException(Exception):
    def __init__(self):
        self.message = "No logs found in database."
        super().__init__(self.message)

class DatabaseConnectionException(Exception):
    def __init__(self):
        self.message = "Database Connection Error."
        super().__init__(self.message)

class FileReadException(Exception):
    def __init__(self):
        self.message = "Failed to read contents of conflict attachment file"
        super().__inti__(self.message)

