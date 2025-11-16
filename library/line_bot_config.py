from pyfk import YmlUtils

class LineBotConfig(YmlUtils):

    active: str

    def __init__(self):
        super().__init__("app.yml")
        self.active = self.get_val("line.active")

    def get_token(self):
        return self.get_val(f"line.{self.active}.token")

    def get_secret(self):
        return self.get_val(f"line.{self.active}.secret")
