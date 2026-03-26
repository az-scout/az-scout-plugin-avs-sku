# az-scout-plugin-avs-sku

[az-scout](https://az-scout.com) plugin for Azure VMware Solution (AVS) SKU exploration.

## Plugin role

This plugin helps compare AVS SKUs by combining:

- **technical specs** (CPU, RAM, cores, architecture, vSAN) bundled as static data,
- **regional retail pricing** (PAYG and reservation monthly equivalents),
- **generation labels** (Generation 1 / Generation 2 when applicable by region).

## Features

- **AVS SKU tab** (`AVS SKU`) with BYOL toggle and pricing display mode selector.
- **Pricing scope selector**: public prices list, or selected subscription scope.
- **AVS generation awareness**.
- **Chat integration**:
  - MCP tools: `avs_sku_tool`, `avs_sku_technical_data_tool`
  - custom chat mode: `avs-sku-advisor`
  - default-mode addendum for AV* SKU interpretation.

## REST API

Base path (mounted by az-scout):

`/plugins/avs-sku`

### Endpoints

#### `GET /plugins/avs-sku/technical-skus`

Returns the raw AVS SKU technical specifications (no pricing, no region context).

**Response shape:**

```json
[
    {
        "name": "AV36",
        "cores": 36,
        "ram": 576,
        "cpu_model": "Intel Xeon Gold 6140",
        "cpu_architecture": "Skylake",
        "cpu_speed_ghz": 2.3,
        "cpu_turbo_speed_ghz": 3.7,
        "cpu_number": 2,
        "logical_threads_with_hyperthreading": 72,
        "vsan_architecture": "OSA",
        "vsan_cache_capacity_in_tb": 3.2,
        "vsan_cache_storage_technology": "NVMe",
        "vsan_capacity_tier_in_tb": 15.2,
        "vsan_capacity_tier_storage_technology": "SSD"
    }
]
```

#### `GET /plugins/avs-sku/skus`

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
        "technical": "bundled (az-scout-plugin-avs-sku)",
        "pricing": "https://prices.azure.com/api/retail/prices"
    },
    "items": [
        {
            "name": "AV64",
            "technical": { "...": "..." },
            "generation_labels": ["Generation 1", "Generation 2"],
            "stretched_cluster": false,
            "available_in_region": true,
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

## MCP tools

### `avs_sku_technical_data_tool`

Returns AVS SKU technical specifications (CPU, RAM, vSAN) as a JSON string. No parameters.

### `avs_sku_tool`

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
uv pip install az-scout-plugin-avs-sku
az-scout  # plugin is auto-discovered
```

For development:

```bash
git clone https://github.com/az-scout/az-scout-plugin-avs-sku
cd az-scout-plugin-avs-sku
uv sync --group dev
uv pip install -e .
az-scout  # plugin is auto-discovered
```

## Structure

```
src/az_scout_avs_sku/
├── __init__.py
├── avs_data.py
├── routes.py
├── tools.py
└── static/
    ├── css/avs-sku.css
    ├── data/sku.json
    ├── html/avs-sku-tab.html
    └── js/avs-sku-tab.js
```

## Quality checks

```bash
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/
uv run pytest
```

## Copilot support

The `.github/copilot-instructions.md` file provides context to GitHub Copilot about
the plugin structure, conventions, and az-scout plugin API.

## Using AVS SKU data from another plugin

Other az-scout plugins can consume AVS SKU technical data by adding this plugin as a dependency.

### 1. Add the dependency

In your plugin's `pyproject.toml`:

```toml
[project]
dependencies = [
    "az-scout>=2026.3.4",
    "az-scout-plugin-avs-sku",
    # ...
]
```

### 2. Import directly (recommended for backend code)

```python
from az_scout_avs_sku.avs_data import get_avs_sku_technical_data

skus = get_avs_sku_technical_data()
# Returns: list[dict[str, Any]] — the full list of AVS SKU specs
```

### 3. Call the API endpoint (recommended for frontend code)

```javascript
const response = await fetch("/plugins/avs-sku/technical-skus");
const skus = await response.json();
// Returns: array of SKU objects
```

### 4. Use the MCP tool (for AI chat integrations)

The `avs_sku_technical_data_tool` is automatically available in the AI chat when both plugins are installed.

## License

[MIT](LICENSE.txt)

## Disclaimer

> **This tool is not affiliated with Microsoft.** All capacity, pricing, and availability information is indicative and not a guarantee of deployment success. Values are dynamic and may change between planning and actual deployment. Always validate in official Microsoft sources and in your target tenant/subscription.
