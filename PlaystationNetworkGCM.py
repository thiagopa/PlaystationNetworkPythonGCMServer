# -*- coding: utf-8 -*-
import webapp2

from DataStore import DataStore
from suds.mem_cache import MemCache
from suds.client import Client
from settings import *
from gcm import GCM
import json
import logging

logger = logging.getLogger(__name__)

class ApplicationHandler(webapp2.RequestHandler):
    
    """
        Classe Base, Responsável pelas Requisições ao Servidor
    """
    def responseOk(self):
        self.response.status_int = 200
        self.response.headers['Content-Type'] = 'text/plain'

    def post(self):
        """
            Registra uma nova Chave
        """

        key = self.request.get('key')
        
        DataStore().register(key)
        
        self.responseOk()

    def delete(self):
        """
            Desregistra uma Chave Existente
        """

        key = self.request.get('key')
        
        DataStore().unregister(key)
        
        self.responseOk()

class FriendChecker(webapp2.RequestHandler):
    """
        Classe que faz uma busca no WS por amigos online
    """
    
    API_KEY = DataStore().retrieve_api_key()
    
    def get(self):
        
        gcm = GCM(self.API_KEY)
        
        client = Client(PSN_WSDL, cache=MemCache())
        
        friends = client.service.GetOnlineFriends()
        
        data = []
        
        for friend in friends[0] :
            f = { 'PsnId' : friend.PsnId,
                 'AvatarSmall' : friend.AvatarSmall,
                 'Playing' :friend.Playing 
            }
            
            data.append(f)
        
        logger.debug(json.dumps(data))
            
        reg_ids = ['12', '34', '69']
        response = gcm.json_request(registration_ids=reg_ids, data=json.dumps(data))
        
        logger.debug(response)
            
        self.responseOk()
            

  
application = webapp2.WSGIApplication([('/',ApplicationHandler),
                                       ('/whosonline',FriendChecker)]
                                      ,debug=True)
