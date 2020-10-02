from os import environ as env
import os
# pyzfs is python2 only apparently :(
# import libzfs_core
# from libzfs_core.exceptions import FilesystemExists

ZFS_ROOT = env['ZFS_ROOT']

ZFS_DATASET_OPTIONS = {
    'quota', '5G'
}

def create_website_dataset(website_id):
    dataset_name = f'{ZFS_ROOT}/{website_id}'
    print('Creating dataset ' + dataset_name)
    os.system(f"zfs create -o quota=5G {ZFS_ROOT}/{website_id}")
    # try:
        # libzfs_core.lzc_create(dataset_name, ds_type='zfs', props=ZFS_DATASET_OPTIONS)
    # except FilesystemExists:
        # print('Dataset already exists')


def remove_website_dataset(website_id):
    os.system(f"zfs rename {ZFS_ROOT}/{website_id} {ZFS_ROOT}/{website_id}_deleted")
