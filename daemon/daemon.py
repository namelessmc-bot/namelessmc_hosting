from time import sleep
# import libzfs_core
import db

import create_site
import update_site
import delete_site

print("Daemon started")

def daemon():
    while True:
        conn = db.open_db()
        cur = conn.cursor()
        cur.execute("SELECT id,type,content FROM jobs WHERE done = FALSE ORDER BY priority DESC LIMIT 1")
        job = cur.fetchone()
        if job:
            print(f"Job: {job}")
            (job_id, job_type, job_content) = job
            if job_type == 0:
                site_id = int(job_content)
                create_site.run(site_id)
            elif job_type == 1:
                site_id = int(job_content)
                update_site.run(site_id)
            elif job_type == 4:
                site_id = int(job_content)
                delete_site.run(site_id)
            else:
                print(f"Unknown job type {job_type}")
                # do not set job to done
                cur.close()
                conn.close()
                sleep(5)
                continue

            cur.execute("UPDATE jobs SET done = TRUE WHERE id=%s", (job_id,))
            conn.commit()
            print("Done")

        cur.close()
        conn.close()
        sleep(5)

daemon()
