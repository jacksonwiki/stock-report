---
name: stock-report
description: A股研报MCP Server - 基于FastMCP与AkShare的股票研报MCP服务
version: 0.1.0
entry: python mcp_server.py --transport stdio
transport: stdio
tools:
  - get_stock_basic
  - get_stock_research_report
  - get_stock_news
  - get_financial_indicator
env:
  MCP_TRANSPORT: stdio
  MCP_HOST: "0.0.0.0"
  MCP_PORT: "8000"
  MCP_LOG_LEVEL: INFO
requires: "python>=3.11"
dependencies:
  - akshare
  - fastmcp
  - python-dotenv
---

# stock-report

基于 [FastMCP](https://github.com/fastmcp/fastmcp) 与 [AkShare](https://github.com/akfamily/akshare) 构建的 A 股研报 MCP Server，支持 `stdio`、`http`、`sse` 三种传输协议，可发布到 ModelScope 平台供任意支持 MCP 的客户端（Claude Desktop、Cursor、Trae 等）调用，实现对个股基础信息、券商研报、新闻及财务指标的一键查询。

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
- 兼容 ModelScope MCP 平台发布规范

## 📁 目录结构

```
stock-report/
├── mcp_server.py               # 根目录入口（ModelScope 平台要求）
├── app/
│   ├── __init__.py             # 包标识
│   └── mcpserver/
│       ├── __init__.py         # 包导出（mcp 实例）
│       ├── config.py           # 集中配置管理
│       └── server.py          # MCP 实例 + 工具注册
├── pyproject.toml              # 项目元数据与依赖声明
├── .env                        # 运行时环境变量
├── .gitignore
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

在项目根目录创建 `.env` 文件（本地开发用）：

```bash
MCP_TRANSPORT=stdio
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_LOG_LEVEL=INFO
REQUEST_TIMEOUT=12
```

### 4. 启动 MCP Server

```bash
# 默认 stdio 模式
python mcp_server.py

# HTTP 模式
python mcp_server.py --transport http --port 8000

# SSE 模式
python mcp_server.py --transport sse --port 8000
```

### 5. 本地客户端接入

#### stdio 模式（推荐）

在 MCP 客户端配置中：

```json
{
  "mcpServers": {
    "stock-report": {
      "command": "python",
      "args": ["mcp_server.py", "--transport", "stdio"]
    }
  }
}
```

#### HTTP 模式

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
| `--transport` | `stdio` / `http` / `sse` | `stdio` | 传输协议 |
| `--host` | IP 地址 | `0.0.0.0` | HTTP/SSE 监听地址 |
| `--port` | 端口号 | `8000` | HTTP/SSE 监听端口 |
| `--log-level` | `DEBUG` / `INFO` / `WARNING` / `ERROR` | `INFO` | 日志级别 |

## 🚀 发布到 ModelScope 平台

### 前置准备

1. 将代码推送到 GitHub 仓库
2. 确保 `mcp_server.py` 位于仓库根目录
3. `pyproject.toml` 中声明了所有依赖
4. README.md 顶部包含 YAML 元数据（本文件已配置）

### 发布步骤

1. 登录 [ModelScope MCP 平台](https://www.modelscope.cn/mcp)
2. 点击 **"创建 MCP"** → 选择 **"GitHub 快速创建"**
3. 填写基础信息：
   - 创建类型：`GitHub快速创建`
   - 托管类型：`可托管部署`
   - 英文名称：唯一标识
   - 中文名称：展示名称
   - 来源地址：你的 GitHub 仓库链接
4. 提交后，平台会自动：
   - 解析 README.md 中的 YAML 元数据
   - 克隆仓库代码
   - 执行 `pip install .` 安装依赖
   - 运行 `python mcp_server.py --transport stdio` 校验服务可用性
   - 校验通过后完成部署

### 校验失败排查清单

如果遇到 **"基础信息解析失败"** 或 **"校验服务配置可用性"** 失败，按以下顺序排查：

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | **README.md 顶部 YAML 元数据** | ModelScope 解析 README 开头的 YAML front matter 获取配置信息 |
| 2 | **根目录是否有 `mcp_server.py`** | ModelScope 默认查找根目录的 `mcp_server.py`，缺少会直接失败 |
| 3 | **默认传输协议是否为 `stdio`** | 平台用 stdio 验证，确保 `MCP_TRANSPORT` 环境变量为 `stdio` |
| 4 | **依赖能否快速安装** | AkShare 依赖较重，首次安装可能超时。本地先 `pip install -e .` 验证 |
| 5 | **Python 版本** | 平台可能使用 Python 3.11，确保代码兼容 |
| 6 | **本地测试通过** | 在本地先执行 `python mcp_server.py --transport stdio` 验证服务能正常启动 |

### 本地模拟 ModelScope 验证

在提交到平台前，先本地模拟验证：

```bash
# 1. 安装依赖
pip install -e .

# 2. 测试 stdio 模式启动
echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | python mcp_server.py --transport stdio

# 3. 测试列出工具
echo '{"jsonrpc":"2.0","method":"tools/list","id":2}' | python mcp_server.py --transport stdio
```

如果返回了有效的 JSON-RPC 响应，说明服务可以正常工作。

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

在 `app/mcpserver/config.py` 中集中管理配置项，支持通过环境变量覆盖默认值。

### 日志说明

为避免污染 MCP 协议的 stdout 通道，业务日志统一通过 `stderr` 输出。

### 关于传输协议

- **`stdio`**（生产/平台推荐）：由 MCP 客户端作为子进程拉起，通过 stdin/stdout 通信，ModelScope 平台使用此协议验证和部署。
- **`http`**（开发调试推荐）：以 Streamable-HTTP 方式对外暴露服务，端点 `/mcp`，便于跨客户端共享。
- **`sse`**：基于 Server-Sent Events 的传统推送模式。

## ⚠️ 免责声明

1. 本项目仅作为 MCP 协议学习与 A 股数据聚合的技术示例。
2. 数据来源于 AkShare 聚合的公开接口，**不保证实时性、准确性与完整性**。
3. 作者及相关贡献者不对任何投资决策承担责任，使用本项目所产生的一切后果由使用者自行承担。

## 📄 License

MIT