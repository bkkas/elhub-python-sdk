"""
ElHub API client
"""
from datetime import datetime, timedelta
from typing import Tuple

from zeep import Client, Settings
from zeep.plugins import HistoryPlugin
from zeep.wsse import utils
from zeep.wsse.signature import BinarySignature


class APIClient:
    """
    Main ElHub API client class
    """

    @staticmethod
    def get_zeep_client(
        wsdl, secure: bool = True, key_file: str = "", cert_file: str = ""
    ) -> Tuple[Client, HistoryPlugin]:
        """
        Returns a client
        Args:
            wsdl:
            key_file:
            cert_file:
            secure:

        Returns:

        """
        history = HistoryPlugin()

        client_settings = Settings(strict=False)
        binary_signature = None
        if secure:
            binary_signature = BinarySignatureTimestamp(
                key_file=key_file,
                certfile=cert_file,
            )

        client = Client(wsdl=wsdl, plugins=[history], wsse=binary_signature, settings=client_settings)
        return client, history


class BinarySignatureTimestamp(BinarySignature):
    """
    Add timestamp in signature
    """

    def apply(self, envelope, headers):
        """
        Apply header
        Args:
            envelope:
            headers:

        Returns:

        """
        security = utils.get_security_header(envelope)

        created = datetime.utcnow()
        expired = created + timedelta(seconds=1 * 60)

        timestamp = utils.WSU('Timestamp')
        timestamp.append(utils.WSU('Created', created.replace(microsecond=0).isoformat() + 'Z'))
        timestamp.append(utils.WSU('Expires', expired.replace(microsecond=0).isoformat() + 'Z'))

        security.append(timestamp)
        super().apply(envelope, headers)
        return envelope, headers

    def verify(self, envelope):
        """
        Args:
            envelope:

        Returns:

        """
        return envelope
