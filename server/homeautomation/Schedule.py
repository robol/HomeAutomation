#
# -*- coding: utf-8 -*-
#
# Author: Leonardo Robol <leo@robol.it>

import os, Utils, json

class Schedule():
    """Schedule for the irrigation. 

    Each entry of the schedule is composed by a client, and a daily
    frequency of irrigations. The latter has to be specified as a sequence
    of times of the day when the irrigation should take place, 
    toghether with their length. 

    This is representeted by an IrrigationAction object. 
    """

    def __init__(self, db_path = None):
        """Create a new  Schedule. If db_path is set to None, 
        or not specified, a default DB is opened. """

        if db_path is None:
            # Check for a safe path to open the database
            db_path = self.__detect_safe_db()

        # self.__db is a list of entries of the form
        # { 'client': address, 'time': time, 'length': length }
        # that can be used to construct an IrrigationAction to be performed at a
        # a certain time. 
        self.__db = self.__open_db(db_path)

    def __open_db(self, db_path):
        self.__db_path = db_path
        if db_path is not None:
            with open(db_path) as h:
                return json.load(h)
        else:
            return []

    def __detect_safe_db(self):
        tentative_path = os.path.expanduser('~/.config/wireless-irrigation')
        if not os.path.exists(tentative_path):
            try:
                os.makedirs(tentative_path)
            except (Exception e):
                # If we get here it is not possible to create the default
                # directory, therefore we just keep the database in memory
                Utils.Logger.logDebug(
                    'Cannot create a new DB, keeping it in memory')
                tentative_path = None

        # If we managed to get a valid DB, return the path to the DB file. 
        if tentative_path is not None:
            tentative_path = os.path.join(tentative_path,
                                          'irrigation.json')
        return tentative_path

    def save(self):
        if self.__db_path is not None:
            with open(self.__db_path, 'w') as h:
                json.dump(self.__db, h)
