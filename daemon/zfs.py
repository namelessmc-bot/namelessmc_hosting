import os

ZFS_ROOT = os.environ['ZFS_ROOT']

def create_website_dataset(website_id):
    dataset_name = f'{ZFS_ROOT}/{website_id}'
    print('Creating dataset ' + dataset_name)
    os.system(f"zfs create -o quota=500M {ZFS_ROOT}/{website_id}")


def remove_website_dataset(website_id):
    os.system(f"zfs rename {ZFS_ROOT}/{website_id} {ZFS_ROOT}/{website_id}_deleted")
