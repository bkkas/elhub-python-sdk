"""
ElHub API client
"""
from zeep import Client, Settings

from datetime import datetime, timedelta
from zeep.wsse.signature import BinarySignature
from zeep.wsse import utils

from elhub_sdk.settings import KEY_FILE, CERT_FILE


class APIClient():
    """
    Main ElHub API client class
    """

    @staticmethod
    def get_zeep_client(wsdl)->Client:
        client_settings = Settings()
        client = Client(
            wsdl=wsdl,
            wsse=BinarySignatureTimestamp(
                key_file=KEY_FILE,
                certfile=CERT_FILE,
            ),
            settings=client_settings
        )
        return client


class BinarySignatureTimestamp(BinarySignature):
    """
    Add timestamp in signature
    """
    def apply(self, envelope, headers):
        security = utils.get_security_header(envelope)

        created = datetime.utcnow()
        expired = created + timedelta(seconds=1 * 60)

        timestamp = utils.WSU('Timestamp')
        timestamp.append(utils.WSU('Created', created.replace(microsecond=0).isoformat()+'Z'))
        timestamp.append(utils.WSU('Expires', expired.replace(microsecond=0).isoformat()+'Z'))

        security.append(timestamp)
        super().apply(envelope, headers)
        return envelope, headers

    def verify(self, envelope):
        return envelope



