# -*- coding: utf-8 -*-

import os
import psycopg2

DBS = ["longport"]

# --addons-path <directories>
addons_path = "/Users/eneldoserrata/PycharmProjects/marcos/odoo8/odoo/openerp/addons,/Users/eneldoserrata/PycharmProjects/marcos/odoo8/odoo/addons,/Users/eneldoserrata/PycharmProjects/marcos/odoo8/odoo8_community_modules,/Users/eneldoserrata/PycharmProjects/marcos/odoo8/cost_control,/Users/eneldoserrata/PycharmProjects/marcos/odoo8/marcos8_addons"
db_host = "127.0.0.1"
db_user = "odoo"
db_password = "1234"


for DB in DBS:
    conn = psycopg2.connect("dbname={} user={} password={}".format(DB, db_user, db_password))
    cur = conn.cursor()
    cur.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.procpid)
        FROM pg_stat_get_activity(NULL::integer)
        WHERE datid=(SELECT oid from pg_database where datname = '{}');

    """.format(DB))
    cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    os.system(
        "python odoo.py --addons-path {} --db_host = {} --db_user = {} --db_password {} -d {} -u all --max-cron-threads 0 "
        "--xmlrpc-port 4343 --stop-after-init".format(addons_path, db_host, db_user, db_password, DB))
