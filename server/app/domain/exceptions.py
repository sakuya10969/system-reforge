class ProjectNotFoundError(Exception):
    pass


class InvalidZipFileError(Exception):
    pass


class EmptyZipFileError(Exception):
    pass


class AnalysisJobNotFoundError(Exception):
    pass


class InvalidStatusTransitionError(Exception):
    pass


class NoSourceFilesError(Exception):
    pass


class RequirementNotFoundError(Exception):
    pass
