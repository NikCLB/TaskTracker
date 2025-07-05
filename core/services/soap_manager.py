from zeep import Client


class SoapClient:
    def __init__(self):
        self._wsdl_root: str = "https://mantisbt.condor-fx.com"
        self._client: None | Client = None

    def makeSignUpRequest(self, username: str, password: str) -> str:
        wdslLink = self._wsdl_root + "/api/soap/mantisconnect.php"
        self._client = Client(wdslLink)
        try:
            response = self._client.service.mc_login(username=username, password=password)
            return response
        except Exception as e:
            print(f'Произошла ошибка: {e}')

soapClient = SoapClient()
