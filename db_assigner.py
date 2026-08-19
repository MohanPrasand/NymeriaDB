from database import Database

class DBAssigner:
    dbs = {}
    users = {}
    
    def get_db(self, db_name):
        if db_name not in DBAssigner.dbs:
            DBAssigner.dbs[db_name] = Database(db_name)
            DBAssigner.users[db_name] = DBAssigner.users.get(db_name, 0) + 1
        return DBAssigner.dbs[db_name]
    
    def close_db(self, db_name):
        if db_name in DBAssigner.dbs:
            if DBAssigner.users[db_name] == 1:
                DBAssigner.dbs[db_name].close()
                del DBAssigner.dbs[db_name]
                del DBAssigner.users[db_name]
            else: 
                DBAssigner.users[db_name] -= 1