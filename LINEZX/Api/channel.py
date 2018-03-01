# -*- coding: utf-8 -*-
import os, sys, json
path = os.path.join(os.path.dirname(__file__), '../lib/')
sys.path.insert(0, path)
import requests

from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from .config import Config
from Gen import ChannelService
from Gen.ttypes import *
import tempfile

class Channel(Config):
    
    client = None

    authToken = None
    mid = None
    channel_access_token = None
    token = None
    obs_token = None
    refresh_token = None

    def __init__(self, authToken,mid):
        Config.__init__(self)
        self.mid = mid
        self.authToken = authToken
        self.transport = THttpClient.THttpClient(self.LINE_HOST_DOMAIN, None, self.LINE_API_QUERY_PATH_FIR)
        self.transport.path = self.LINE_AUTH_QUERY_PATH
        self.transport.setCustomHeaders({"X-Line-Application" : self.APP_NAME,"User-Agent" : self.USER_AGENT,"X-Line-Access": authToken})
        self.transport.open()
        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self.client = ChannelService.Client(self.protocol)

        self.transport.path = self.LINE_CHAN_QUERY_PATH

    def login(self):
        result = self.client.issueChannelToken("1341209950")

        self.channel_access_token = result.channelAccessToken
        self.token = result.token
        self.obs_token = result.obsToken
        self.refresh_token = result.refreshToken

    def new_post(self, text):

        header = {
            "Content-Type": "application/json",
            "User-Agent" : self.USER_AGENT,
            "X-Line-Mid" : self.mid,
            "x-lct" : self.channel_access_token,
        }

        payload = {
            "postInfo" : { "readPermission" : { "type" : "ALL" } },
            "sourceType" : "TIMELINE",
            "contents" : { "text" : text }
        }

        r = requests.post(self.LINE_HOST_DOMAIN + "/mh/api/v39/post/create.json",
            headers = header,
            data = json.dumps(payload)
        )

        return r.json()

    def postPhoto(self,text,path):
        header = {
            "Content-Type": "application/json",
            "User-Agent" : self.USER_AGENT,
            "X-Line-Mid" : self.mid,
            "x-lct" : self.channel_access_token,
        }

        payload = {
            "postInfo" : { "readPermission" : { "type" : "ALL" } },
            "sourceType" : "TIMELINE",
            "contents" : { "text" : text ,"media" :  [{u'objectId': u'F57144CF9ECC4AD2E162E68554D1A8BD1a1ab0t04ff07f6'}]}
        }
        r = requests.post(self.LINE_HOST_DOMAIN + "/mh/api/v39/post/create.json",
            headers = header,
            data = json.dumps(payload)
        )

        return r.json()

    def like(self, mid, postid, likeType=1001):

        header = {
            "Content-Type" : "application/json",
            "X-Line-Mid" : self.mid,
            "x-lct" : self.channel_access_token,
        }

        payload = {
            "likeType" : likeType,
            "activityExternalId" : postid,
            "actorId" : mid
        }

        r = requests.post(self.LINE_HOST_DOMAIN + "/mh/api/v39/like/create.json?homeId=" + mid,
            headers = header,
            data = json.dumps(payload)
        )

        return r.json()

    def comment(self, mid, postid, text):
        header = {
            "Content-Type" : "application/json",
            "X-Line-Mid" : self.mid,
            "x-lct" : self.channel_access_token,
        }

        payload = {
            "commentText" : text,
            "activityExternalId" : postid,
            "actorId" : mid
        }

        r = requests.post(self.LINE_HOST_DOMAIN + "/mh/api/v39/comment/create.json?homeId=" + mid,
            headers = header,
            data = json.dumps(payload)
        )

        return r.json()

    def activity(self, limit=20):

        header = {
            "Content-Type" : "application/json",
            "X-Line-Mid" : self.mid,
            "x-lct" : self.channel_access_token,
        }

        r = requests.get(self.LINE_HOST_DOMAIN + "/tl/mapi/v39/activities?postLimit=" + str(limit),
            headers = header
        )
        return r.json()
    def getAlbum(self, gid):

        header = {
            "Content-Type" : "application/json",
            "X-Line-Mid" : self.mid,
            "x-lct": self.channel_access_token,

        }

        r = requests.get(self.LINE_HOST_DOMAIN + "/mh/album/v3/albums?type=g&sourceType=TALKROOM&homeId=" + gid,
            headers = header
        )
        return r.json()
    def changeAlbumName(self,gid,name,albumId):
        header = {
            "Content-Type" : "application/json",
            "X-Line-Mid" : self.mid,
            "x-lct": self.channel_access_token,

        }
        payload = {
            "title": name
        }
        r = requests.put(self.LINE_HOST_DOMAIN + "/mh/album/v3/album/" + albumId + "?homeId=" + gid,
            headers = header,
            data = json.dumps(payload),
        )
        return r.json()
    def deleteAlbum(self,gid,albumId):
        header = {
            "Content-Type" : "application/json",
            "X-Line-Mid" : self.mid,
            "x-lct": self.channel_access_token,

        }
        r = requests.delete(self.LINE_HOST_DOMAIN + "/mh/album/v3/album/" + albumId + "?homeId=" + gid,
            headers = header,
            )
        return r.json()
    def getNote(self,gid, commentLimit, likeLimit):
        header = {
            "Content-Type" : "application/json",
            "X-Line-Mid" : self.mid,
            "x-lct": self.channel_access_token,

        }
        r = requests.get(self.LINE_HOST_DOMAIN + "/mh/api/v39/post/list.json?homeId=" + gid + "&commentLimit=" + commentLimit + "&sourceType=TALKROOM&likeLimit=" + likeLimit,
            headers = header
        )
        return r.json()

    def postNote(self, gid, text):
        header = {
            "Content-Type": "application/json",
            "User-Agent" : self.USER_AGENT,
            "X-Line-Mid" : self.mid,
            "x-lct" : self.channel_access_token,
        }
        payload = {"postInfo":{"readPermission":{"homeId":gid}},
                   "sourceType":"GROUPHOME",
                   "contents":{"text":text}
                   }
        r = requests.post(self.LINE_HOST_DOMAIN + "/mh/api/v39/post/create.json",
            headers = header,
            data = json.dumps(payload)
            )
        return r.json()

    def getDetail(self, mid):
        header = {
            "Content-Type": "application/json",
            "User-Agent" : self.USER_AGENT,
            "X-Line-Mid" : self.mid,
            "x-lct" : self.channel_access_token,
        }

        r = requests.get(self.LINE_HOST_DOMAIN + "/ma/api/v1/userpopup/getDetail.json?userMid=" + mid,
        headers = header
        )
        return r.json()

    def getHome(self,mid):
        header = {
                    "Content-Type": "application/json",
                    "User-Agent" : self.USER_AGENT,
                    "X-Line-Mid" : self.mid,
                    "x-lct" : self.channel_access_token,
        }

        r = requests.get(self.LINE_HOST_DOMAIN + "/mh/api/v39/post/list.json?homeId=" + mid + "&commentLimit=2&sourceType=LINE_PROFILE_COVER&likeLimit=6",
        headers = header
        )
        return r.json()
    def getCover(self,mid):
        h = self.getHome(mid)
        objId = h["result"]["homeInfo"]["objectId"]
        return "http://dl.profile.line-cdn.net/myhome/c/download.nhn?userid=" + mid + "&oid=" + objId
    def createAlbum(self,gid,name):
        header = {
                    "Content-Type": "application/json",
                    "User-Agent" : self.USER_AGENT,
                    "X-Line-Mid" : self.mid,
                    "x-lct" : self.channel_access_token,
        }
        payload = {
                "type" : "image",
                "title" : name
        }
        r = requests.post(self.LINE_HOST_DOMAIN + "/mh/album/v3/album?count=1&auto=0&homeId=" + gid,
            headers = header,
            data = json.dumps(payload)
        )
        return r.json()

    def createAlbum2(self,gid,name,path,oid):
        header = {
                    "Content-Type": "application/json",
                    "User-Agent" : self.USER_AGENT,
                    "X-Line-Mid" : self.mid,
                    "x-lct" : self.channel_access_token,
        }
        payload = {
                "type" : "image",
                "title" : name
        }
        r = requests.post(self.LINE_HOST_DOMAIN + "/mh/album/v3/album?count=1&auto=0&homeId=" + gid,
            headers = header,
            data = json.dumps(payload)
        )
      