import os, sys, time
path = os.path.join(os.path.dirname(__file__), '../lib/')
sys.path.insert(0, path)

from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from .config import Config
from Gen import TalkService
from Gen.ttypes import *
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

class Poll(Config):

  client = None

  rev = 0

  def __init__(self, authToken):
    Config.__init__(self)
    self.transport = THttpClient.THttpClient(self.LINE_HOST_DOMAIN, None, self.LINE_API_QUERY_PATH_FIR)
    self.transport.path = self.LINE_AUTH_QUERY_PATH
    self.transport.setCustomHeaders({"X-Line-Application" : self.APP_NAME,"User-Agent" : self.USER_AGENT,"X-Line-Access": authToken})
    self.protocol = TCompactProtocol.TCompactProtocol(self.transport);
    self.client = TalkService.Client(self.protocol)
    self.rev = self.client.getLastOpRevision()
    self.transport.path = self.LINE_POLL_QUERY_PATH_FIR
    self.transport.open()

  def stream(self):
    #usleep = lambda x: time.sleep(x/1000000.0)
    while True:
      try:
        Ops = self.client.fetchOps(self.rev, 50, 0, 0)
      except EOFError:
        raise Exception("It might be wrong revision\n" + str(self.rev))

      for Op in Ops:
          # print Op.type
        if (Op.type != OpType.END_OF_OPERATION):
          self.rev = max(self.rev, Op.revision)
          return Op

      #usleep(sleep)
