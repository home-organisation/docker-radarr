#!/usr/bin/python3
import sys
import os
import sqlite3
import logging

###########################################################
# SET STATIC CONFIG
###########################################################
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
RADARR_DB = '/config/radarr.db'


###########################################################
# DEFINE FUNCTION
###########################################################
def update_namingconfig(database, enable):
    if enable == "True":
        query = "UPDATE NamingConfig SET RenameMovies = 1"
    else:
        query = "UPDATE NamingConfig SET RenameMovies = 0"

    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query)
        connexion.commit()

        db.close()
        connexion.close()
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    else:
        return enable


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    RADARR_NAMING = os.environ.get('RADARR_NAMING')
    if RADARR_NAMING is None or RADARR_NAMING not in ["True", "False"]:
        logging.warning("RADARR_NAMING <%s> is empty or has unaccepted value (True or False), "
                        "nothing to do" % RADARR_NAMING)
        sys.exit(0)

    logging.info("Set Naming Config to application with value %s ..." % RADARR_NAMING)
    NAMING = update_namingconfig(RADARR_DB, RADARR_NAMING)
    if NAMING is None:
        sys.exit(1)
