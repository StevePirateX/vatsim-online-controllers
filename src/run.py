import functions as f
import constants as c

f.import_config("config.ini")
print(c.VATSIM_ONLINE_URL)
afv_api = f.get_afv_url()
print(afv_api)