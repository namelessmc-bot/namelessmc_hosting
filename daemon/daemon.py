from time import sleep
import db
import ftp
import create_site
import update_site
import delete_site
import reset_site
import certs
import compose


print("Daemon started")


def daemon():
    # ftp.recreate()

    while True:
        conn = db.open_db()
        cur = conn.cursor()
        cur.execute("SELECT id,type,content,priority FROM jobs WHERE done = FALSE ORDER BY priority DESC LIMIT 1")
        job = cur.fetchone()
        if job:
            (job_id, job_type, job_content, job_priority) = job
            print('Job', 'job_id', job_id, 'job_type', job_type, 'job_content', job_content, 'job_priority', job_priority)
            cur.execute("UPDATE jobs SET running = TRUE WHERE id=%s", (job_id,))
            if job_type == 0:
                site_id = int(job_content)
                create_site.run(site_id)
            elif job_type == 1:
                site_id = int(job_content)
                update_site.run(site_id)
            elif job_type == 2:
                site_id = int(job_content)
                reset_site.run(site_id)
            elif job_type == 3:
                site_id = int(job_content)
                certs.renew_cert(site_id)
            elif job_type == 4:
                pos = job_content.find('_')
                site_id = int(job_content[:pos])
                _domain = job_content[pos+1:]
                delete_site.run(site_id)
            elif job_type == 5:
                site_id = int(job_content)
                compose.start(site_id)
            else:
                print(f"Unknown job type {job_type}")
                cur.execute("UPDATE jobs SET running = FALSE WHERE id=%s", (job_id,))
                conn.commit()
                cur.close()
                conn.close()
                sleep(5)
                continue

            cur.execute("UPDATE jobs SET done = TRUE, running = FALSE WHERE id=%s", (job_id,))
            conn.commit()
            print("Done")

        cur.close()
        conn.close()

        if job:
            if job_type == 5:
                sleep(.3)
            else:
                sleep(1)
        else:
            sleep(3)

daemon()
