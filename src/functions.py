import constants
from classes import AfvClient
from classes import AtcPosition
from classes import VatsimController
import os
import configparser
import random
import json
import requests
import datetime
import matplotlib.path as mplpath
import ast

afv_refresh_time = datetime.datetime.now()


def import_config(filename: str) -> None:
    """
    Imports the .ini file specified and sets the constants.
    :param filename: String of the filename of the csv. The file
        is to be located in the same folder as the python file.
    :return: None
    """
    config_file_path = os.path.join(constants.ROOT_DIR, filename)
    print("Loading config at {}".format(config_file_path))
    if not os.path.exists(config_file_path):
        print("'{}' not found. Creating default".format(config_file_path))
        config_file = open(config_file_path, 'w')

        config_w = configparser.ConfigParser()
        config_w.add_section('General')
        config_w.set('General', 'vatsim_online_data_url',
                     constants.VATSIM_ONLINE_URL)
        config_w.set('General', 'controller_filter_area',
                     '{!r}'.format(constants.POLYGON))

        config_w.add_section('Audio For VATSIM')
        config_w.set('Audio For VATSIM', 'api_servers', "{!r}".format(
            constants.AFV_API_SERVERS))
        config_w.set('Audio For VATSIM', 'api_version',
                     constants.AFV_API_VERSION)
        config_w.set('Audio For VATSIM', 'api_post_url',
                     constants.AFV_API_POST_URL)

        config_w.write(config_file)
        config_file.close()

    with open(config_file_path, 'r') as file:
        config_r = configparser.RawConfigParser(allow_no_value=True)
        config_r.read_file(file)

        if config_r.has_option('General', 'vatsim_online_data_url'):
            constants.VATSIM_ONLINE_URL = config_r.get('General',
                                                       'vatsim_online_data_url'
                                                       )
        constants.POLYGON = ast.literal_eval(
            config_r.get('General', 'controller_filter_area'))
        constants.AREA = mplpath.Path(constants.POLYGON)
        constants.AFV_API_SERVERS = ast.literal_eval(
            config_r.get('Audio For VATSIM',
                         'api_servers'))
        constants.AFV_API_VERSION = config_r.get('Audio For VATSIM',
                                                 'api_version')
        constants.AFV_API_POST_URL = config_r.get('Audio For VATSIM',
                                                  'api_post_url')


def get_afv_url() -> str:
    server_selection = random.randint(0, len(constants.AFV_API_SERVERS) - 1)

    server = constants.AFV_API_SERVERS[server_selection]
    version = constants.AFV_API_VERSION
    post_url = constants.AFV_API_POST_URL

    request_url = f"https://{server}/api/v{version}/{post_url}"
    return request_url


def get_json_from_url(url: str) -> json:
    return requests.get(url).json()


def add_controller_coordinates(afv_json: json) -> None:
    for client in afv_json:
        callsign = client.get('callsign')
        if callsign[-3:] in constants.CONTROLLER_SUFFIXES:
            transceivers = client.get('transceivers')
            if len(transceivers) > 0:
                transceiver = client.get('transceivers')[0]
                agl = transceiver['heightAglM']
                if agl < 100:
                    latitude = transceiver['latDeg']
                    longitude = transceiver['lonDeg']
                    AfvClient(callsign, latitude, longitude, agl)


def get_vatsim_controllers():
    controllers = get_json_from_url(constants.VATSIM_ONLINE_URL).get(
        'controllers')
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
        VatsimController(vatsim_id, name, callsign,
                         frequency, facility,
                         rating, server, visual_range,
                         logon_time)


def is_point_in_polygon(point: tuple) -> bool:
    if point is None:
        point = [0, 0]
    return constants.AREA.contains_point(point)


def get_atc_positions() -> list:
    atc_positions = []
    directory = '{}/resources'.format(constants.ROOT_DIR)
    filepath = os.path.join(directory, 'vrc.pof')
    with open(filepath, 'r') as file:
        lines = file.readlines()

    adjoining_fir_lines = 1000
    for index, line in enumerate(lines):
        if line.__contains__('adjoining FIRs'):
            adjoining_fir_lines = index

    for index, line in enumerate(lines):
        if ';' not in line and line != '\n' and index < adjoining_fir_lines:
            position = line.split(":")
            name = position[0]
            callsign = "{}_{}".format(position[5], position[6])
            AtcPosition(name, callsign)
            atc_positions.append(callsign)

    return atc_positions


def average_run_calc(total_loop_time, total_runs) -> float:
    return round(total_loop_time / total_runs, 3)
