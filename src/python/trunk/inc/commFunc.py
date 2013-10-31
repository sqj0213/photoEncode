#!/bin/env python
#coding=utf-8

import logging,ConfigParser
__author__ = 'sunshare'
"""
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
"""
logDict = {'debug':logging.DEBUG,
           'info':logging.INFO,
           'warning':logging.warn,
           'error':logging.ERROR
}
logObj = logging




def convertListToDict( _cf ):
    sectionsList = _cf.sections()
    retDict = {}
    for val1 in sectionsList:
        retDict[ val1 ] = dict( _cf.items( val1 ) )
    return retDict


cf = ConfigParser.ConfigParser()
cf.read( './conf/conf.ini' )
confIniDict = convertListToDict(cf)

logObj.basicConfig(
    filename=confIniDict[ 'log' ][ 'log' ],
    filemode='a+',
    format='%(asctime)s %(levelname) 5s %(name)s | %(message)s %(filename)s %(module)s %(lineno)d',
    datefmt='%Y-%m-%dT%H:%M:%S%z',
    level=logDict[ confIniDict['log']['loglevel'] ])

