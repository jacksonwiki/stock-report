"""CLI 入口 - 支持 stdio / http / sse 三种传输模式"""
import argparse

from .config import settings
from .logging_setup import logger
from .server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="stock-mcp",
        description="Stock Report MCP Server - A股研报MCP服务",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="http",
        help="传输协议: stdio(标准输入输出，子进程模式) / http(Streamable-HTTP) / sse(Server-Sent Events)",
    )
    parser.add_argument("--host", default=settings.host, help="HTTP/SSE 监听地址")
    parser.add_argument("--port", type=int, default=settings.port, help="HTTP/SSE 监听端口")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=settings.log_level,
        help="日志级别",
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        logger.info("Starting MCP server via stdio (子进程模式) ...")
        mcp.run(transport="stdio")
    elif args.transport == "http":
        logger.info(
            "Starting MCP server via Streamable-HTTP on %s:%s",
            args.host,
            args.port,
        )
        mcp.run(transport="http", host=args.host, port=args.port)
    elif args.transport == "sse":
        logger.info(
            "Starting MCP server via SSE on %s:%s",
            args.host,
            args.port,
        )
        mcp.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main()