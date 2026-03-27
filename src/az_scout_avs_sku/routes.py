"""API routes for AVS SKU and pricing data."""

from typing import Any

from az_scout.plugin_api import PluginUpstreamError, PluginValidationError
from fastapi import APIRouter

from az_scout_avs_sku.avs_data import get_avs_sku_technical_data, get_avs_skus_for_region

router = APIRouter()


@router.get("/technical-skus")
def technical_skus() -> list[dict[str, Any]]:
    """Return raw AVS SKU technical specifications (no pricing, no region context)."""
    return get_avs_sku_technical_data()


@router.get("/skus")
def skus(
    region: str = "",
    byol: bool = True,
    sku: str = "",
    pricing_source: str = "public",
    subscription_id: str = "",
) -> dict[str, object]:
    """Return AVS SKUs with technical data and optional regional pricing."""
    normalized_region = region.strip().lower()
    normalized_sku = sku.strip()
    normalized_pricing_source = pricing_source.strip().lower() or "public"
    normalized_subscription_id = subscription_id.strip()

    try:
        return get_avs_skus_for_region(
            region=normalized_region,
            byol=byol,
            sku=normalized_sku,
            pricing_source=normalized_pricing_source,
            subscription_id=normalized_subscription_id,
        )
    except ValueError as exc:
        raise PluginValidationError(str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise PluginUpstreamError(
            f"Failed to load AVS SKU data for region '{normalized_region}': {exc}"
        ) from exc
