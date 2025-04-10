import logging
import sys
import time
from typing import Any
from typing import Dict
from typing import List

import structlog
from app.core.config import settings

processors: List[structlog.types.Processor] = [
    structlog.stdlib.filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]

if settings.ENVIRONMENT != "development":
    processors.append(structlog.processors.JSONRenderer())
else:
    processors.append(structlog.dev.ConsoleRenderer())

structlog.configure(
    processors=processors,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=getattr(logging, settings.LOG_LEVEL),
)


def get_logger(name: str):
    return structlog.get_logger(name)
