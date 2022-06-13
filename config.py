import os
import pathlib
import configparser

__file_path = os.path.abspath(__file__)
__dir_path = os.path.dirname(__file_path)

PROJ_LOC=pathlib.Path(__dir_path)
AVRO_SCHEMA_LOC=os.path.join(PROJ_LOC, "avro_modules")

if int(os.environ.get("INGESTION_PROD", '0')) != 1:
    print("in the dev environment")
    print("environment variables: {}".format(list(os.environ.keys())))

    __app_config = configparser.ConfigParser()
    __app_config.read(os.path.join(PROJ_LOC,'config.ini'))

    # IDENTITY_SERVER_SETTINGS = __app_config['IDENTITY_SERVER']
    DB_CONFIG = __app_config["CREDENTIALS_DATABASE"]

else:
    print("in the prod environment")
    try:

        IDENTITY_SERVER_SETTINGS = {
            'HOST_URL': os.environ.get('IDENTITY_SERVER_HOST', "0.0.0.0"),
            'HOST_PORT': os.environ.get('IDENTITY_SERVER_PORT', 5002)
        }
        DB_CONFIG = {
            'USERNAME': os.environ.get('CREDENTIALS_DB_USER'),
            'PASSWORD': os.environ.get('CREDENTIALS_DB_PASSWORD'),
            'HOST': os.environ.get('CREDENTIALS_DB_HOST'),
            'NAME': os.environ.get('CREDENTIALS_DB_NAME'),
        }

    except KeyError as e:
        print("failed to create configs for the application")
        print("missing configuration {} from environment variables".format(e))
        raise e