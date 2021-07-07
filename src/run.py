import functions as f

if __name__ == "__main__":
    f.import_config("config.ini")
    afv_api = f.get_afv_url()
    print(afv_api)

    afv_data = f.get_json_from_url(afv_api)
    f.add_controller_coordinates(afv_data)