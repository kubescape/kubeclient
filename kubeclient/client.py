import logging
from pathlib import Path
from typing import Optional

from kubernetes import client, config

_logger = logging.getLogger(__name__)


class KubernetesApiClient:
    """
    A class to manage the Kubernetes API client.
    """

    _api_client: client.ApiClient
    _config_file_path: Optional[Path] = None

    def __init__(self, config_file_path: Optional[Path] = None):
        self._config_file_path = config_file_path
        self._load_config()
        self._api_client = client.ApiClient()

    def _load_config(self) -> None:
        if self._config_file_path is not None:
            _logger.info(
                f"Loading Kubernetes configuration from {self._config_file_path}"
            )
            config.load_kube_config(config_file=self._config_file_path)
            return None

        _logger.info("Loading Kubernetes configuration from default location")
        config.load_kube_config()

    @property
    def api_client(self) -> client.ApiClient:
        return self._api_client

    @property
    def get_config(self) -> config:
        return self._api_client.configuration

    def close(self) -> None:
        self._api_client.close()
