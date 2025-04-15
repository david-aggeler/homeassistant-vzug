import aiohttp
import custom_components.vzug.api as api
import pytest
import tests.fixtures.adora_slq.expected as expected_result
import tests.integration.test_core as test_core

BASE_URL = "http://127.0.0.1:5000"

########################################################################

@pytest.mark.asyncio
async def test_ai_get_device_status():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_ai_get_device_status_core(vzug_client, expected_result)

@pytest.mark.asyncio
async def test_ai_get_fw_version():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_ai_get_fw_version(vzug_client, expected_result)

@pytest.mark.asyncio
async def test_ai_get_last_push_notifications():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_ai_get_last_push_notifications(vzug_client, expected_result)

@pytest.mark.asyncio
async def test_ai_get_model_description():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_ai_get_model_description(vzug_client, expected_result)

@pytest.mark.asyncio
async def test_ai_get_mac_address():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_ai_get_mac_address(vzug_client)

@pytest.mark.asyncio
async def test_ai_get_update_status():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_ai_get_update_status(vzug_client, expected_result)

@pytest.mark.asyncio
async def test_hh_get_categories_and_commands():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_hh_get_categories_and_commands(vzug_client, expected_result)

@pytest.mark.asyncio
async def test_hh_get_eco_info():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_hh_get_eco_info(vzug_client, expected_result)

@pytest.mark.asyncio
async def test_hh_get_fw_version():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_hh_get_fw_version(vzug_client, expected_result)

@pytest.mark.asyncio
async def test_hh_get_zh_mode():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)
        await test_core.assert_hh_get_zh_mode(vzug_client, expected_result)

