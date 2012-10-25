#-*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

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
    def register(self,key):
        """
            Registra a chave específica
        """ 
        k = MobileKey(value=key)
        k.put()
        logger.debug("Register Mobile Key = %s" % (key))
        
    def unregister(self,key):
        """
            Desregistra a chave específica
        """ 
        k = MobileKey.all().filter("value =", key).get()
        k.delete()
        logger.debug("Unregister Mobile Key = %s" % (key))

    def retrieve_api_key(self) :
	"""
            Recupera a chave de ativação para da api
	"""
        api_key = db.Key.from_path('ApiKey', 'access')
        return db.get(api_key)

    def list_registered_devices(self) :
	"""
            Busca por todos os dispositivos registrados
	"""
        devices = []
        for key in MobileKey.all() :
            devices.append(key.value)
        return devices

