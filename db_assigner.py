from database import Database

class DBAssigner:
    dbs = {}
    
    def get_db(self, db_name):
        if db_name not in DBAssigner.dbs:
            DBAssigner.dbs[db_name] = Database(db_name)
        return DBAssigner.dbs[db_name]