class IpstackAPIValueError(Exception):
    """
    Raised when Ipstack API returns 'None' for mandatory field.
    """
    def __init__(self, message: str = ""):
        super().__init__(message)
