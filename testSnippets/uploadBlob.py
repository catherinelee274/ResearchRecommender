#upload to microsoft blob

import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess


ACCOUNT_NAME = ''
ACCOUNT_KEY = ''
container_name ='papers'

block_blob_service = BlockBlobService(
    account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

#block_blob_service.create_container(CONTAINER_NAME)

#block_blob_service.set_container_acl(CONTAINER_NAME, public_access=PublicAccess.Container)

# List the blobs in the container
#print("\nList blobs in the container")
#generator = block_blob_service.list_blobs(container_name)
#for blob in generator:
#    print("\t Blob name: " + blob.name)

#in prog

#block_blob_service.create_blob_from_path(container_name, fileName, fileName) #replace full_path_to_file as a get request?
