import functions as f
import constants as c
from classes import VatsimController

if __name__ == "__main__":
    f.import_config(c.CONFIG_FILENAME)
    afv_api = f.get_afv_url()
    print(afv_api)

    afv_data = f.get_json_from_url(afv_api)
    f.add_controller_coordinates(afv_data)

    f.get_vatsim_controllers()
    for controller in VatsimController.vatsim_controllers:
        location = controller.get_position()
        is_displayed = f.is_point_in_polygon(location)
        if is_displayed:
            print(controller.callsign, controller.name, location)
