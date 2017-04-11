#!/usr/bin/python
"""
This script creates a timestamped database backup,
and cleans backups older than a set number of dates

"""    

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sqlite3
import shutil
import time
import os

DESCRIPTION = """
             Create a timestamped SQLite database backup, and
             clean backups older than a defined number of days
             """

# How old a file needs to be in order
# to be considered for being removed
NO_OF_DAYS = 3


def sqlite3_backup(dbfile, backupdir):
    """Create timestamped database copy"""
    if not os.path.isdir(backupdir):
        raise Exception("Backup directory does not exist: {}".format(backupdir))
    
    backup_file = os.path.join(backupdir, os.path.basename(dbfile) + time.strftime("-%Y%m%d-%H%M"))
    
    connection = sqlite3.connect(dbfile)
    cursor = connection.cursor()
    
    # Lock database before making a backup
    cursor.execute('begin immediate')
    # Make new backup file
    shutil.copyfile(dbfile, backup_file)
    print("\nCreating {}...".format(backup_file))
    # Unlock database
    connection.rollback()


def clean_data(backup_dir):
    """Delete files older than NO_OF_DAYS days"""
    print("\n------------------------------")
    print("Cleaning up old backups")
    for filename in os.listdir(backup_dir):
        backup_file = os.path.join(backup_dir, filename)
        if os.path.isfile(backup_file):
            if os.stat(backup_file).st_ctime < (time.time() - NO_OF_DAYS * 86400):
                os.remove(backup_file)
                print("Deleting {}...".format(backup_file))

if __name__ == "__main__":
    db_file = "/var/db/smarthome.db"
    backup_dir = "/var/backup"
    sqlite3_backup(db_file, backup_dir)
    clean_data(backup_dir)
    print("\nBackup has been successful.")