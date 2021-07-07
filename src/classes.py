class VatsimController:
    """This class defines all the VATSIM clients (pilots and controllers)"""

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

    def get_position(self) -> list[2]:
        """
        Queries the AFV Json file to return the first transceiver's position
        :return: list (`float`, `float`) -> (latitude, longitude)
        """
        pass
