import compose
import nginx
import zfs

def run(website_id):
    compose.uninstall(website_id)
    nginx.uninstall(website_id)
    zfs.remove_website_dataset(website_id)
