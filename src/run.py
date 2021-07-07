import functions as f
import constants as c
from classes import VatsimController

if __name__ == "__main__":
    f.import_config("config.ini")
    afv_api = f.get_afv_url()
    print(afv_api)

    afv_data = f.get_json_from_url(afv_api)
    f.add_controller_coordinates(afv_data)

    # Get VATSIM controllers
    controllers = f.get_json_from_url(c.VATSIM_ONLINE_URL).get('controllers')
    for controller in controllers:
        vatsim_id = controller['cid']
        name = controller['name']
        callsign = controller['callsign']
        frequency = controller['frequency']
        facility = controller['facility']
        rating = controller['rating']
        server = controller['server']
        visual_range = controller['visual_range']
        logon_time = controller['logon_time']
        vatsim_controller = VatsimController(vatsim_id, name, callsign,
                                             frequency, facility,
                                             rating, server, visual_range,
                                             logon_time)

    print(VatsimController.vatsim_controllers)
