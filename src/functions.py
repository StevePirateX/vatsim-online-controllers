import constants
import os
import configparser
import random

def import_config(filename: str) -> None:
    """
    Imports the .ini file specified and sets the constants.
    :param filename: String of the filename of the csv. The file
        is to be located in the same folder as the python file.
    :return: None
    """
    config_file_path = os.path.join(constants.ROOT_DIR, filename)
    if not os.path.exists(filename):
        print("'{}' not found. Creating default".format(filename))
        config_file = open(config_file_path, 'w')

        config = configparser.ConfigParser()
        config.add_section('General')
        config.set('General', 'vatsim_online_data_url',
                   constants.VATSIM_ONLINE_URL)

        config.add_section('Audio For VATSIM')
        config.set('Audio For VATSIM', 'api_server', constants.AFV_API_SERVER)
        config.set('Audio For VATSIM', 'api_server_backup',
                   constants.AFV_API_SERVER_BACKUP)
        config.set('Audio For VATSIM', 'api_version',
                   constants.AFV_API_VERSION)
        config.set('Audio For VATSIM', 'api_post_url',
                   constants.AFV_API_POST_URL)

        config.write(config_file)
        config_file.close()

    with open(config_file_path, 'r') as file:
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_file(file)

    if config.has_option('General', 'chores_to_generate'):
        constants.VATSIM_ONLINE_URL = config.get('General',
                                                 'vatsim_online_data_url')
        constants.AFV_API_SERVER = config.get('Audio For VATSIM', 'api_server')
        constants.AFV_API_SERVER_BACKUP = config.get('Audio For VATSIM',
                                                     'api_server_backup')
        constants.AFV_API_VERSION = config.get('Audio For VATSIM',
                                               'api_version')
        constants.AFV_API_POST_URL = config.get('Audio For VATSIM',
                                                'api_post_url')


def get_afv_url() -> str:
    server_selection = random.randint(1, 2)

    if server_selection == 1:
        domain = constants.AFV_API_SERVER
    elif server_selection == 2:
        domain = constants.AFV_API_SERVER_BACKUP
    else:
        domain = constants.AFV_API_SERVER
    version = constants.AFV_API_VERSION
    post_url = constants.AFV_API_POST_URL

    request_url = f"{domain}/v{version}/{post_url}"
    return request_url
