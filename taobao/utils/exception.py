'''
Created on Aug 29, 2013

@author: root
'''


class Error(StandardError):
    
    code = None
    title = None
    message_format = None
    
    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            message = self.message_format
        
        super(Error, self).__init__(message)
    
    def _build_message(self, message, **kwargs):
        if not message:
            message = self.message_format % kwargs
        return message
    
class ValidateError(Error):
    
    message_format = "where validate %(key)s, error occur."
    code = 400
    title = "Bad revoke"

class AccessError(Error):
    message_format = "When access ' %(url)s', error occur."
    code = 400
    title = "Access Error"
    
class LoginError(ValidateError):
    message_format = "When login, error occur." 
    title = "Login Error"   