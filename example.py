# -*- coding: utf-8 -*-
import LINEZX
from tcr.ttypes import *
from datetime import datetime
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast

cl = LINEZX.LINE()
cl.login(qr=True)
cl.loginResult()

#cl.login(token='TOKEN MU')
#cl.loginResult()
#wibu lu


reload(sys)
sys.setdefaultencoding('utf-8')

def bot(op):
    try:
        if op.type == 0:
            return
        if op.type == 25:
          msg = op.message
          #print (msg)
          pesan = msg.text
          if pesan is None:
            	return
          if "sp" == pesan.lower():
               start = time.time()
               cl.sendText(msg.to, "Testing....")
               elapsed_time = time.time() - start
               cl.sendText(msg.to, "%s detik" % (elapsed_time))

    except Exception as error:
        print error

while True:
	bot(cl.Poll.stream())