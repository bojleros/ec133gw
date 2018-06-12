#!/usr/bin/python

import serial
import time
import sys
import os
import json

pwd = os.path.dirname(os.path.realpath(__file__))

from flask import Flask
from flask import request

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

app = Flask(__name__)
app.debug = True

conf=None


@app.route('/setch/<int:c>/<int:b>', methods=['GET'])
def set_light(c,b,i=0):
  if c<0 or c>2:
    return("Channel out of range",400)
  if b>255:
    b=255
  if b<0:
    b=0

  while i<3:
    try:
      #rs.write_register(c,b,0)
      conf['rtu'].execute(conf['ec133'], cst.WRITE_SINGLE_REGISTER, c, output_value=b)
    except Exception as e:
      print(str(e))
      time.sleep(float(conf['RtuMaster']['timeout']))
      i=i+1
    else:
      return ("Success",200)

  return ("This rs485 sucks a lot", 500)

@app.route('/setall/<int:b>', methods=['GET'])
def setall_light(b,i=0):
  if b>255:
    b=255
  if b<0:
    b=0

  while i<3:
    try:
      #rs.write_registers(0,[b,b,b])
      conf['rtu'].execute(conf['ec133'], cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[b,b,b])
    except Exception as e:
      print(str(e))
      time.sleep(float(conf['RtuMaster']['timeout']))
      i=i+1
    else:
      return ("Success",200)

  return ("This rs485 sucks a lot", 500)


def init():
  """
  Main routine only to initialize configs
  """
  global conf
  global lh

  if os.path.isfile(pwd + '/ec133gw.json'):
    cfgpath = pwd + '/ec133gw.json'
  else:
    cfgpath = '/etc/ec133gw/ec133gw.json'

  with open(cfgpath) as cf:
    conf=json.load(cf)

  conf['lh'] = modbus_tk.utils.create_logger("console")

  serconf = conf['RtuMaster'].get('serial',None)
  if serconf == None:
    print("Unable to load serial port config")
    sys.exit(1)

  try:
    conf['rtu'] = modbus_rtu.RtuMaster(serial.Serial(**serconf))
  except Exception as e:
    print(str(e))
    sys.exit(2)

  conf['rtu'].set_timeout(float(conf['RtuMaster']['timeout']))


if __name__ == "__main__":

  if conf == None:
    init()

  app.run(host=conf['listen']['host'],port=int(conf['listen']['port']))

