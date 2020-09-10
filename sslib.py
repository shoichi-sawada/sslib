#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import yaml
import logging

class Dict(dict):
  def __init__(self, d=None, **kwargs):
    if isinstance(d, str): d = yaml.load(d)
    if not isinstance(d, dict): d = {}
    d.update(**kwargs)
    for key, val in d.items(): setattr(self, str(key), val)

  def __setattr__(self, key, val):
    if isinstance(val, dict):
      val = Dict(val)
    elif isinstance(val, (list, tuple)):
      val = [Dict(x) if isinstance(x, dict) else x for x in val]
    dict.__setattr__(self, key, val)
    dict.__setitem__(self, key, val)

  __setitem__ = __setattr__


  def __delattr__(self, key):
    dict.__delattr__(self, key)
    dict.__delitem__(self, key)

  __delitem__ = __delattr__

def readConf(confFile='conf.yaml'):
  conf = Dict(yaml.load(open(confFile)))
  return conf

def initLogger(name='', output='stdout', level=logging.INFO, fmt='normal',
               datefmt = '%Y-%m-%d %H:%M:%S'):
  logger = logging.getLogger(name)
  if output == 'stdout':
    handler = logging.StreamHandler()
  else:
    handler = logging.FileHandler(output)
  handler.setLevel(level)
  if handler.level < logger.level:
    logger.setLevel(level)
  if fmt == 'normal':
    fmt = '%(asctime)s %(levelname)s: %(message)s'
  elif fmt == 'long':
    fmt = '%(asctime)s.%(msecs)03d - %(name)s (%(levelname)s): ' \
          '%(funcName)s [%(filename)s:%(lineno)d]: %(message)s'
  elif fmt == 'short':
    fmt = '%(asctime)s: %(message)s'
    datefmt = '%H%M%S'
  handler.setFormatter(logging.Formatter(fmt, datefmt))
  logger.addHandler(handler)  
  logger.debug('Init logger: %s'%(name))
  return logger

def getLogger(name=''):
  logger = logging.getLogger(name)
  return logger

