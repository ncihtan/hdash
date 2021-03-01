class ValidationRule:
    def __init__(self, validation_code, validation_text):
        self.validation_code = validation_code
        self.validation_text = validation_text
        self.validation_passed = False

    def set_status(self, validation_passed):
        self.validation_passed = validation_passed
