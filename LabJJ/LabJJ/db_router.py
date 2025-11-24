class DBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.db_table == "posicoes":
            return "DBJJPos"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table == "posicoes":
            return "DBJJPos"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.db_table == "posicoes" or obj2._meta.db_table == "posicoes":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # ensure the posicoes app migrates to the DBJJPos database
        if app_label == "posicoes":
            return db == "DBJJPos"
        return None
