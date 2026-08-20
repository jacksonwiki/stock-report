# stock-report

## 项目简介

基于 [FastMCP](https://github.com/fastmcp/fastmcp) 与 [AkShare](https://github.com/akfamily/akshare) 构建的 A 股研报 MCP Server，支持 `stdio`、`http`、`sse` 三种传输协议，可发布到 ModelScope 平台供任意支持 MCP 的客户端（Claude Desktop、Cursor、Trae 等）调用，实现对个股基础信息、券商研报、新闻及财务指标的一键查询。

> 本项目仅用于技术演示，所有数据来源于公开接口，不构成任何投资建议。

### 功能特性

| # | 工具名 | 说明 |
|---|--------|------|
| 1 | `get_stock_basic` | 查询个股基础信息（公司概况、上市信息等） |
| 2 | `get_stock_research_report` | 查询券商最新研报摘要（默认 5 条） |
| 3 | `get_stock_news` | 查询个股最新相关新闻（默认 8 条） |
| 4 | `get_financial_indicator` | 查询核心财务指标（营收、净利润、ROE 等） |

### 技术栈

- Python 3.11+
- [FastMCP](https://github.com/fastmcp/fastmcp) — MCP 协议工具服务器框架
- [AkShare](https://github.com/akfamily/akshare) — A 股开源金融数据接口库

## 部署指南

### 环境要求

- Python `>= 3.11`
- `pip` 包管理工具

### 安装依赖

```bash
pip install akshare fastmcp python-dotenv
```

或使用 `pyproject.toml`：

```bash
pip install -e .
```

### 启动 MCP Server

```bash
# stdio 模式（默认，ModelScope 平台验证用）
python mcp_server.py

# HTTP 模式
python mcp_server.py --transport http --port 8000

# SSE 模式
python mcp_server.py --transport sse --port 8000
```

### 客户端配置

#### stdio 模式

```json
{
  "mcpServers": {
    "stock-report": {
      "command": "python",
      "args": ["mcp_server.py"]
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

### 目录结构

```
stock-report/
├── mcp_server.py          # 单文件入口（自包含所有逻辑）
├── pyproject.toml         # 依赖声明
├── server_config.json     # MCP 服务配置
├── .env                   # 环境变量（可选）
├── .gitignore
└── README.md
```

## 使用示例

以股票 `600036`（招商银行）为例：

### 查询股票基础信息

```
get_stock_basic(symbol="600036")
```

返回示例：
```json
{
  "公司名称": "招商银行",
  "上市时间": "2002-04-09",
  "行业": "银行",
  "总股本": "252.20亿股"
}
```

### 查询券商最新研报

```
get_stock_research_report(symbol="600036", limit=3)
```

返回示例：
```json
[
  {
    "报告标题": "招商银行：净息差企稳，零售转型加速",
    "研究员": "张三",
    "发布日期": "2026-08-15",
    "评级": "买入"
  }
]
```

### 查询个股相关新闻

```
get_stock_news(symbol="600036", limit=5)
```

### 查询核心财务指标

```
get_financial_indicator(symbol="600036")
```

### 本地测试

```bash
# 测试 stdio 协议握手
echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | python mcp_server.py

# 测试列出工具
echo '{"jsonrpc":"2.0","method":"tools/list","id":2}' | python mcp_server.py
```

## 开发说明

### 新增工具

在 `mcp_server.py` 中使用 `@mcp.tool()` 装饰器：

```python
@mcp.tool()
def my_new_tool(symbol: str) -> str:
    """工具描述"""
    try:
        df = ak.some_akshare_function(symbol=symbol)
        return json.dumps(df.head().to_dict(orient="records"), ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
```

### 关于传输协议

- **`stdio`**：由 MCP 客户端作为子进程拉起，通过 stdin/stdout 通信
- **`http`**：以 Streamable-HTTP 方式对外暴露服务，端点 `/mcp`
- **`sse`**：基于 Server-Sent Events 的传统推送模式

## 免责声明

1. 本项目仅作为 MCP 协议学习与 A 股数据聚合的技术示例。
2. 数据来源于 AkShare 聚合的公开接口，不保证实时性、准确性与完整性。
3. 作者及相关贡献者不对任何投资决策承担责任。