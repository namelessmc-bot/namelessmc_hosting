import os
import compose
import zfs
import update_site
import sitedb

def run(website_id):
    compose.uninstall(website_id)
    dataset = f'/{zfs.ZFS_ROOT}/{website_id}'
    # print(f'rm -rf {dataset}/db')
    # os.system(f'rm -rf {dataset}/db')
    print(f'rm -rf {dataset}/web')
    os.system(f'rm -rf {dataset}/web')
    sitedb.reset(website_id)
    update_site.run(website_id)
