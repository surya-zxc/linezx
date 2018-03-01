# -*- coding: utf-8 -*-
import os, sys
path = os.path.join(os.path.dirname(__file__), '../lib/')
sys.path.append(path)
import json, requests, rsa

from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from .config import Config
from Gen import TalkService
from Gen import AuthService
from Gen.ttypes import *
con = Config()
_session = requests.session()

def getJson(url, headers=None):
    if headers is None:
        return json.loads(_session.get(url).text)
    else:
        return json.loads(_session.get(url, headers=headers).text)

def defaultCallback(str):
    print(str)

def createTransport(path=None, update_headers=None, service=None):
    Headers = {
        'User-Agent': con.USER_AGENT,
        'X-Line-Application': con.APP_NAME,
        "x-lal": "ja-US_US",
    }
    Headers.update({"x-lpqs" : path})
    if(update_headers is not None):
        Headers.update(update_headers)
    transport = THttpClient.THttpClient(con.LINE_HOST_DOMAIN + path)
    transport.setCustomHeaders(Headers)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = service(protocol)
    return client

class LineCallback(object):

    def __init__(self, callback):
        self.callback = callback

    def QrUrl(self, url, showQr=True):
        self.callback(url)

    def default(self, str):
        self.callback(str)

class Talk(Config):
  client = None


  authToken = None
  cert = None

  def __init__(self):
    Config.__init__(self)
    self.transport = THttpClient.THttpClient(self.LINE_HOST_DOMAIN,None, self.LINE_API_QUERY_PATH_FIR)
    self.transport.setCustomHeaders({
      "X-Line-Application" : self.APP_NAME,"User-Agent" : self.APP_NAME})
    self.transport.open()
    self.protocol = TCompactProtocol.TCompactProtocol(self.transport);
    self.client = TalkService.Client(self.protocol)
    
  def ready(self,moji):
    r = moji.split(",")
    self.cert = r[0]
    self.authToken = r[1]
    self.transport.setCustomHeaders({
      "X-Line-Application" : self.LA,
      "User-Agent" : self.UA,
      "X-Line-Access" : r[1]
      })
    self.transport.path = self.LINE_API_QUERY_PATH_FIR

  def TokenLogin(self, authToken):
    self.transport.setCustomHeaders({"X-Line-Application" : self.APP_NAME,"User-Agent" : self.APP_NAME,"X-Line-Access" : authToken,})
    self.authToken = authToken
    self.transport.path = self.LINE_API_QUERY_PATH_FIR

  def qrLogin(self,keepLoggedIn=True, systemName=None):
        if systemName is None:
            systemName=self.SYSTEM_NAME
        client = createTransport(self.LINE_AUTH_QUERY_PATH, None, TalkService.Client)

        qr = client.getAuthQrcode(keepLoggedIn, systemName)
        uri = "line://au/q/" + qr.verifier
        clb = LineCallback(defaultCallback)
        clb.QrUrl(uri, 1)
        header = {
                'User-Agent': self.USER_AGENT,
                'X-Line-Application': self.APP_NAME,
                "x-lal" : "ja-US_US",
                "x-lpqs" : self.LINE_LOGIN_QUERY_PATH,
                'X-Line-Access': qr.verifier
        }
        getAccessKey = getJson(self.LINE_HOST_DOMAIN + self.LINE_CERTIFICATE_PATH, header)

        client = createTransport(self.LINE_LOGIN_QUERY_PATH, None, AuthService.Client)
        req = LoginRequest()
        req.type = 1
        req.verifier = qr.verifier
        req.e2eeVersion = 1
        res = client.loginZ(req)
        client = createTransport(self.LINE_API_QUERY_PATH_FIR, {'X-Line-Access':res.authToken}, TalkService.Client)
        self.TokenLogin(res.authToken)
        return res.authToken
    

  def __crypt(self, mail, passwd, RSA):
    message = (chr(len(RSA.sessionKey)) + RSA.sessionKey +
                   chr(len(mail)) + mail +
                   chr(len(passwd)) + passwd).encode('utf-8')

    pub_key = rsa.PublicKey(int(RSA.nvalue, 16), int(RSA.evalue, 16))
    crypto = rsa.encrypt(message, pub_key).encode('hex')

    return crypto
