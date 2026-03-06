import json
from unittest.mock import patch

from az_scout_avs_sku.tools import avs_sku_tool


def test_avs_sku_tool_returns_json_string_payload() -> None:
    payload = {
        "region": "eastus",
        "byol": True,
        "sku_filter": "AV64",
        "pricing_source": "public",
        "subscription_id": "",
        "source": {"technical": "https://example.test/sku.json", "pricing": "https://example.test"},
        "items": [],
    }

    with patch("az_scout_avs_sku.tools.get_avs_skus_for_region", return_value=payload) as mocked:
        result = avs_sku_tool(
            region=" EastUS ",
            byol=True,
            sku=" av64 ",
            pricing_source=" Public ",
            subscription_id=" ",
        )

    assert isinstance(result, str)
    assert json.loads(result) == payload
    mocked.assert_called_once_with(
        region="eastus",
        byol=True,
        sku="av64",
        pricing_source="public",
        subscription_id="",
    )


def test_avs_sku_tool_supports_default_arguments() -> None:
    payload = {
        "region": "",
        "byol": True,
        "sku_filter": "",
        "pricing_source": "public",
        "subscription_id": "",
        "source": {"technical": "https://example.test/sku.json", "pricing": None},
        "items": [],
    }

    with patch("az_scout_avs_sku.tools.get_avs_skus_for_region", return_value=payload) as mocked:
        result = avs_sku_tool()

    assert json.loads(result) == payload
    mocked.assert_called_once_with(
        region="",
        byol=True,
        sku="",
        pricing_source="public",
        subscription_id="",
    )
