"""Base Validation Rule."""


class ValidationRule:
    """Base Validation Rule."""

    def __init__(self, validation_code, validation_text):
        """Construct Base Validation Rule."""
        self.validation_code = validation_code
        self.validation_text = validation_text
        self.validation_passed = False
        self.error_list = []

    def set_status(self, validation_passed):
        """Set pass/fail validation status."""
        self.validation_passed = validation_passed

    def set_error_list(self, error_list):
        """Set the error list."""
        self.error_list = error_list
        if len(error_list) == 0:
            self.set_status(True)
        else:
            self.set_status(False)
