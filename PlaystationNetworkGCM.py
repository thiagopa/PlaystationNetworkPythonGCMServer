# -*- coding: utf-8 -*-
import webapp2

from DataStore import DataStore

class ApplicationHandler(webapp2.RequestHandler):
    
    """
        Classe Base, Responsável pelas Requisições ao Servidor
    """
    def responseOk(self):
        self.response.status_int = 200
        self.response.headers['Content-Type'] = 'text/plain'

    """
        Registra uma nova Chave
    """
    def post(self):
        key = self.request.get('key')
        
        DataStore().register(key)
        
        self.responseOk()

    """
        Desregistra uma Chave Existente
    """
    def delete(self):
        key = self.request.get('key')
        
        DataStore().unregister(key)
        
        self.responseOk()
  
application = webapp2.WSGIApplication([('/',ApplicationHandler)],debug=True)
