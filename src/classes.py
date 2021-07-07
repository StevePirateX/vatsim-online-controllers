class VatsimController:
    """This class defines all the VATSIM clients (pilots and controllers)"""
    vatsim_controllers = []

    def __init__(self, vatsim_id, name, callsign, frequency, facility,
                 rating, server, visual_range, logon_time):
        self.vatsim_id = vatsim_id
        self.name = name
        self.callsign = callsign
        self.frequency = frequency
        self.facility = facility
        self.rating = rating
        self.server = server
        self.visual_range = visual_range
        self.logon_time = logon_time

        VatsimController.vatsim_controllers.append(self)

    def get_position(self) -> tuple:
        """
        Queries the AFV Json file to return the first transceiver's position
        :return: tuple (`float`, `float`) -> (latitude, longitude)
        """
        position = AfvClient.get_callsign_position(self.callsign)
        return position


class AfvClient:
    """This contains all the clients on VATSIM, not just controllers"""
    afv_clients = []

    def __init__(self, callsign, latitude, longitude, agl_m):
        self.callsign = callsign
        self.latitude = latitude
        self.longitude = longitude
        self.agl_m = agl_m

        AfvClient.insert_all_clients(callsign, latitude, longitude, agl_m)

    @staticmethod
    def insert_all_clients(callsign, latitude, longitude, agl_m):
        client_details = (callsign, latitude, longitude, agl_m)
        AfvClient.afv_clients.append(client_details)

    @staticmethod
    def get_callsign_position(callsign: str) -> tuple:
        for client in AfvClient.afv_clients:
            if client[0] == callsign:
                return client[1], client[2]


class AtcPosition:
    atc_positions = []

    def __init__(self, callsign, name):
        self.callsign = callsign
        self.name = name

        AtcPosition.atc_positions.append(self)

    @staticmethod
    def get_atc_positions():
        return AtcPosition.atc_positions
