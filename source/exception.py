import sys


def error_message_detail(error, error_detail: sys):
    """
    Create a detailed error message including the script name, line number, and error message.

    Args:
        error: The error that occurred.
        error_detail (sys): The sys object containing error details.

    Returns:
        str: The detailed error message.
    """

    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


class BackOrderException(Exception):
    """
     Custom exception class for back order prediction pipeline.

    Args:
    error_message: The error message.
    error_detail: The sys object containing error details.
    """

    def __init__(self, error_message, error_detail):

        super().__init__(error_message)

        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message