import http.client
import urllib.parse
import json

from Message import Message

'''
@auhor:         Alessio Moretti (AGESCI RM97)
@version:       0.0.1 (alpha)

PLEASE NOTE THAT THE SOFTWARE IS NOT INTENDED TO BE A FRAMEWORK
IT IS UNDER ALPHA TESTING AND IT ONLY SUPPORTS TEXT MESSAGES FOR NOW
'''


class ScoutBot:
    def __init__(self, token):
        '''
        this class defines the ScoutBot as its elementary functions
        :param token: string, the token given by the Telegram Messenger to access the bot platform API
        :return: a ScoutBot class
        '''
        # constructing the uri + url identifier
        self._uri            = "api.telegram.org"
        self._tok            = "/bot" + token
        # the API url for simple bot info
        self._get_me         = "/getMe"
        # the API url for retrieving updates
        self._get_updates    = "/getUpdates"
        self._updates_offset = 0
        # the API url for the send message
        self._send_message   = "/sendMessage"
        # the client
        self._client         = None

    def retrieveJSON(self, url, params=None):
        '''
        this method make a request using the HTTPSConnection client
        it can be a GET or a POST connection, depending upon the caller necessities
        :param url: string, the resource locator for the Telegram Messenger APIs
        :param params: dictionary, the POST params if POST is necessary
        :return: the response on success or None
        '''
        self._client = http.client.HTTPSConnection(self._uri)

        # perform a GET request
        if params is None:
            try:
                self._client.request("GET", self._tok + url)
                response = self._client.getresponse().read()
                return str(response, 'ascii')
            except:
                return None
        # perform a POST request
        else:
            try:
                headers = {"Content-type": "application/x-www-form-urlencoded"}
                params = urllib.parse.urlencode(params)
                self._client.request("POST", self._tok + url, params, headers)
                response = self._client.getresponse().read()
                return str(response, 'ascii')
            except:
                return None


    def getResponse(self, response):
        '''
        this method is used to retrieve the result in the response JSON by Telegram API
        :param response: string, the JSON given by the Telegram response
        :return: tuple, (boolean, dictionary)
        '''
        response = json.loads(response)
        if response['ok']:
            return True, response['result']
        else:
            return False, None

    def getMe(self):
        '''
        this is only a debug purposes method to access bot infos
        :return: dictionary open success or None
        '''
        response = self.retrieveJSON(self._get_me)
        _response = self.getResponse(response)
        if _response[0]:
            return _response[1]
        else:
            return None


    def getUpdates(self):
        '''
        this method is used to retrieve the updates and perform a reply action
        :return: dictionary upon success or None
        '''
        # in this very simple implementation the bot retrieve only an update at a time
        params = {'limit': 1, 'offset': self._updates_offset}
        response = self.retrieveJSON(self._get_updates, params)
        try:
            _response = self.getResponse(response)
        except:
            return None

        if _response[0]:
            # the Telegram API return a list of updates
            # it is necessary to check wheter the list is empty or not
            if len(_response[1]) != 0:
                print("telegram:", _response[1][0]['update_id'], "\nlocal:", self._updates_offset, "\n")
                if self._updates_offset == 0:
                    # it is necessary to make the offset be aligned to the Telegram offset in order
                    # to retrieve in the right order the updates from the remote storage
                    self._updates_offset = _response[1][0]['update_id']
                # updating local offset
                self._updates_offset += 1
            return _response[1]
        else:
            return None

    def readUpdate(self, update):
        '''
        this method read the updates and instantiates a Message object to handle the
        request and the reply
        :param update: dictionary, the update returned by Telegram
        :return: the Message object upon success or None
        '''
        # it is necessary that the message is present in the update
        # and it is necessary (in this very implementation) that the
        # message is a textual one
        if 'message' in update:
            if 'text' not in update['message']:
                return None
            else:
                return Message(update['message']['message_id'],
                               update['message']['from']      ,
                               update['message']['date']      ,
                               update['message']['chat']      ,
                               update['message']['text'])

    def sendMessage(self, message):
        '''
        this method is used to send a message using the rather simple Telegram API
        :param message: Message, the previously read updates can generate in the
                        Message object the correct reply
        :return: Telegram response upon success or None
        '''
        self._client = http.client.HTTPSConnection(self._uri)

        try:
            headers = {'Content-type': "application/x-www-form-urlencoded"}
            params  = urllib.parse.urlencode(message.makeReply())

            self._client.request("POST", self._tok + self._send_message, params, headers)
            response = self._client.getresponse().read()
            return str(response, 'ascii')
        except:
            return None


