import custom_components.vzug.api as api

import re
import aiohttp
import pytest

import tests.fixtures.adora_tslq_wp.decoded.expected_result as expected_result

BASE_URL = "http://10.0.0.90"

# Doing a fixture to create vzug_client not yet work. Async & Fixture seems a bad combo

@pytest.mark.asyncio
async def test_ai_get_device_status():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        device_status = await vzug_client.get_device_status()

        # Assertions using dictionary key access
        assert device_status["DeviceName"] == expected_result.ai_device_status["DeviceName"]
        assert is_valid_serial_type_1(device_status["Serial"])
        assert device_status["Inactive"] == expected_result.ai_device_status["Inactive"]
        assert device_status["Program"] == expected_result.ai_device_status["Program"]
        assert device_status["Status"] == expected_result.ai_device_status["Status"]
        assert device_status["ProgramEnd"]["End"] == expected_result.ai_device_status["ProgramEnd"]["End"]
        assert device_status["ProgramEnd"]["EndType"] == expected_result.ai_device_status["ProgramEnd"]["EndType"]
        assert is_valid_serial_type_2(device_status["deviceUuid"])


@pytest.mark.asyncio
async def test_ai_get_fw_version():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        fw_version = await vzug_client.get_ai_fw_version()

        assert is_valid_serial_type_1(fw_version["fn"])
        assert fw_version["SW"] == expected_result.ai_firmware_version["SW"]
        assert fw_version["SD"] == expected_result.ai_firmware_version["SD"]
        assert fw_version["HW"] == expected_result.ai_firmware_version["HW"]
        assert fw_version["apiVersion"] == expected_result.ai_firmware_version["apiVersion"]
        assert fw_version["phy"] == expected_result.ai_firmware_version["phy"]
        assert is_valid_serial_type_2(fw_version["deviceUuid"])

@pytest.mark.asyncio
async def test_ai_get_last_push_notifica():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        last_push_notifican = await vzug_client.get_last_push_notifications()

@pytest.mark.asyncio
async def test_ai_get_model_description():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        model_description = await vzug_client.get_model_description()
        assert model_description == expected_result.ai_model_description

@pytest.mark.asyncio
async def test_ai_get_mac_address():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        mac_info = await vzug_client.get_mac_address()
        assert is_valid_macaddr802(mac_info)

@pytest.mark.asyncio
async def test_ai_get_last_push_notifications():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        last_push_notifications = await vzug_client.get_last_push_notifications()

        for i in range(len(expected_result.ai_last_push_notifications)):
            assert last_push_notifications[i]["date"] == expected_result.ai_last_push_notifications[i]["date"]
            assert last_push_notifications[i]["message"] == expected_result.ai_last_push_notifications[i]["message"]

@pytest.mark.asyncio
async def test_ai_get_update_status():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        update_status = await vzug_client.get_update_status()

        assert update_status["status"] == expected_result.ai_update_status["status"]
        assert update_status["isAIUpdateAvailable"] == expected_result.ai_update_status["isAIUpdateAvailable"]
        assert update_status["isHHGUpdateAvailable"] == expected_result.ai_update_status["isHHGUpdateAvailable"]
        assert update_status["isSynced"] == expected_result.ai_update_status["isSynced"]

        for i in range(len(expected_result.ai_update_status["components"])):
            assert update_status["components"][i]["name"] == expected_result.ai_update_status["components"][i]["name"]
            assert update_status["components"][i]["running"] == expected_result.ai_update_status["components"][i]["running"]
            assert update_status["components"][i]["available"] == expected_result.ai_update_status["components"][i]["available"]
            assert update_status["components"][i]["required"] == expected_result.ai_update_status["components"][i]["required"]
            assert update_status["components"][i]["progress"]["download"] == expected_result.ai_update_status["components"][i]["progress"]["download"]
            assert update_status["components"][i]["progress"]["installation"] == expected_result.ai_update_status["components"][i]["progress"]["installation"]


@pytest.mark.asyncio
async def test_hh_get_categories_and_hh_get_category():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        categories = await vzug_client.list_categories()

        assert len(categories) > 0
        for i in range(len(expected_result.hh_categories)):
            category = await vzug_client.get_category(categories[i])
            assert categories[i] == expected_result.hh_categories[i][0]
            assert category == expected_result.hh_categories[i][1]

@pytest.mark.asyncio
async def test_hh_get_eco_info():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        eco_info = await vzug_client.get_eco_info()

        assert eco_info["energy"]["total"]   == expected_result.hh_eco_info["energy"]["total"]
        assert eco_info["energy"]["average"] == expected_result.hh_eco_info["energy"]["average"]
        assert eco_info["energy"]["program"] == expected_result.hh_eco_info["energy"]["program"]

@pytest.mark.asyncio
async def test_hh_get_fw_version():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        fw_version = await vzug_client.get_hh_fw_version()

        for key, value in expected_result.hh_firmware_version.items():
            if key == "fn" or key == "Serial":
                assert is_valid_serial_type_1(fw_version[key])
            elif  key == "an" or key == "deviceUuid":
                assert is_valid_serial_type_2(fw_version[key])
            else:
                # For other keys, just compare the values directly
                assert fw_version[key].strip() == value.strip()

@pytest.mark.asyncio
async def x_test_hh_get_zh_mode():
    async with aiohttp.ClientSession() as session:
        vzug_client = api.VZugApi(session, BASE_URL)

        zh_mode = await vzug_client.get_zh_mode()


def is_valid_macaddr802(value):
    return  re.search("^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$|^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$", value, re.IGNORECASE) is not None


def is_valid_serial_type_1(value):
    ### Check if serial number is of the form 12345 123456
    return re.search("^[0-9]{5} [0-9]{6}$", value) is not None

def is_valid_serial_type_2(value):
    ### Check for 10 digit serial number or deviceUUID
    return re.search("^[0-9]{10}$", value) is not None

