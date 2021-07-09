import functions as f
import constants as c
from classes import VatsimController
from datetime import datetime
import threading
import time

loop_end_time = 0
afv_data = None


def refresh_loop(fetch_afv: bool):
    global afv_data
    global loop_end_time
    if fetch_afv or afv_data is None:
        log_print('Fetching AFV Data')
        afv_data = f.get_json_from_url(f.get_afv_url())
    log_print('Fetching VATSIM Data')
    VatsimController.copy_controllers()
    f.add_controller_coordinates(afv_data)
    f.get_vatsim_controllers()
    log_print('VATSIM data loaded')
    log_print('Online controllers:')

    local_online_controllers = []
    callsign_max_length = 0
    for controller in VatsimController.vatsim_atc:
        location = controller.get_position()
        is_in_defined_airpsace = f.is_point_in_polygon(location)
        if is_in_defined_airpsace or controller.callsign in atc_positions:
            local_online_controllers.append(controller)
            if len(controller.callsign) > callsign_max_length:
                callsign_max_length = len(controller.callsign)

    if len(local_online_controllers) > 0:
        header = '{0:{1}} {2:20} {3}'.format('Callsign', callsign_max_length,
                                             'Name', 'Online Time')
        log_print(header)
        local_online_controllers.sort(key=lambda x: x.callsign)
        for controller in local_online_controllers:
            session_time = controller.get_session_time()
            hours = str(session_time[0]).zfill(2)
            minutes = str(session_time[1]).zfill(2)
            controller_output = '{0:{1}} - {2:20} {3}:{4}'.format(
                controller.callsign, callsign_max_length, controller.name,
                hours, minutes)
            log_print(controller_output)
    else:
        log_print("No controllers found")
    VatsimController.clean_controllers()
    loop_end_time = time.time()


def log_print(label: str):
    print('{}: {}'.format(datetime.now().strftime('%H:%M:%S.%f')[:12], label))


def average_run_calc(total_loop_time, total_runs) -> float:
    return round(total_loop_time / total_runs, 3)


if __name__ == "__main__":
    log_print('Starting')
    log_print("VATSIM Online Controllers v{}".format(c.VERSION))
    f.import_config(c.CONFIG_FILENAME)
    log_print('Config loaded')
    afv_api_url = f.get_afv_url()
    # afv_data = f.get_json_from_url(afv_api_url)
    # log_print('AFV data loaded')
    atc_positions = f.get_atc_positions()
    log_print('POF file loaded')

    event = threading.Event()
    afv_update_counter = 0

    afv_refreshes = 0
    afv_total_run_time = 0
    afv_avg_refresh = 0
    nonafv_refreshes = 0
    nonafv_total_run_time = 0
    nonafv_avg_refresh = 0
    while True:
        try:
            print()
            log_print('Refreshing...')
            loop_start_time = time.time()
            if afv_update_counter % 3 == 0:
                refresh_loop(True)
                afv_refreshes += 1
                afv_total_run_time += round(loop_end_time - loop_start_time, 3)
                afv_avg_refresh = average_run_calc(afv_total_run_time,
                                                   afv_refreshes)
            else:
                refresh_loop(False)
                nonafv_refreshes += 1
                nonafv_total_run_time += round(loop_end_time - loop_start_time,
                                               3)
                nonafv_avg_refresh = average_run_calc(nonafv_total_run_time,
                                                      nonafv_refreshes)
            afv_update_counter += 1
            loop_running_time = round(loop_end_time - loop_start_time, 3)
            log_print('Refresh run time = {}s'.format(loop_running_time))
            log_print('Average refresh time w/o AFV = {}s'.format(
                nonafv_avg_refresh))
            log_print(
                'Average refresh time with AFV= {}s'.format(afv_avg_refresh))
            event.wait(c.REFRESH_TIME)
        except KeyboardInterrupt:
            event.set()
            break
