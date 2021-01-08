from time import sleep
import compose
import nginx
import zfs

def run(website_id):
    compose.uninstall(website_id)
    nginx.uninstall(website_id)

    time = 4
    print(f'Waiting {time} seconds before removing dataset to let it unmount')
    sleep(time)
    zfs.remove_website_dataset(website_id)
