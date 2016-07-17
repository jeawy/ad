# -*- coding: utf8 -*-
# 
import pdb
DB_USER  =  'web'
USER_APP =   ('administration', 
            'auth', 
            'admin',
            'contenttypes',
            'sessions',
            'messages',
            'staticfiles',  
            'center',
            'myjiwei',
    )

class WebSiteRouter(object):
    'Route to database'
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to write USER_APP models go to ad database.
        """  
        if model._meta.app_label in USER_APP:
            return DB_USER
         
        return False
    
    
    def db_for_write(self, model, **hints):
        """
        Attempts to write USER_APP models go to DB_USER.
        """ 
        if model._meta.app_label in  USER_APP:
            return DB_USER
        
        return False
            
        
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the USER_APP app is involved.
        """  
        if obj1._meta.app_label in  USER_APP or \
           obj2._meta.app_label in  USER_APP:
               return DB_USER
        return False
        
    def allow_migrate(self, db, app_label, model_name = None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """ 
        
        if app_label in USER_APP: 
            return db == DB_USER
        
        return None
        
        