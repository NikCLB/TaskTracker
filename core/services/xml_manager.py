import xml.etree.ElementTree as ET


class XMLManager:

    def parseXMLResponseForName(self, xmlResponse: str) -> str | None:
        root = ET.fromstring(xmlResponse)

        name_element = root.find('.//ns1:name', namespaces={'ns1': 'http://futureware.biz/mantisconnect'})

        if name_element is not None:
            name_value = name_element.text
            return name_value
        else:
            print('Element <name> not found.')

    def parseXMLResponseForID(self, xmlResponse: str) -> str | None:
        root = ET.fromstring(xmlResponse)

        name_element = root.find('.//ns1:id', namespaces={'ns1': 'http://futureware.biz/mantisconnect'})

        if name_element is not None:
            name_value = name_element.text
            return name_value
        else:
            print('Element <id> not found.')

xmlManager = XMLManager()
