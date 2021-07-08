import functions as f
import constants as c
from classes import VatsimController
from datetime import datetime
import threading


def refresh_loop(afv_counter: int):
    global afv_data
    if afv_counter > 10:
        afv_data = f.get_json_from_url(f.get_afv_url())
    print()
    print("Refresh time: {}".format(datetime.now().isoformat()[:-7]))
    VatsimController.copy_controllers()
    f.add_controller_coordinates(afv_data)
    print("Currently online controllers:")
    f.get_vatsim_controllers()
    controllers_online = 0
    for controller in VatsimController.vatsim_atc:
        location = controller.get_position()
        is_in_defined_airpsace = f.is_point_in_polygon(location)
        if is_in_defined_airpsace or controller.callsign in atc_positions:
            controllers_online += 1
            print(controller.callsign, controller.name, location)
    if controllers_online == 0:
        print("Currently no controllers online")
    VatsimController.clean_controllers()


if __name__ == "__main__":
    print("VATSIM Online Controllers v{}".format(c.VERSION))
    f.import_config(c.CONFIG_FILENAME)
    afv_api_url = f.get_afv_url()
    afv_data = f.get_json_from_url(afv_api_url)
    atc_positions = f.get_atc_positions()

    event = threading.Event()
    afv_update_counter = 0
    while True:
        try:
            afv_update_counter += 1
            refresh_loop(afv_update_counter)
            event.wait(c.REFRESH_TIME)
        except KeyboardInterrupt:
            event.set()
            break
