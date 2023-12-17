import logging
import time
from typing import Callable, Optional

_logger = logging.getLogger(__name__)


class Condition:
    """
    This class is used to represent a condition in a Kubernetes resource.
    """

    def __init__(
        self,
        name: str,
        fn: Callable,
        timeout: Optional[int] = 0,
        interval: Optional[float] = 0.5,
        *args,
        **kwargs,
    ) -> None:
        if not callable(fn):
            raise TypeError(f"Condition {name} must be callable")

        self._name = name
        self._fn = fn
        self._timeout = timeout
        self._interval = interval
        self._args = args
        self._kwargs = kwargs

        self._last_check_result = False

    def _check(self) -> bool:
        """
        Check the condition.
        timeout:Optional: The timeout in seconds.
        """
        self._last_check_result = self._fn(*self._args, **self._kwargs)
        return self._last_check_result

    def wait(self) -> bool:
        """
        Wait for the condition to be true.
        timeout:Optional: The timeout in seconds.
        interval:Optional: The interval in seconds between checks.
        """
        _logger.info(f"Waiting for condition {self._name} to be true")
        start_time = time.time()
        while True:
            if self._check():
                return True

            if time.time() - start_time > self._timeout:
                _logger.error(f"Timeout waiting for condition {self._name} to be true")
                return False

            time.sleep(self._interval)
