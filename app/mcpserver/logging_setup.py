"""日志配置 - 输出到 stderr，避免污染 MCP 协议的 stdout 通道"""
import logging
import sys

from .config import settings


def setup_logging() -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stderr,
    )
    logger = logging.getLogger("stock-mcp")
    logger.propagate = False
    return logger


logger = setup_logging()