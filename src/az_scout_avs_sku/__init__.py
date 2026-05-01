"""az-scout AVS SKU plugin.

Adds Azure VMware Solution (AVS) SKU exploration with regional
pricing, generation compatibility, and technical specifications.
"""

from __future__ import annotations

from collections.abc import Callable
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from az_scout.plugin_api import ChatMode, TabDefinition
    from fastapi import APIRouter

_STATIC_DIR = Path(__file__).parent / "static"

try:
    __version__ = _pkg_version("az-scout-plugin-avs-sku")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"


class AvsSkuPlugin:
    """az-scout AVS SKU plugin.

    Adds Azure VMware Solution (AVS) SKU exploration with regional
    pricing, generation compatibility, and technical specifications.
    """

    name = "avs-sku"
    version = __version__

    def get_router(self) -> APIRouter | None:
        """Return API routes, or None to skip."""
        from az_scout_avs_sku.routes import router

        return router

    def get_mcp_tools(self) -> list[Callable[..., Any]] | None:
        """Return MCP tool functions, or None to skip."""
        from az_scout_avs_sku.tools import avs_sku_technical_data_tool, avs_sku_tool

        return [avs_sku_tool, avs_sku_technical_data_tool]

    def get_static_dir(self) -> Path | None:
        """Return path to static assets directory, or None to skip."""
        return _STATIC_DIR

    def get_tabs(self) -> list[TabDefinition] | None:
        """Return UI tab definitions, or None to skip."""
        from az_scout.plugin_api import TabDefinition

        return [
            TabDefinition(
                id="avs-sku",
                label="AVS SKU",
                icon="bi bi-puzzle",
                js_entry="js/avs-sku-tab.js",
                css_entry="css/avs-sku.css",
            )
        ]

    def get_chat_modes(self) -> list[ChatMode] | None:
        """Return chat mode definitions, or None to skip."""
        from az_scout.plugin_api import ChatMode

        return [
            ChatMode(
                id="avs-sku-advisor",
                label="AVS SKU Advisor",
                system_prompt=(
                    "You are an Azure VMware Solution (AVS) SKU advisor. "
                    "Help users compare AVS SKU capabilities and prices by region. "
                    "Use the avs_sku_tool when regional pricing or capability data is needed. "
                    "Explain differences between SKUs "
                    "(CPU, RAM, vSAN architecture, generation labels) "
                    "and pricing modes (PAYG hourly/monthly, reservations). "
                    "Generation compatibility source of truth is generation_labels "
                    "from avs_sku_tool output. "
                    "Never infer Generation 2 compatibility from CPU model, "
                    "vSAN architecture, or SKU family name. "
                    "When suggesting Gen 2 alternatives, only suggest SKUs "
                    "where generation_labels includes 'Generation 2' "
                    "for the same queried region. "
                    "If no such SKU exists (or tool data is missing/unclear), "
                    "say so explicitly and do not guess alternatives. "
                    "A SKU with available_in_region=false (no pricing data) "
                    "is NOT available in that region — do not recommend it. "
                    "Only present SKUs that are available_in_region=true. "
                    "Stretched Clusters are AVS SDDCs that leverage Azure region "
                    "Availability Zone support to provide High Availability and very "
                    "low RTO to replicated workloads. "
                    "The stretched_cluster field indicates whether a SKU supports "
                    "Stretched Clusters in the queried region. "
                    "Call out uncertainty when availability may have changed "
                    "and recommend checking official Microsoft docs."
                    "Be concise (important) but informative,"
                    "and use bullet points or tables for comparisons when helpful."
                ),
                welcome_message=(
                    "Ask me about AVS SKU sizing, generation compatibility, "
                    "and regional pricing (PAYG or reservation). "
                    "Try:\n"
                    "- [[What are the SKU available in this region?]]\n"
                    "- [[What is the CPU architecture of AV36P?]]\n"
                    "- [[Is AVS Gen 2 available in this region?]]"
                ),
            )
        ]

    def get_system_prompt_addendum(self) -> str | None:
        """Return extra guidance for the default discussion chat mode, or None."""
        return (
            "If the user references a SKU whose name starts with 'AV' (e.g., 'AV64'), "
            "interpret it as Azure VMware Solution (AVS) related ask. "
            "Use avs_sku_tool for AVS SKU capability, generation, and pricing questions. "
            "If region is missing, request or infer only technical specs (no regional pricing). "
            "For Gen 2 compatibility, rely only on generation_labels returned by avs_sku_tool "
            "and do not infer from CPU model or vSAN architecture. "
            "When suggesting alternatives, keep them in the same region and use the same "
            "pricing source selected by the user: 'Use public prices list' or "
            "'Use selected subscription'. "
            "A SKU with available_in_region=false (no pricing data) is NOT available "
            "in that region — do not recommend it. "
            "Stretched Clusters are AVS SDDCs using Azure region Availability Zone "
            "support for High Availability and very low RTO. "
            "The stretched_cluster field indicates regional support."
        )


# Module-level instance — referenced by the entry point
plugin = AvsSkuPlugin()
