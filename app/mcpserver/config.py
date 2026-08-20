"""集中配置管理"""
import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    server_name: str = field(
        default_factory=lambda: os.getenv("MCP_SERVER_NAME", "stock-report-mcp")
    )
    host: str = field(default_factory=lambda: os.getenv("MCP_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("MCP_PORT", "8000")))
    log_level: str = field(default_factory=lambda: os.getenv("MCP_LOG_LEVEL", "INFO"))
    request_timeout: int = field(
        default_factory=lambda: int(os.getenv("REQUEST_TIMEOUT", "12"))
    )


settings = Settings()