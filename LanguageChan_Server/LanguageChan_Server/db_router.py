class DBRouter:
    def __init__(self):
        self.app_to_db = {
            'users': 'users',
            'entities': 'entities',
            'lessons': 'lessons',
        }
    def db_for_read(self, model, **hints):
        return self.app_to_db.get(model._meta.app_label, 'default')
    def db_for_write(self, model, **hints):
        return self.app_to_db.get(model._meta.app_label, 'default')
    def allow_migrate(self, db_label, app_label, model_name=None, **hints):
        if app_label in self.app_to_db:
            return self.app_to_db[app_label] == db_label
        return db_label == 'default'
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == obj2._state.db:
            return True
        return None
