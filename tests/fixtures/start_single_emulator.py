import json
import os

from flask import Flask, jsonify, request, send_from_directory
import argparse
import logging

### If no parameters are specified, show the models to choose from
### Flask only allows one app.run at the same time

def file_content_or_error(response_directory, filename):
    file = os.path.join(response_directory, filename)
    if os.path.exists(file):
        with open(file) as f:
            content = f.read().strip()
            if "\"code\": 404" in content:
                return jsonify({"error": "", "code": 404}), 404
            else:
                return send_from_directory(response_directory, filename)
    else:
        return jsonify({"error": "{ \"code\":400.03}"}), 400

def register_routes(app, response_directory):

    @app.route("/ai", methods=["GET"])
    def handle_ai_request():
        # extract params from request
        command = request.args.get('command')
        if command == "getDeviceStatus":
            return file_content_or_error(response_directory, "ai_get_devicestatus.json")
        elif command == "getFWVersion":
            return file_content_or_error(response_directory, "ai_get_fwversion.json")
        elif command == "getLastPUSHNotifications":
            return file_content_or_error(response_directory, "ai_get_lastpushnotifications.json")
        elif command == "getMacAddress":
            return file_content_or_error(response_directory, "ai_get_macaddress.txt")
        elif command == "getModelDescription":
            return file_content_or_error(response_directory, "ai_get_modeldescription.txt")
        elif command == "getUpdateStatus":
            return file_content_or_error(response_directory, "ai_get_updatestatus.json")
        else:
            return file_content_or_error(response_directory, "ai_get_invalid_command.txt"), 404

    @app.route("/hh", methods=["GET"])
    def handle_hh_request():
        # extract params from request
        command = request.args.get('command')
        value = request.args.get('value')
        #cache_avoidance_number = request.args.get('_')

        if command == "getCategories":
            result = []
            with open(os.path.join(response_directory, "hh_get_categories.json")) as f:
                categories_content = json.loads(f)
                for category in categories_content:
                    result.append(category["id"])

        elif command == "getCategory":

            with open(os.path.join(response_directory, "hh_get_categories.json")) as f:
                categories_content = json.loads(f)

                # Find category that matches the value
                matching_category = next((c for c in categories_content if c["id"] == value), None)
                if matching_category:
                    result.append(matching_category)
                    return jsonify(matching_category["category"])
                else:
                    return jsonify({"error": ["code", "400.03"]}), 400

        elif command == "getCommands":
            with open(os.path.join(response_directory, "hh_get_categories.json")) as f:
                categories_content = json.loads(f)

                # Find category that matches the value
                matching_category = next((c for c in categories_content if c["id"] == value), None)
                if matching_category:
                    result.append(matching_category)
                    return jsonify(matching_category["commands"])
                else:
                    return jsonify({"error": ["code", "400.03"]}), 400

        elif command == "getEcoInfo":
            return file_content_or_error(response_directory, "hh_get_ecoinfo.json")
        elif command == "getFWVersion":
            return file_content_or_error(response_directory, "hh_get_fwversion.json")
        elif command == "getZHMode":
            return file_content_or_error(response_directory, "hh_get_zhmode.json")
        else:
            return file_content_or_error(response_directory, "hh_get_invalid_command.txt"), 404

    # add default route
    @app.route("/", methods=["GET"])
    def handle_default_request():
        logging.ERROR("Invalid URL '/'. Request parameters:")
        for key, value in request.args.items():
            logging.ERROR(f"{key}: {value}")


def start_emulator(port, device_id):
    """ Get the project root from the environment variable """
    project_root = os.getenv("PROJECT_ROOT")
    if not project_root:
        raise ValueError("PROJECT_ROOT environment variable is not set.")

    response_directory = os.path.join(os.getenv("PROJECT_ROOT"), "tests/fixtures", device_id)

    # check if the directory for the desired device exists
    if not os.path.exists(response_directory):
        raise ValueError(f"Directory {response_directory} does not exist.")

    # Create a Flask app
    app = Flask(f"V-Zug Emulator {device_id}")

    # Register routes
    register_routes(app, response_directory)

    # Run the app
    app.run(port=port, debug=False, threaded=True)

def select_device() -> str:
    """ Used for interactive debugging, when no command line parameters are provided """

    response_root = f"{os.getenv("PROJECT_ROOT")}/tests/fixtures"

    # Show list of subdirectories in the current directory
    subdirectories = [d for d in os.listdir(response_root) if os.path.isdir(os.path.join(response_root, d))]

    # Select the device to be used
    print("Devices:")
    for idx, subdir in enumerate(subdirectories, start=1):
        print(f"{idx}: {subdir}")

    response_id = input("Please enter device # use: ")
    if not response_id.isdigit() or int(response_id) < 1 or int(response_id) > len(subdirectories):
        print("Invalid device ID. Please enter a valid number.")
        exit(1)

    return subdirectories[int(response_id)]

def main() -> None:
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--port', type=int, required=False,help='Port number to run the emulator on')
    parser.add_argument('--device_id', type=str, required=False, help='Device ID to emulate')

    args = parser.parse_args()

    if args.port and args.device_id:
        start_emulator(args.port, args.device_id)
    else:
        print ("No port or device_id provided, starting interactive mode.")
        device = select_device()
        start_emulator(80, device)

if __name__ == "__main__":
    main()
