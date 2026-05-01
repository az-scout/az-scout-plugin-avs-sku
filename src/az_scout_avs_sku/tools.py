"""MCP tools for AVS SKU lookups."""

import json
from typing import Any

from az_scout_avs_sku.avs_data import get_avs_sku_technical_data, get_avs_skus_for_region


def avs_sku_technical_data_tool() -> str:
    """Get AVS SKU technical specifications (CPU, RAM, vSAN) without pricing or region context.

    Returns the full list of known AVS SKU hardware specs. Useful for sizing
    calculations, comparisons, and as input data for other tools or plugins.
    """
    try:
        data: list[dict[str, Any]] = get_avs_sku_technical_data()
        return json.dumps(data, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        return json.dumps({"error": str(exc)})


def avs_sku_tool(
    region: str | None = None,
    byol: bool = True,
    sku: str | None = None,
    pricing_source: str = "public",
    subscription_id: str | None = None,
) -> str:
    """Get AVS SKU list with optional region, SKU filtering, and pricing scope selection.

    Parameters
    ----------
    region:
        Azure region name (e.g. ``"eastus"``, ``"westeurope"``). When omitted,
        only technical specifications are returned without any pricing data.
    byol:
        When ``True`` (default), return BYOL (Bring Your Own License) prices.
        When ``False``, return full-license (non-BYOL) prices.
    sku:
        Filter results to a specific SKU name (e.g. ``"AV36P"``). Case-insensitive
        substring match. When omitted, all known SKUs are returned.
    pricing_source:
        One of ``"public"`` (default) to use the Azure public retail price list, or
        ``"subscription"`` to fetch prices from the subscription's Consumption Price
        Sheet (requires ``subscription_id`` and an EA/MCA billing account).
    subscription_id:
        Azure subscription ID. Required when ``pricing_source="subscription"``.
        Ignored when ``pricing_source="public"``.
    """
    try:
        normalized_region = (region or "").strip().lower()
        normalized_sku = (sku or "").strip()
        normalized_pricing_source = pricing_source.strip().lower() or "public"
        normalized_subscription_id = (subscription_id or "").strip()
        payload: dict[str, Any] = get_avs_skus_for_region(
            region=normalized_region,
            byol=byol,
            sku=normalized_sku,
            pricing_source=normalized_pricing_source,
            subscription_id=normalized_subscription_id,
        )
        return json.dumps(payload, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        return json.dumps({"error": str(exc)})
