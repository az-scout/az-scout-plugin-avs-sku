# az-scout-plugin-avs-sku

az-scout plugin for Azure VMware Solution (AVS) SKU exploration.

It adds:

- an AVS SKU UI tab in az-scout,
- a REST API route that returns technical SKU data and optional regional pricing,
- an MCP tool for AI/chat workflows,
- an AVS-focused chat mode.

## Plugin role

This plugin helps compare AVS SKUs by combining:

- **technical specs** (CPU, RAM, cores, architecture, vSAN) from upstream SKU metadata,
- **regional retail pricing** (PAYG and reservation monthly equivalents),
- **generation labels** (Generation 1 / Generation 2 when applicable by region).

## Features

- **AVS SKU tab** (`AVS SKU`) with BYOL toggle and pricing display mode selector.
- **Pricing scope selector**: public prices list, or selected subscription scope.
- **AVS generation awareness**.
- **Chat integration**:
  - MCP tool: `avs_sku_tool`
  - custom chat mode: `avs-sku-advisor`
  - default-mode addendum for AV* SKU interpretation.

## REST API

Base path (mounted by az-scout):

`/plugins/avs-sku`

### Endpoint

`GET /plugins/avs-sku/skus`

### Query parameters

- `region` (optional, string): Azure region key (for example `eastus`).
- `byol` (optional, bool, default `true`): include BYOL pricing rows.
- `sku` (optional, string): filter SKUs by name fragment.
- `pricing_source` (optional, string, default `public`): `public` or `subscription`.
- `subscription_id` (optional, string): selected subscription when `pricing_source=subscription`.

### Behavior notes

- If `region` is omitted, response still includes technical SKU data, but no regional pricing lookup.
- Current pricing retrieval uses Azure Retail Prices API. `pricing_source` and `subscription_id` are preserved in response metadata for scope continuity.

### Response shape (summary)

```json
{
    "region": "eastus",
    "byol": true,
    "sku_filter": "AV64",
    "pricing_source": "public",
    "subscription_id": "",
    "source": {
        "technical": "https://.../sku.json",
        "pricing": "https://prices.azure.com/api/retail/prices"
    },
    "items": [
        {
            "name": "AV64",
            "technical": { "...": "..." },
            "generation_labels": ["Generation 1", "Generation 2"],
            "price": {
                "found": true,
                "byol": true,
                "currency_code": "USD",
                "payg_hour": 12.34,
                "payg_month": 9008.2,
                "reservation_1y_month": 7000.0,
                "reservation_3y_month": 5400.0,
                "reservation_5y_month": 4900.0
            }
        }
    ]
}
```

## MCP tool

Tool name: `avs_sku_tool`

### Parameters

- `region: str | None = None`
- `byol: bool = True`
- `sku: str | None = None`
- `pricing_source: str = "public"`
- `subscription_id: str | None = None`

### Return value

- Returns a **JSON string** (serialized payload) with the same structure as the REST endpoint.

## Setup

```bash
uv sync --group dev
uv pip install -e .
az-scout
```

## Project structure

```
src/az_scout_avs_sku/
├── __init__.py
├── avs_data.py
├── routes.py
├── tools.py
└── static/
        ├── css/avs-sku.css
        ├── html/avs-sku-tab.html
        └── js/avs-sku-tab.js
tests/
├── test_routes.py
└── test_tools.py
```

## Quality checks

```bash
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/
uv run pytest
```

## License

[MIT](LICENSE.txt)

## Disclaimer

> **This tool is not affiliated with Microsoft.** SKU, pricing, and availability information is indicative and can change. Always validate final sizing, generation availability, and cost in official Microsoft sources and in your target tenant/subscription before deployment.
