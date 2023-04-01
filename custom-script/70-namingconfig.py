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
def set_namingconfig(database, enable):
    if enable == "True":
        naming = 1
    else:
        naming = 0
    data = (0, 1, '{Movie Title} ({Release Year}) {Quality Full}', '{Movie Title} ({Release Year})', 0, naming)
    query = "INSERT INTO NamingConfig (MultiEpisodeStyle,ReplaceIllegalCharacters,StandardMovieFormat," \
            "MovieFolderFormat,ColonReplacementFormat,RenameMovies) VALUES(?, ?, ?, ?, ?, ?)"
    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query, data)
        connexion.commit()

        db.close()
        connexion.close()
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    else:
        return enable


def get_namingconfig(database):
    query = "SELECT RenameMovies FROM NamingConfig"

    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query)
        rows = db.fetchall()

        db.close()
        connexion.close()

        if not rows:
            raise ValueError
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    except ValueError:
        return ""
    else:
        if rows[0][0] == 1:
            return "True"
        else:
            return "False"


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
    NAMING = get_namingconfig(RADARR_DB)
    if NAMING is None:
        sys.exit(1)

    if NAMING == "":
        NAMING = set_namingconfig(RADARR_DB, RADARR_NAMING)
        if NAMING is None:
            sys.exit(1)

    if NAMING != RADARR_NAMING:
        NAMING = update_namingconfig(RADARR_DB, RADARR_NAMING)
        if NAMING is None:
            sys.exit(1)
