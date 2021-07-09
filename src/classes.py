from datetime import datetime


class VatsimController:
    """This class defines all the VATSIM clients (pilots and controllers)"""
    vatsim_atc = []
    vatsim_atc_old = []
    max_name_length = 0
    max_callsign_length = 0

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
        self.logon_time_iso = datetime.fromisoformat(self.logon_time[:19])

        if len(self.name) > VatsimController.max_name_length:
            VatsimController.max_name_length = len(self.name)

        if len(self.callsign) > VatsimController.max_callsign_length:
            VatsimController.max_callsign_length = len(self.callsign)

        is_callsign_taken = False
        for controller in VatsimController.vatsim_atc:
            if callsign == controller.callsign:
                is_callsign_taken = True

        if not is_callsign_taken:
            VatsimController.vatsim_atc.append(self)

    def get_position(self) -> tuple:
        """
        Queries the AFV Json file to return the first transceiver's position
        :return: tuple (`float`, `float`) -> (latitude, longitude)
        """
        position = AfvClient.get_callsign_position(self.callsign)
        return position

    def get_session_time(self):
        current_time = datetime.utcnow()
        session_start = self.logon_time_iso
        difference = current_time - session_start
        minutes_in_day = 24 * 60
        div_mod = divmod(
            difference.days * minutes_in_day + difference.seconds // 60, 60)
        return div_mod

    @staticmethod
    def copy_controllers():
        VatsimController.vatsim_atc_old = VatsimController.vatsim_atc.copy()

    @staticmethod
    def clean_controllers():
        for old_controller in VatsimController.vatsim_atc_old:
            is_callsign_still_active = False
            for index, controller in enumerate(
                    VatsimController.vatsim_atc):
                if old_controller.callsign == controller.callsign:
                    #                 Still connected
                    is_callsign_still_active = True
                    break
            if not is_callsign_still_active:
                VatsimController.vatsim_atc.remove(old_controller)
        VatsimController.vatsim_atc.clear()


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
        """Returns the lat, long of the controller"""
        for client in AfvClient.afv_clients:
            afv_callsign = client[0]
            afv_latitude = client[1]
            afv_longitude = client[2]
            if afv_callsign == callsign:
                return afv_latitude, afv_longitude


class AtcPosition:
    atc_positions = []

    def __init__(self, callsign, name):
        self.callsign = callsign
        self.name = name

        AtcPosition.atc_positions.append(self)

    @staticmethod
    def get_atc_positions():
        return AtcPosition.atc_positions
