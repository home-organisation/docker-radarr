#!/usr/bin/python3
import sys
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
def set_custom_format(database):
    # Create Custom Formats HEVC, AVC and VOSTFR
    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        spec = '[{ "type": "ReleaseTitleSpecification", "body": { "order": 1, "implementationName": "Release Title", "infoLink": "https://wiki.servarr.com/radarr/settings#custom-formats-2", "value": "(((x|h)\\\\.?265)|(HEVC))", "name": "x265", "negate": false, "required": true }}]'
        data = ("HEVC", spec, 0)
        query = "INSERT INTO CustomFormats (Name,Specifications,IncludeCustomFormatWhenRenaming) VALUES(?, ?, ?)"

        db.execute(query, data)
        connexion.commit()
    except sqlite3.Error as er:
        if er.args == ('UNIQUE constraint failed: CustomFormats.Name',):
            logging.info("Custom Formats HEVC already exist, nothing to do")
        else:
            logging.error('SQLite error: %s' % (' '.join(er.args)))
            return None

    try:
        spec = '[{ "type": "ReleaseTitleSpecification", "body": { "order": 1, "implementationName": "Release Title", "infoLink": "https://wiki.servarr.com/radarr/settings#custom-formats-2", "value": "(x|h)\\\\.?264", "name": "x264", "negate": false, "required": true}}]'
        data = ("AVC", spec, 0)
        query = "INSERT INTO CustomFormats (Name,Specifications,IncludeCustomFormatWhenRenaming) VALUES(?, ?, ?)"

        db.execute(query, data)
        connexion.commit()
    except sqlite3.Error as er:
        if er.args == ('UNIQUE constraint failed: CustomFormats.Name',):
            logging.info("Custom Formats AVC already exist, nothing to do")
        else:
            logging.error('SQLite error: %s' % (' '.join(er.args)))
            return None

    try:
        spec = '[{ "type": "ReleaseTitleSpecification", "body": { "order": 1, "implementationName": "Release Title", "infoLink": "https://wiki.servarr.com/radarr/settings#custom-formats-2", "value": "\\\\b(VOST.*?FR(E|A)?)\\\\b", "name": "VOSTFR", "negate": false, "required": true}}, { "type": "ReleaseTitleSpecification", "body": { "order": 1, "implementationName": "Release Title", "infoLink": "https://wiki.servarr.com/radarr/settings#custom-formats-2", "value": "\\\\b(SUBFR(A|ENCH)?)\\\\b", "name": "SUBFRENCH", "negate": false, "required": true}}]'
        data = ("VOSTFR", spec, 0)
        query = "INSERT INTO CustomFormats (Name,Specifications,IncludeCustomFormatWhenRenaming) VALUES(?, ?, ?)"

        db.execute(query, data)
        connexion.commit()
    except sqlite3.Error as er:
        if er.args == ('UNIQUE constraint failed: CustomFormats.Name',):
            logging.info("Custom Formats VOSTFR already exist, nothing to do")
        else:
            logging.error('SQLite error: %s' % (' '.join(er.args)))
            return None

    db.close()
    connexion.close()
    return 0


def set_custom_profiles(database):
    # Create Custom Profiles HD-1080p-FR and HD-1080p-VO
    connexion = sqlite3.connect(database)
    db = connexion.cursor()

    try:
        items = '[{ "quality": 9, "items": [], "allowed": true }, { "id": 1002, "name": "WEB 1080p", "items": [{ "quality": 3, "items": [], "allowed": true }, { "quality": 15, "items": [], "allowed": true }], "allowed": true}, { "quality": 7, "items": [], "allowed": true }, { "quality": 30, "items": [], "allowed": true }]'
        formatitems = '[{ "format": 1, "score": 1 }, { "format": 2, "score": 1 }, { "format": 3, "score": 0 }]'
        data = ("HD-1080p-FR", 30, items, 2, formatitems, 0, 1, 0)
        query = "INSERT INTO QualityProfiles (Name,Cutoff,Items,Language,FormatItems,UpgradeAllowed,MinFormatScore,CutoffFormatScore) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

        db.execute(query, data)
        connexion.commit()
    except sqlite3.Error as er:
        if er.args == ('UNIQUE constraint failed: QualityProfiles.Name',):
            logging.info("Custom Profiles HD-1080p-FR already exist, nothing to do")
        else:
            logging.error('SQLite error: %s' % (' '.join(er.args)))
            return None

    try:
        items = '[{ "quality": 9, "items": [], "allowed": true }, { "id": 1002, "name": "WEB 1080p", "items": [{ "quality": 3, "items": [], "allowed": true }, { "quality": 15, "items": [], "allowed": true }], "allowed": true}, { "quality": 7, "items": [], "allowed": true }, { "quality": 30, "items": [], "allowed": true }]'
        formatitems = '[{ "format": 1, "score": 1 }, { "format": 2, "score": 1 }, { "format": 3, "score": 1 }]'
        data = ("HD-1080p-VO", 30, items, -2, formatitems, 0, 2, 0)
        query = "INSERT INTO QualityProfiles (Name,Cutoff,Items,Language,FormatItems,UpgradeAllowed,MinFormatScore,CutoffFormatScore) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

        db.execute(query, data)
        connexion.commit()
    except sqlite3.Error as er:
        if er.args == ('UNIQUE constraint failed: QualityProfiles.Name',):
            logging.info("Custom Profiles HD-1080p-VO already exist, nothing to do")
        else:
            logging.error('SQLite error: %s' % (' '.join(er.args)))
            return None

    db.close()
    connexion.close()
    return 0


###########################################################
# INIT CONFIG
###########################################################
if __name__ == '__main__':
    logging.info("Set Custom Formats HEVC, AVC and VOSTFR ...")
    FORMAT = set_custom_format(RADARR_DB)
    if FORMAT is None:
        sys.exit(1)

    logging.info("Set Custom Profiles HD-1080p-FR and HD-1080p-VO ...")
    PROFILES = set_custom_profiles(RADARR_DB)
    if PROFILES is None:
        sys.exit(1)
