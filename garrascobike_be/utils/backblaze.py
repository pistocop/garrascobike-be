from os.path import basename
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
