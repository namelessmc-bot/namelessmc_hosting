import os

ZFS_ROOT = os.environ['ZFS_ROOT']

ZFS_DATASET_OPTIONS = {
    'quota', '1G'
}

def create_website_dataset(website_id):
    dataset_name = f'{ZFS_ROOT}/{website_id}'
    print('Creating dataset ' + dataset_name)
    os.system(f"zfs create -o quota=5G {ZFS_ROOT}/{website_id}")


def remove_website_dataset(website_id):
    os.system(f"zfs rename {ZFS_ROOT}/{website_id} {ZFS_ROOT}/{website_id}_deleted")
