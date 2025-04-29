# errors.py


# Base Errors
class ExtractError(Exception):
    """Base class for extract-related errors."""
    def __init__(self, message="An error occurred during extraction."):
        super().__init__(message)

class TransformError(Exception):
    """Base class for transform-related errors."""
    def __init__(self, message="An error occurred during transformation."):
        super().__init__(message)

class LoadError(Exception):
    """Base class for load-related errors."""
    def __init__(self, message="An error occurred during loading."):
        super().__init__(message)


# Extract Errors
class SupermarketNotFound(ExtractError):
    def __init__(self, message="Supermarket not found."):
        super().__init__(message)

class CategoryURLsHTMLNotFound(ExtractError):
    def __init__(self, message="Category URLs HTML not found."):
        super().__init__(message)

class CategoryURLsNotFound(ExtractError):
    def __init__(self, message="Category URLs not found."):
        super().__init__(message)

class ProductURLsHTMLNotFound(ExtractError):
    def __init__(self, message="Product URLs HTML not found."):
        super().__init__(message)

class ProductURLsNotFound(ExtractError):
    def __init__(self, message="Product URLs not found."):
        super().__init__(message)

class ProductsHTMLNotFound(ExtractError):
    def __init__(self, message="Products HTML not found."):
        super().__init__(message)


# Transform Errors
class MalformedHTML(TransformError):
    def __init__(self, message="Malformed HTML encountered."):
        super().__init__(message)

class ContainerNotFound(TransformError):
    def __init__(self, message="Expected container not found in HTML."):
        super().__init__(message)

class DetailNotFound(TransformError):
    def __init__(self, message="Expected detail not found during parsing."):
        super().__init__(message)

class RedisStreamEmpty(TransformError):
    def __init__(self, message="Input redis stream is empty."):
        super().__init__(message)


# Load Errors
class PostgresError(LoadError):
    def __init__(self, message="Postgres operation failed."):
        super().__init__(message)

class RedisError(LoadError):
    def __init__(self, message="Redis operation failed."):
        super().__init__(message)
