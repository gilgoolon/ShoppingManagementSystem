

class ReceiptProcessorError(Exception):
    """
    General error with the receipt processor
    """


class NotAReceiptError(ReceiptProcessorError):
    """
    The given image wasn't a valid receipt
    """


class BadQualityError(ReceiptProcessorError):
    """
    The given image's quality was too bad to process
    """
