class Error(BaseException):
    def __init__(self, text=""):
        super().__init__(text)

class Pass(BaseException):
    def __init__(self, text=""):
        super().__init__(text)
