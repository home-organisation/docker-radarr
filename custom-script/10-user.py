#!/usr/bin/python3
import sys
import os
import sqlite3
import logging
import hashlib
import uuid
import base64

###########################################################
# SET STATIC CONFIG
###########################################################
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
RADARR_DB = '/config/radarr.db'


###########################################################
# DEFINE FUNCTION
###########################################################
def set_credential(database, username, password):
    # Create user in database
    identifier = str(uuid.uuid4())
    salt = base64.b64encode(os.urandom(16))
    hashpassword = get_hashed_password(password, salt)

    data = (identifier, username, hashpassword, salt, 10000)
    query = "INSERT INTO Users (Identifier,Username,Password,Salt,Iterations) VALUES(?, ?, ?, ?, ?)"
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
        return password


def update_credential(database, username, password):
    # Update user password in database
    salt = base64.b64encode(os.urandom(16))
    hashpassword = get_hashed_password(password, salt)

    data = (hashpassword, salt, username)
    query = "UPDATE Users SET Password = ?, Salt = ? WHERE Username = ?"

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
        return password


def verify_hashed_password(database, username, password):
    data = (username,)
    query = "SELECT Password,Salt FROM Users WHERE Username = ?"

    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        db.execute(query, data)
        rows = db.fetchall()

        db.close()
        connexion.close()
        if not rows:
            raise ValueError
    except sqlite3.Error as er:
        logging.error('SQLite error: %s' % (' '.join(er.args)))
        return None
    except ValueError:
        return "empty"

    salt = rows[0][1]
    hashpassword = rows[0][0]
    if get_hashed_password(password, salt) == hashpassword:
        return "true"
    else:
        return "false"


def get_hashed_password(password, salt):
    encryptsalt = base64.b64decode(salt)
    encryptpassword = base64.b64encode(hashlib.pbkdf2_hmac('sha512',password.encode('utf-8'), encryptsalt, 10000, 32))

    return encryptpassword


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    RADARR_USER = os.environ.get('RADARR_USER') or "admin"
    RADARR_PASSWORD = os.environ.get('RADARR_PASSWORD')
    if RADARR_USER is None or RADARR_PASSWORD is None:
        logging.warning("RADARR_USER or RADARR_PASSWORD with no value, nothing to do")
        sys.exit(0)

    logging.info("Set Credential to application for user %s ..." % RADARR_USER)

    PASSWORD = verify_hashed_password(RADARR_DB, RADARR_USER, RADARR_PASSWORD)
    if PASSWORD is None:
        sys.exit(1)
    elif PASSWORD == "empty":
        logging.info("User %s doesnt exist, create ..." % RADARR_USER)
        PASSWORD = set_credential(RADARR_DB, RADARR_USER, RADARR_PASSWORD)
        if PASSWORD is None:
            sys.exit(1)
    elif PASSWORD == "false":
        logging.info("User %s already exist but with an other password, update ..." % RADARR_USER)
        PASSWORD = update_credential(RADARR_DB, RADARR_USER, RADARR_PASSWORD)
        if PASSWORD is None:
            sys.exit(1)
    elif PASSWORD == "true":
        logging.info("User %s already exist with this password, nothing to do ..." % RADARR_USER)
