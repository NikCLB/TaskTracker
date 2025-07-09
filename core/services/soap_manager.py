from zeep import Client, Transport, Settings


class SoapClient:
    def __init__(self):
        self._wsdl_root: str = "https://mantisbt.condor-fx.com"
        self._client: None | Client = None

    def makeSignUpRequest(self, username: str, password: str) -> str:
        wsdl_url  = self._wsdl_root + "/api/soap/mantisconnect.wsdl"
        real_endpoint = f"{self._wsdl_root}/api/soap/mantisconnect.php"
        settings = Settings(strict=False)
        self._client = Client(wsdl=wsdl_url, settings=settings)
        self._client.service._binding_options['address'] = real_endpoint    
        try:
            response = self._client.service.mc_login(username=username, password=password)
            return response
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            return None

soapClient = SoapClient()
