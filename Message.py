import random


'''
@auhor:         Alessio Moretti (AGESCI RM97)
@version:       0.0.1 (alpha)

PLEASE NOTE THAT THE SOFTWARE IS NOT INTENDED TO BE A FRAMEWORK
IT IS UNDER ALPHA TESTING AND IT ONLY SUPPORTS TEXT MESSAGES FOR NOW

MESSAGE CLASS CAN SUPPORT A LOT MORE FEATURES NOW IN PROJECTING PHASE
'''

class Message:
    def __init__(self, message_id, message_from, message_date, message_chat, message_text):
        '''
        this class is used to handle updates and replies through Telegram Messenger bot API
        :param message_id: int, the message unique identifier
        :param message_from: User, the user who sent the message
        :param message_date: string, the message date
        :param message_chat: User or GroupChat, the chat identifier to send the reply
        :param message_text: string, the textual message
        :return: the Message class
        '''
        self._id      = message_id
        self._from    = message_from
        self._date    = message_date
        self._chat    = message_chat
        self._chat_id = message_chat['id']
        self._text    = message_text
        # this boolen will be used to be aware of a necessary reply
        self._reply   = False

    def getText(self):
        return self._text

    def getChat(self):
        return self._chat

    def isReplyWaiting(self):
        return self._reply

    def readTaccuino(self):
        '''
        this method is used to retrieve a random quote from the Taccuino of B.P.
        :return: string, the quote
        '''
        with open('./resources/taccuino.txt', 'r') as taccuino:
            quotes = taccuino.readlines()
            taccuino.close()
            return quotes[random.randint(0, len(quotes))]

    def insertSuggerimento(self, text):
        '''
        this method is used to store advices and suggestions by the other scouts
        (it is intended that the bot staff will be sure of their content before use them officially)
        :param text: string, the suggestion made
        :return: None
        '''
        with open('./resources/suggerimenti.txt', 'a') as suggerimenti:
            suggerimenti.write(text + "\n")
            suggerimenti.close()

    def readSuggerimento(self):
        '''
        this method is used to retrieve the suggestions approved by the staff
        and stored into the bivacco.txt
        :return: string, the suggestion
        '''
        with open('./resources/bivacco.txt', 'r') as bivacco:
            advices = bivacco.readlines()
            if len(advices) != 0:
                print("Suggerimenti presenti")
                bivacco.close()
                return advices[random.randint(0, len(advices))]
            else:
                bivacco.close()
                return "Nessuno ha ancora condiviso nulla... Vuoi essere il primo?\n/suggerisci"

    def makeReply(self):
        '''
        thsi method returns a reply appropriate to the request made by the user
        :return: dictionary, chat id to send the message using Telegram API and the string
                 with the reply
        '''
        reply = ""
        if self._text == "/start":
            reply = "Ciao, benvenuto fratellino/sorellina. Spero di poterti essere d'aiuto. Buona caccia e buona strada!"

        if self._text == "/help":
            reply = "/taccuino potrai leggere alcuni suggerimenti direttamente da B.P.\n" \
                    "/bivacco potrai leggere alcuni suggerimenti provenienti dai ragazzi e dai capi che hanno voluto condividere la propria esperienza!\n" \
                    "/suggerisci inserisci un motto o un suggerimento che vuoi condividere con i tuoi fratelli scout ed una tua firma.\n\n Buona caccia e buona strada!"

        if self._text == "/taccuino":
            reply = self.readTaccuino()

        if self._text == "/bivacco":
            reply = self.readSuggerimento()

        if self._text == "/suggerisci":
            reply = "Scrivi il suggerimento e chi sei!"
            self._reply = True

        # easter egg from the author :D
        # Yours in scouting!
        if self._text == "/rm97":
            reply = "Buona caccia! \nTasso Intellettuale, AGESCI Roma97"

        return {'chat_id': self._chat_id, 'text': reply}
