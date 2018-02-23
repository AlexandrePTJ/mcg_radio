#coding: utf-8

from sqlite3 import dbapi2 as sqlite3

class DBAccess(object):

    def __init__(self, dbpath):
        super(DBAccess, self).__init__()
        self._dbpath = dbpath

    def _get_db(self):
        db = sqlite3.connect(self._dbpath)
        db.row_factory = sqlite3.Row
        return db

    def get_station_by_position(self, position):
        db = self._get_db()
        cur = db.execute("SELECT * FROM stations WHERE position=?", str(position))
        station = cur.fetchone()
        db.close()
        return station

    def get_station_by_id(self, id):
        db = self._get_db()
        cur = db.execute("SELECT * FROM stations WHERE id=?", str(id))
        station = cur.fetchone()
        db.close()
        return station

    def get_current_info(self):
        db = self._get_db()
        cur = db.execute("SELECT * FROM current_info")
        current_info = cur.fetchone()
        db.close()
        return current_info

    def clear_current_info(self):
        db = self._get_db()
        db.execute("DELETE FROM current_info")
        db.commit()
        db.close()

    def set_current_station(self, stationId):
        db = self._get_db()
        db.execute("INSERT INTO current_info (station_id) VALUES(?)", str(stationId))
        db.commit()
        db.close()

    def update_current_info(self, title, name):
        db = self._get_db()
        db.execute("UPDATE current_info SET title=?,name=?", (title, name))
        db.commit()
        db.close()
