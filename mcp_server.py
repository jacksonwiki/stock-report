"""
Root-level entry point for ModelScope MCP Platform.
ModelScope expects a standard mcp_server.py at project root that exposes
a `mcp` (FastMCP) instance and supports direct execution.

Usage on ModelScope Platform:
    python mcp_server.py              # stdio mode (default, for MCP platform validation)
    python mcp_server.py --transport http --port 8000
    python mcp_server.py --transport sse --port 8000
"""
import os
import sys
import argparse
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from app.mcpserver.config import settings
    from app.mcpserver.server import mcp, logger  # noqa: F401
except ImportError as e:
    print(f"ERROR: Failed to import MCP server modules: {e}", file=sys.stderr)
    print("Make sure dependencies are installed: pip install -e .", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="stock-mcp",
        description="Stock Report MCP Server - A股研报MCP服务",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default=os.getenv("MCP_TRANSPORT", "stdio"),
        help="传输协议 (默认: stdio)",
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

    try:
        if args.transport == "stdio":
            logger.info("Starting MCP server via stdio ...")
            mcp.run(transport="stdio")
        elif args.transport == "http":
            logger.info("Starting MCP server via HTTP on %s:%s", args.host, args.port)
            mcp.run(transport="http", host=args.host, port=args.port)
        elif args.transport == "sse":
            logger.info("Starting MCP server via SSE on %s:%s", args.host, args.port)
            mcp.run(transport="sse", host=args.host, port=args.port)
    except Exception as e:
        logger.error("MCP server failed: %s", e)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()