from pathlib import Path
import matplotlib.path as mplpath

ROOT_DIR = Path(__file__).parent.parent

CONFIG_FILENAME = "config.ini"

VATSIM_ONLINE_URL = "https://data.vatsim.net/v3/vatsim-data.json"

AFV_API_SERVER = "https://voice1.vatsim.uk/api"
AFV_API_SERVER_BACKUP = "https://voice2.vatsim.uk/api"
AFV_API_VERSION = "1"
AFV_API_POST_URL = "network/online/callsigns"

CONTROLLER_SUFFIXES = {"DEL", "GND", "TWR", "APP", "DEP", "CTR", "FSS"}

POLYGON = [[-49.38, 151.35], [-35.54, 100.0], [-16.39, 110.25],
           [-10.98, 126.96], [-9.84, 145.12], [-27.47, 162.06]]
# noinspection PyTypeChecker
AREA = mplpath.Path(POLYGON, closed=True)
