import functions as f
import constants as c
from classes import VatsimController
from datetime import datetime
import threading


def refresh_loop():
    f.add_controller_coordinates(afv_data)
    print("Currently online controllers:")
    f.get_vatsim_controllers()
    for controller in VatsimController.vatsim_controllers:
        location = controller.get_position()
        is_in_defined_airpsace = f.is_point_in_polygon(location)
        if is_in_defined_airpsace or controller.callsign in atc_positions:
            print(controller.callsign, controller.name, location)


if __name__ == "__main__":
    print("VATSIM Online Controllers v{}".format(c.VERSION))
    f.import_config(c.CONFIG_FILENAME)
    afv_api_url = f.get_afv_url()
    atc_positions = f.get_atc_positions()

    event = threading.Event()
    afv_update_counter = 0
    while True:
        try:
            afv_update_counter += 1
            if afv_update_counter > 10:
                afv_api_url = f.get_afv_url()
                afv_data = f.get_json_from_url(afv_api_url)
            print()
            print("Refresh time: {}".format(datetime.now().isoformat()[:-7]))
            refresh_loop()
            event.wait(c.REFRESH_TIME)
        except KeyboardInterrupt:
            event.set()
            break
