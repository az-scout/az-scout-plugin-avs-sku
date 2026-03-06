"""API routes for AVS SKU and pricing data."""

from fastapi import APIRouter, HTTPException

from az_scout_avs_sku.avs_data import get_avs_skus_for_region

router = APIRouter()


@router.get("/skus")
async def skus(
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
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=502,
            detail=f"Failed to load AVS SKU data for region '{normalized_region}': {exc}",
        ) from exc
