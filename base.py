

def class BaseDao(object):
    
    def query_one(self, id, field_list=None):
        raise NotImplementedError
        
    def query_many(self, id_list, field_list=None):
        raise NotImplementedError
    
    def remove_one(self, id):
        raise NotImplementedError
        
    def remove_many(self, id_list):
        raise NotImplementedError
        
    def update(self, obj):
        raise NotImplementedError
        
    def insert_one(self, obj):
        raise NotImplementedError
        
    def insert_many(self, obj_list):
        raise NotImplementedError
    
    def query(self, id_or_id_list, field_list=None):    
        if self._is_list(id_or_id_list):
            self.query_many(id_or_id_list, field_list)
        else:
            self.query_one(id_or_id_list, field_list)
        
    def remove(self, id_or_id_list):
        if self._is_list(id_or_id_list):
            self.remove_many(id_or_id_list)
        else:
            self.remove_one(id_or_id_list)
    
    def insert(self, obj_or_obj_list):
        if self._is_list(obj_or_obj_list):
            self.insert_many(obj_or_obj_list)
        else:
            self.insert_one(obj_or_obj_list)
        
    def _is_list(self, obj):
        return isinstance(obj, list)
