"""MCP 实例创建与注册工具"""
import json

import akshare as ak
from fastmcp import FastMCP

from .config import settings
from .logging_setup import logger

mcp = FastMCP(settings.server_name)


@mcp.tool()
def get_stock_basic(symbol: str) -> str:
    """
    获取A股股票基础概况信息
    Args:
        symbol: A股股票代码，例如 "600036"
    """
    try:
        df = ak.stock_individual_info_em(symbol=symbol)
        info = dict(zip(df["item"], df["value"]))
        return json.dumps(info, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.exception("get_stock_basic error")
        return json.dumps({"error": f"获取股票基础信息失败: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def get_stock_research_report(symbol: str, limit: int = 5) -> str:
    """
    获取券商最新研报摘要
    Args:
        symbol: A股股票代码
        limit: 返回研报最大条数，默认5
    """
    try:
        df = ak.stock_research_report_em(symbol=symbol)
        records = df.head(limit).to_dict(orient="records")
        return json.dumps(records, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.exception("get_stock_research_report error")
        return json.dumps({"error": f"获取券商研报失败: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def get_stock_news(symbol: str, limit: int = 8) -> str:
    """
    获取个股最新相关新闻
    Args:
        symbol: A股股票代码
        limit: 返回新闻最大条数，默认8
    """
    try:
        df = ak.stock_news_em(symbol=symbol)
        records = df.head(limit).to_dict(orient="records")
        return json.dumps(records, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.exception("get_stock_news error")
        return json.dumps({"error": f"获取个股新闻失败: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def get_financial_indicator(symbol: str) -> str:
    """
    获取股票最新核心财务指标，营收、净利润、ROE等
    Args:
        symbol: A股股票代码
    """
    try:
        df = ak.stock_financial_analysis_indicator(symbol=symbol)
        latest_data = df.head(2).to_dict(orient="records")
        return json.dumps(latest_data, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.exception("get_financial_indicator error")
        return json.dumps({"error": f"获取财务指标失败: {str(e)}"}, ensure_ascii=False)