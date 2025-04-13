import os
import json
import random
from pathlib import Path
import argparse
import requests
import logging

DEVICE_CONF_FILE = "config.json"
RESPONSES_SUBDIR = "responses"

def collect_responses(device_id):
    """
    Collect all JSON responses from predefined URLs and create different results
    """

    config = get_config_from_existing_file(device_id)

    response_root = responses_directory(device_id)

    # with the result from getCategories one should loop through getCategory & getCommands
    url_mapping = {

        "ai_get_devicestatus.json" : "/ai?command=getDeviceStatus",
        "ai_get_fwversion.json" : "/ai?command=getFWVersion",
        "ai_get_lastpushnotifications.json" : "/ai?command=getLastPUSHNotifications",
        "ai_get_macaddress.txt" : "/ai?command=getMacAddress",
        "ai_get_modeldescription.txt" : "/ai?command=getModelDescription",
        "ai_get_updatestatus.json" : "/ai?command=getUpdateStatus",
        "hh_get_categories.json" : "/hh?command=getCategories",
        "hh_get_commands_settings.json" : "/hh?command=getCommands&value=settings",
        "hh_get_ecoinfo.json" : "/hh?command=getEcoInfo",
        "hh_get_fwversion.json" : "/hh?command=getFWVersion",
        "hh_get_zhmode.json" : "/hh?command=getZHMode"   ,
        "ai_get_invalid_command.txt" : "/ai?command=getErrorAnswer42",
        "hh_get_invalid_command.txt" : "/hh?command=getErrorAnswer42"
    }

    for filename, relative_url in url_mapping.items():
        url = config["base_url"] + relative_url

        output_file = os.path.join(response_root, filename)
        response = requests.get(url.strip())

        if relative_url == "/hh?command=getCategories":
            #Special treatment
            a=1
            # collect_categories_details(config["base_url"], response.text)

        elif filename.endswith('.txt'):
            with open(output_file, 'w') as f:
                f.write(response.text)
            logging.info(f"Response saved to {output_file}")

        elif filename.endswith('.json'):
            if "400.03" in response.text:
                logging.error(f"The response from {url} contains 400.03 error.")
            else:
                with open(output_file, 'w') as f:
                    json.dump(response.json(), f, indent=2)
                logging.info(f"Response saved to {output_file}")
        else:
            logging.error(f"Error: Unrecognized file type for {output_file}. Skipped collecting response.")

def collect_categories_details(filename, base_url, response_text):

    # categories = {}

    categories_json = json.loads(response_text)

    for category in categories_json["categories"]:
        category_id = category["id"]
        category_url = f"{base_url}/hh?command=getCategory&value={category_id}"
        category_commands_url = f"{base_url}/hh?command=getCommands&value={category_id}"

        category_response = requests.get(category_url)
        detail_response = requests.get(category_url)

        # category_description = category["description"]

        

        # categories.add(category_description, json.loads(response_text))

        # "hh_get_categories.json" : "/hh?command=getCategories",



        #     "hh_get_category_userxsettings.json" : "/hh?command=getCategory&value=UserXsettings",
        # "hh_get_category_ecomanagement.json" : "/hh?command=getCategory&value=EcoManagement",
        # "hh_get_category_settings.json" : "/hh?command=getCategory&value=settings",
        # "hh_get_command_userxsettings.json" : "/hh?command=getCommands&value=UserXsettings",
        # "hh_get_command_ecomanagement.json" : "/hh?command=getCommands&value=EcoManagement",


def fixtures_directory() -> str:
    return os.path.join(os.getenv("PROJECT_ROOT"), "tests/fixtures")

def device_directory(device_id) -> str:
    return os.path.join(os.getenv("PROJECT_ROOT"), "tests/fixtures", device_id)

def device_config_file(device_id) -> str:
    return os.path.join(os.getenv("PROJECT_ROOT"), "tests/fixtures", device_id, DEVICE_CONF_FILE)

def responses_directory(device_id) -> str:
    return os.path.join(os.getenv("PROJECT_ROOT"), "tests/fixtures", device_id, RESPONSES_SUBDIR)

def is_valid_device(device_id) -> bool:
    return os.path.exists(device_config_file(device_id))

def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

def get_config_from_existing_file(device_id):
    with open(device_config_file(device_id)) as f:
        config = json.load(f)

    return config

def get_config_from_user_and_save(device_id):

    if not os.path.exists(device_directory(device_id)):
        os.makedirs(device_directory(device_id))

        ip_address = input("Please enter IP address: ")

        # Create random serial numbers of format "nnnnn mmmmmm"
        serial_number_1 = f"{random.randint(10000, 99999)} {random.randint(100000, 999999)}"
        serial_number_2 = f"{random.randint(1000000000, 9999999999)}"

        # Create random MAC address of format "02:nn:nn:nn:nn:nn"
        mac_address = "02:" + ":".join(f"{random.randint(0, 255):02x}" for _ in range(5))

        # store in config.json
        config = {
            "base_url": f"http://{ip_address}",
            "fake_mac_address": mac_address,
            "fake_device_serial_1": serial_number_1,
            "fake_device_serial_2": serial_number_2
        }
        with open(device_config_file(device_id), 'w') as f:
            json.dump(config, f, indent=2)


def select_device() -> str:
    """ Used for interactive debugging, when no command line parameters are provided """

    fixtures_root = fixtures_directory()
    # Show list of subdirectories in the current directory
    subdirectories = [d for d in os.listdir(fixtures_root) if os.path.isdir(os.path.join(fixtures_root, d))]

    # Select the device to be used
    print("")
    print("--------------------------------------------------------------------------------------")
    print("Select an existing device or create a new one.")
    print("- When 0 is selected and the device already exists, it will be completely overwritten.")
    print("- When an existing device is selected only the responses will be deleted.")
    print("--------------------------------------------------------------------------------------")
    print(f"0: New device")

    for idx, subdir in enumerate(subdirectories, start=1):
        print(f"{idx}: {subdir}")

    print("")

    response_id = input("Please enter device number: ")

    if int(response_id) == 0:
        device_id = input("Specify new device ID: ")
        if os.path.exists(device_directory(device_id)):
            rmdir(device_directory(device_id))
    else:
        device_id = subdirectories[int(response_id) - 1]

    if not is_valid_device(device_id):
        get_config_from_user_and_save(device_id)

    # Eventually, we want to have multiple responses for the same device
    responses_dir = responses_directory(device_id)
    if os.path.exists(responses_directory(device_id)):
        print(f"Responses for device {device_id} already exists. Delete exiting ones")
        rmdir(responses_dir)
    else:
        os.makedirs(responses_dir)

    return device_id


def main():
    parser = argparse.ArgumentParser(description='Collect JSON responses from predefined URLs into a single file')
    parser.add_argument('--device_id',  required=False, help='Output JSON file path')

    args = parser.parse_args()

    if args.device_id and is_valid_device(args.device_id):
        collect_responses(args.device_id)
    else:
        print ("No port or device_id provided or device config not found. Starting interactive mode.")
        device = select_device()
        collect_responses(device)

if __name__ == '__main__':
    main()
