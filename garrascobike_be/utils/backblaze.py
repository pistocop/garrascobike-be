import json
from os import makedirs
from os.path import basename
from os.path import exists
from os.path import join

from b2sdk.v2 import B2Api
from b2sdk.v2 import InMemoryAccountInfo
from loguru import logger


class BackblazeManager:
    def __init__(self,
                 app_key_id: str,
                 app_key: str,
                 realm_account: str = "production",
                 ):
        info = InMemoryAccountInfo()
        self.b2_api = B2Api(info)
        self.b2_api.authorize_account(realm_account, app_key_id, app_key)

    def download_file(self,
                      file_id: str,
                      out_path: str):
        bb_file = self.b2_api.download_file_by_id(file_id)
        bb_file.save_to(out_path)

    def download_folder(self,
                        bucket_name: str,
                        bucket_folder_path: str,
                        local_folder_path: str):
        bucket_files = []

        bucket = self.b2_api.get_bucket_by_name(bucket_name)
        for file_info, folder_name in bucket.ls(folder_to_list=bucket_folder_path, recursive=True):
            file_extended_name = file_info.file_name  # e.g.ml-models/20210625162104/.bzEmpty
            bucket_files.append(file_extended_name)
        logger.debug(f"'{len(bucket_files)}' files found on '{bucket_name}:{bucket_folder_path}' bucket")

        for file_extended_name in bucket_files:
            file_name = basename(file_extended_name)
            file_output_path = join(local_folder_path, file_name)
            file_mng = bucket.download_file_by_name(file_extended_name)
            file_mng.save_to(file_output_path)
            logger.debug(f"File '{bucket_name}:{file_extended_name}' stored at '{local_folder_path}'")


def download_garrascobike_model(local_path: str,
                                model_info_path: str,
                                app_key_id: str,
                                app_key: str,
                                ) -> str:
    # Load remote ML info
    model_info = json.loads(open(model_info_path, 'r').read())

    # Create support info
    remote_model_path = model_info["model_path"]
    remote_bucket_name = model_info["bucket"]
    model_id = basename(remote_model_path)
    local_model_path = join(local_path, model_id)

    # Preliminary checks
    if exists(local_model_path):
        logger.info(f"ML model loading skipped: '{local_model_path}' already exist")
        return local_model_path

    if not app_key or not app_key_id:
        msg = "app_key or app_key_id not provided, cannot connect to backblaze"
        logger.error(msg)
        raise EnvironmentError(msg)

    # Download the model
    logger.info(f"ML model '{remote_model_path}' downloading...")
    makedirs(local_model_path)
    bb_mng = BackblazeManager(app_key_id, app_key)
    bb_mng.download_folder(remote_bucket_name, remote_model_path, local_model_path)
    logger.info(f"ML model '{remote_model_path}' downloaded!")

    return local_model_path
