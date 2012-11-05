# -*- coding: utf-8 -*-
import webapp2

from DataStore import DataStore
from suds.mem_cache import MemCache
from suds.client import Client
from settings import *
from messages import *
from gcm import GCM
import logging
from google.appengine.api import mail

logger = logging.getLogger(__name__)

class BaseApplicationHandler(webapp2.RequestHandler):
    """
        Classe Base, Responsável pelas Requisições ao Servidor
    """
    _dataStore = DataStore()

    def responseOk(self):
        self.responseMessage(status=200)        

    def notFound(self,message):
        self.responseMessage(404,message)

    def responseMessage(self,status,message=None):
        self.response.status_int = status
        self.response.headers['Content-Type'] = 'text/plain'
        if message :
            self.response.write(message)

class ApplicationHandler(BaseApplicationHandler):
    """
       Classe que cuida dos Registros dos dispositivos
    """
    def post(self):
        """
            Registra uma nova Chave
        """

        key = self.request.get('key')
        
        self._dataStore.register(key)
        
        self.responseOk()

    def delete(self):
        """
            Desregistra uma Chave Existente
        """

        key = self.request.get('key')
        try :
            self._dataStore.unregister(key)
            self.responseOk()
        except :
            self.notFound("Key '%s' is not registered" % key)
        

class FriendChecker(BaseApplicationHandler):
    
    """
        Classe que faz uma busca no WS por amigos online
    """
    def get(self):
        
        logger.debug("Check if something is registered first")

        devices = self._dataStore.list_registered_devices()
        
        if not devices :
            self.notFound(NO_DEVICE_REGISTERED)
            logger.debug(NO_DEVICE_REGISTERED)
            return
        
        logger.debug("GetOnlineFriends Service")

        client = Client(PSN_WSDL, cache=MemCache())
        
        friends = client.service.GetOnlineFriends()
        
        if any(friends) :

            gcm = GCM(self._dataStore.retrieve_api_key())
            
            for friend in friends[0] :
                
                f = { 'PsnId' : friend.PsnId,
                     'AvatarSmall' : friend.AvatarSmall,
                     'Playing' :friend.Playing 
                }
            
                response = gcm.json_request(registration_ids=devices, data=f)
                
                logger.debug("GCM Server Response : %s" % response)
                
                if 'errors' in response:
                    logger.error("GCM Server is complaining, check the response!")
                    self.responseMessage(500, "Sorry, Couldn't sync to the Mobile Device")
                    
                    """
                        Envia Email de Erro para Notificar o Mau funcionamento da API
                    """
                    mail.send_mail(sender="PlaystationNetworkPythonGCMServer Support <support@psnservergcm.appspot.com>",
                                   to="Thiago Pagonha <thi.pag@gmail.com>",
                                   subject="GCM Server is Complaining",
                                   body="""
                                   There was an error during request phrase to GCM Server, details are as follow:
                                   
                                   gcm.json_request(registration_ids=devices, data=f)
                                   
                                   where
                                   
                                   devices = %s
                                   data = %s
                                   
                                   which generated this server response:
                                   
                                   %s
                                   
                                   More details can be found at appengine.google.com
                                   """ % (devices,f,response))
                    
                    return
                
            self.responseOk()
        else :
            logger.debug(NO_FRIEND_ONLINE)        
            self.notFound(NO_FRIEND_ONLINE)    
  
application = webapp2.WSGIApplication([('/',ApplicationHandler),
                                       ('/whosonline',FriendChecker)]
                                      ,debug=True)
