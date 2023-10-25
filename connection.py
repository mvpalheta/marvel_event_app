from streamlit.connections import ExperimentalBaseConnection
import streamlit as st
import requests
import hashlib
import time


class MarvelAPIEventConnection(ExperimentalBaseConnection):

    def _connect(self, public_key, private_key, offset, eventobj=None, eventid=None):
        # Set credentials
        ts = str(time.time())
        string2hash = (ts+private_key+public_key).encode('utf-8')
        hash = hashlib.md5(string2hash).hexdigest()

        if eventid == None:
            url = "https://gateway.marvel.com:443/v1/public/events?limit=100&offset=%s&ts=%s&apikey=%s&hash=%s" % (offset, ts, public_key, hash)
            self.conn = requests.get(url)
        elif eventid is not None and eventobj is None :
            url = "https://gateway.marvel.com:443/v1/public/events/" + str(eventid) + "?limit=100&offset=%s&ts=%s&apikey=%s&hash=%s" % (offset, ts, public_key, hash)
            self.conn = requests.get(url)
        elif eventid is not None and eventobj is not None :
            url = "https://gateway.marvel.com:443/v1/public/events/" + str(eventid) + "/" + eventobj + "?limit=100&offset=%s&ts=%s&apikey=%s&hash=%s" % (offset, ts, public_key, hash)
            self.conn = requests.get(url)                         

    def get(self, ttl):
        @st.cache_data(ttl=ttl)
        def _get():
            req = self.conn.json()
            return req
        return _get()
