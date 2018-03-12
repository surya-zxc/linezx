# -*- coding: utf-8 -*-
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from .config import Config
from tcr import CallService
from tcr.ttypes import *

class Call(Config):
    client = None

    def __init__(self, authToken):
       Config.__init__(self)
       self.transport = THttpClient.THttpClient(self.LINE_HOST_DOMAIN, None, self.LINE_API_QUERY_PATH_FIR)
       self.transport.path = self.LINE_AUTH_QUERY_PATH
       self.transport.setCustomHeaders({"X-Line-Application" : self.APP_NAME,"User-Agent" : self.USER_AGENT,"X-Line-Access": authToken})
       self.protocol = TCompactProtocol.TCompactProtocol(self.transport);
       self.client = CallService.Client(self.protocol)
       self.transport.path = self.LINE_CALL_QUERY_PATH
       self.transport.open()


    def acquireCallRoute(self,to):
        return self.client.acquireCallRoute(to)

    def acquireGroupCallRoute(self, groupId, mediaType=MediaType.AUDIO):
        return self.client.acquireGroupCallRoute(groupId, mediaType)

    def getGroupCall(self, ChatMid):
        return self.client.getGroupCall(ChatMid)

    def inviteIntoGroupCall(self, chatId, contactIds=[], mediaType=MediaType.AUDIO):
        return self.client.inviteIntoGroupCall(chatId, contactIds, mediaType)