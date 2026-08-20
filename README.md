# stock-report

基于 [FastMCP](https://github.com/fastmcp/fastmcp) 与 [AkShare](https://github.com/akfamily/akshare) 构建的 A 股研报 MCP Server，支持 `stdio`、`http`、`sse` 三种传输协议，供任意支持 MCP 的客户端（如 Claude Desktop、Cursor、Trae 等）调用，实现对个股基础信息、券商研报、新闻及财务指标的一键查询。

> ⚠️ 本项目仅用于技术演示，所有数据来源于公开接口，**不构成任何投资建议**。

## ✨ 功能特性

| # | 工具名 | 说明 |
|---|--------|------|
| 1 | `get_stock_basic` | 查询个股基础信息（公司概况、上市信息等） |
| 2 | `get_stock_research_report` | 查询券商最新研报摘要（默认 5 条） |
| 3 | `get_stock_news` | 查询个股最新相关新闻（默认 8 条） |
| 4 | `get_financial_indicator` | 查询核心财务指标（营收、净利润、ROE 等） |

## 🏗️ 技术栈

- Python 3.11+
- [FastMCP](https://github.com/fastmcp/fastmcp) — 基于 MCP 协议的工具服务器框架
- [AkShare](https://github.com/akfamily/akshare) — A 股开源金融数据接口库
- 支持 `stdio` / `http` / `sse` 三种传输协议

## 📁 目录结构

```
stock-report/
├── app/
│   └── mcpserver/
│       ├── __init__.py        # 包导出（mcp 实例）
│       ├── __main__.py        # python -m 入口
│       ├── cli.py             # CLI 命令行入口（argparse）
│       ├── config.py          # 集中配置管理（环境变量）
│       ├── logging_setup.py   # 日志配置（stderr 输出）
│       └── server.py          # MCP 实例 + 工具注册
├── pyproject.toml             # 项目元数据与依赖声明
├── .env                       # 运行时环境变量
└── README.md
```

## 🚀 快速开始

### 1. 环境要求

- Python `>= 3.11`
- 已安装 `pip` 或 `uv` / `poetry` 等包管理工具

### 2. 安装依赖

```bash
pip install -e .
```

或直接安装依赖：

```bash
pip install akshare fastmcp python-dotenv
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
# 服务端
MCP_SERVER_NAME=stock-report-mcp
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_LOG_LEVEL=INFO

# AkShare
REQUEST_TIMEOUT=12
```

### 4. 启动 MCP Server

#### 方式一：命令行入口（推荐）

```bash
# 默认 Streamable-HTTP
stock-mcp

# 指定传输协议与端口
stock-mcp --transport http --port 8080

# 子进程模式（推荐用于 MCP 客户端集成）
stock-mcp --transport stdio

# SSE 模式
stock-mcp --transport sse
```

#### 方式二：python -m

```bash
python -m app.mcpserver --transport stdio
```

#### 方式三：直接调用模块

```bash
python -m app.mcpserver.cli --transport http --host 0.0.0.0 --port 8000
```

### 5. 客户端接入

#### stdio 模式（推荐，生产环境首选）

在 MCP 客户端配置中：

```json
{
  "mcpServers": {
    "stock-report": {
      "command": "stock-mcp",
      "args": ["--transport", "stdio"]
    }
  }
}
```

#### HTTP 模式（便于跨客户端共享）

```json
{
  "mcpServers": {
    "stock-report": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### CLI 参数

| 参数 | 可选值 | 默认值 | 说明 |
|------|--------|--------|------|
| `--transport` | `stdio` / `http` / `sse` | `http` | 传输协议 |
| `--host` | IP 地址 | `0.0.0.0` | HTTP/SSE 监听地址 |
| `--port` | 端口号 | `8000` | HTTP/SSE 监听端口 |
| `--log-level` | `DEBUG` / `INFO` / `WARNING` / `ERROR` | `INFO` | 日志级别 |

## 🔧 工具调用示例

以股票 `600036`（招商银行）为例：

**1. 查询股票基础信息**
```
get_stock_basic(symbol="600036")
```

**2. 查询最新 5 条券商研报**
```
get_stock_research_report(symbol="600036", limit=5)
```

**3. 查询最新 8 条相关新闻**
```
get_stock_news(symbol="600036", limit=8)
```

**4. 查询最新核心财务指标**
```
get_financial_indicator(symbol="600036")
```

所有工具返回结果均为 JSON 字符串（`ensure_ascii=False`、`indent=2`），便于客户端直接解析和展示。

## 📝 开发说明

### 新增一个工具

在 `app/mcpserver/server.py` 中使用 `@mcp.tool()` 装饰器注册：

```python
# server.py
@mcp.tool()
def my_new_tool(symbol: str) -> str:
    """工具描述（客户端会作为 schema 展示）"""
    try:
        df = ak.some_akshare_function(symbol=symbol)
        return json.dumps(df.head().to_dict(orient="records"), ensure_ascii=False, indent=2)
    except Exception as e:
        logger.exception("my_new_tool error")
        return json.dumps({"error": str(e)}, ensure_ascii=False)
```

### 配置说明

在 `app/mcpserver/config.py` 中集中管理配置项，支持通过环境变量覆盖默认值：

```python
@dataclass
class Settings:
    server_name: str = field(default_factory=lambda: os.getenv("MCP_SERVER_NAME", "stock-report-mcp"))
    # ...
```

### 日志说明

为避免污染 MCP 协议的 stdout 通道，业务日志统一通过 `stderr` 输出，使用标准 `logging` 模块，默认 `INFO` 级别。日志配置位于 `app/mcpserver/logging_setup.py`。

### 关于传输协议

- **`stdio`**（生产环境推荐）：由 MCP 客户端作为子进程拉起，通过 stdin/stdout 通信，隔离性最好。
- **`http`**（开发调试推荐）：以 Streamable-HTTP 方式对外暴露服务，端点 `/mcp`，便于跨客户端共享。
- **`sse`**：基于 Server-Sent Events 的传统推送模式，适用于特定场景。

## ⚠️ 免责声明

1. 本项目仅作为 MCP 协议学习与 A 股数据聚合的技术示例。
2. 数据来源于 AkShare 聚合的公开接口，**不保证实时性、准确性与完整性**。
3. 作者及相关贡献者不对任何投资决策承担责任，使用本项目所产生的一切后果由使用者自行承担。

## 📄 License

MIT