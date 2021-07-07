from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

VATSIM_ONLINE_URL = "https://data.vatsim.net/v3/vatsim-data.json"

AFV_API_SERVER = "https://voice1.vatsim.uk/api"
AFV_API_SERVER_BACKUP = "https://voice2.vatsim.uk/api"
AFV_API_VERSION = "1"
AFV_API_POST_URL = "network/online/callsigns"

CONTROLLER_SUFFIXES = {"DEL", "GND", "APP", "DEP", "CTR", "FSS"}

