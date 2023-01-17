import logging
import time
from functools import wraps
from typing import Any, Optional

logger = logging.getLogger(__name__)


def retry(
    tries: int = 5,
    delay: float = 2,
    retry_exceptions: tuple[Any] = (Exception,),
    logger: Optional[logging.Logger] = logger,
):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            for attempt in range(1, tries):
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as e:
                    logger.warning(f"Attempt: {attempt}, Python Error: {e}")
                    time.sleep(delay)

        return wrapped

    return wrapper
