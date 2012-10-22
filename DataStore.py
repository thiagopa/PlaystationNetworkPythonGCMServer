"""
    Guardar as informações de chaves da aplicação 
"""
from google.appengine.ext import db

class AbstractKey(db.Model):
    value = db.StringProperty()

class ApiKey(AbstractKey): pass
class MobileKey(AbstractKey): pass  

# k = ApiKey(key_name='access',browser='')
# k.put()

class DataStore :
    """
        Operações Para a Recuperação e Escrita das Chaves
    """
    @db.transactional
    def register(self,key):
        """
            Registra a chave específica
        """ 
        k = MobileKey(value=key)
        k.put()
        
    @db.transactional
    def unregister(self,key):
        """
            Desregistra a chave específica
        """ 
        k = MobileKey.all().filter("value =", key)
        k.delete()
        

    def retrieve_api_key(self) :
        api_key = db.Key.from_path('ApiKey', 'access')
        return db.get(api_key)

