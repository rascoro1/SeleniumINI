
class NotValidAttributeException(Exception):
    def __init__(self, message, errors):
            super(NotValidAttributeException, self).__init__(message)
            self.errors = errors


class NoReportFoundException(Exception):
    def __init__(self, message, errors):
            super(NoReportFoundException, self).__init__(message)
            self.errors = errors


class ElementCannotBeFoundException(Exception):
    def __init__(self, message, errors):
            super(ElementCannotBeFoundException, self).__init__(message)
            self.errors = errors


class TemplatePathNotFoundException(Exception):
    def __init__(self, message, errors):
            super(TemplatePathNotFoundException, self).__init__(message)
            self.errors = errors


class NoINITemplateGivenException(Exception):
    def __init__(self, message, errors):
            super(NoINITemplateGivenException, self).__init__(message)
            self.errors = errors


class TemplateINIFileDoesNotExistException(Exception):
    def __init__(self, message, errors):
            super(TemplateINIFileDoesNotExistException, self).__init__(message)
            self.errors = errors


class TemplateFileIsNotAnINIFileException(Exception):
    def __init__(self, message, errors):
            super(TemplateFileIsNotAnINIFileException, self).__init__(message)
            self.errors = errors


class OutputFileAlreadyExistsException(Exception):
    def __init__(self, message, errors):
            super(OutputFileAlreadyExistsException, self).__init__(message)
            self.errors = errors


class InvalidOutputFilePathException(Exception):
    def __init__(self, message, errors):
        super(InvalidOutputFilePathException, self).__init__(message)
        self.errors = errors


class BatchFileDoesNotExistException(Exception):
    def __init__(self, message, errors):
        super(BatchFileDoesNotExistException, self).__init__(message)
        self.errors = errors


class NoBatchFileWithConcurrentEnabled(Exception):
    def __init__(self, message, errors):
        super(NoBatchFileWithConcurrentEnabled, self).__init__(message)
        self.errors = errors


class InvalidDynamicInputStringException(Exception):
    def __init__(self, message, errors):
        super(InvalidDynamicInputStringException, self).__init__(message)
        self.errors = errors


class DynamicVariableNotFoundInTemplateException(Exception):
    def __init__(self, message, errors):
        super(DynamicVariableNotFoundInTemplateException, self).__init__(message)
        self.errors = errors

class DynamicTemplateAlreadyExistsException(Exception):
    def __init__(self, message, errors):
        super(DynamicTemplateAlreadyExistsException, self).__init__(message)
        self.errors = errors

