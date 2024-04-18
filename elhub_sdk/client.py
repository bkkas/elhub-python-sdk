"""
ElHub API client
"""
import logging
import os
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Tuple
import xml.etree.ElementTree as ET

from zeep import Client, Settings
from zeep.plugins import HistoryPlugin
from zeep.wsse import utils
from zeep.wsse.signature import BinarySignature

logger = logging.getLogger()

class ElHubService(str, Enum):
    """
    ElHub services pointing to the correct WSDL file
    """

    MARKET_PROCESSES = "MarketProcesses - WS-Security.wsdl"
    METERING_VALUES = "MeteringValues - WS-Security.wsdl"
    POOL_MARKET_PROCESSES = "PollMarketProcesses - WS-Security.wsdl"
    POOL_METERING_VALUES = "PollMeteringValues - WS-Security.wsdl"
    QUERY = "Query - WS-Security.wsdl"


class ElHubEnvironment(str, Enum):
    """
    ElHub environment, either prod or test
    """

    PRODUCTION = "prod"
    TEST = "test"


class APIClient:
    """
    Main ElHub API client class
    """

    @staticmethod
    def get_client(
        environment: ElHubEnvironment, service: ElHubService, key_file: str = "", cert_file: str = ""
    ) -> Tuple[Client, HistoryPlugin]:
        """
        Get a production client and a history plugin
        Args:
            environment: the environment to use in Elhub
            service: the service to use in Elhub
            key_file: the key file to use
            cert_file: the certificate file to use
        Returns:

        """
        return APIClient._get_zeep_client(
            wsdl=os.path.join(os.path.dirname(__file__), "wsdl", environment, "2.3", "wsdl", service),
            secure=True,
            key_file=key_file,
            cert_file=cert_file,
        )

    @staticmethod
    def _get_zeep_client(
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
        if (key_file is None or key_file == "") or (cert_file is None or cert_file == ""):
            key_file = os.getenv('ELHUB_KEY_FILE')
            cert_file = os.getenv('ELHUB_CERT_FILE')
            logger.info(f"Key file: {key_file}")
            logger.info(f"Cert file: {cert_file}")
        client_settings = Settings(strict=False)
        binary_signature = None
        if secure:
            binary_signature = BinarySignatureTimestamp(
                key_file=key_file,
                certfile=cert_file,
            )

        client = Client(wsdl=wsdl, plugins=[history], wsse=binary_signature, settings=client_settings)
        return client, history

    @staticmethod
    def get_zeep_client(
        wsdl, secure: bool = True, key_file: str = "", cert_file: str = ""
    ) -> Tuple[Client, HistoryPlugin]:
        """
        Deprecated: Please use get_client instead
        Returns a client
        Args:
            wsdl:
            key_file:
            cert_file:
            secure:

        Returns:

        """
        return APIClient._get_zeep_client(wsdl, secure, key_file, cert_file)


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
        if security is not None:
            security_string = ET.tostring(security, encoding='unicode')
            logger.info(f"BinarySignatureTimestamp security: {security_string}")
        created = datetime.now(timezone.utc)
        expired = created + timedelta(seconds=1 * 60)

        timestamp = utils.WSU('Timestamp')
        timestamp.append(utils.WSU('Created', created.replace(microsecond=0).isoformat() + 'Z'))
        timestamp.append(utils.WSU('Expires', expired.replace(microsecond=0).isoformat() + 'Z'))

        security.append(timestamp)
        if security is not None:
            security_string = ET.tostring(security, encoding='unicode')
            logger.info(f"BinarySignatureTimestamp security with timestamp: {security_string}")
        envelope_string = ET.tostring(envelope, encoding='unicode')
        logger.info(f"BinarySignatureTimestamp envelope: {envelope_string}")
        logger.info(f"BinarySignatureTimestamp headers: {headers}")
        try:
            super().apply(envelope, headers)
        except Exception as e:
            logger.error(f"Zeep BinarySignature error: {e}")
        return envelope, headers

    def verify(self, envelope):
        """
        Args:
            envelope:

        Returns:

        """
        return envelope
