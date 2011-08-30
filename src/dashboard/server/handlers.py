from collections import defaultdict
from datetime import date, datetime, time, timedelta
from decimal import *
from mozautoeslib import ESLib
import ConfigParser
import csv
import dateutil.parser
import re
import templeton
import templeton.handlers
import web

try:
  import json
except:
  import simplejson as json

config = ConfigParser.ConfigParser()
config.read("settings.cfg")
ES_SERVER = config.get("database", "ES_SERVER")
eslib = ESLib(ES_SERVER, config.get("database", "INDEX"), config.get("database", "TYPE"))

# "/api/" is automatically prepended to each of these
urls = (
 '/perfdata/?',"PerfdataHandler"
)

class PerfdataHandler():
    @templeton.handlers.json_response
    def GET(self):
        params,body = templeton.handlers.get_request_parms()

        queryparams = defaultdict()

        #No params supplied -- query everything
        if not params:
            queryparams["test"] = "*"

        #Params supplied, query by them
        for arg in params:
            #Treat startdate and enddate uniquely (build a daterange for the query)
            if arg == "startdate" or arg == "enddate":
                try:
                    queryparams["date"].append(str(params[arg][0]))
                except:
                    queryparams["date"] = []
                    queryparams["date"].append(str(params[arg][0]))
            else:
                queryparams[arg] = params[arg][0]

        #Query based on params supplied, return json
        result = eslib.query(queryparams)
        return result
