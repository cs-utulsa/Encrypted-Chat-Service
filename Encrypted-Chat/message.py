import json

class Message:
    """
    This class outlines the messaging and control protocol for the chat client.
    The message has two sections defined as HEADERS and CONTENT.

    The header section contains parameters useful for message processing in the future.
    """
    
    _content = None
    _headers = {'username': 'anonymous', 'message_type': 'message'}


    def __init__(self, content=None):
        self._content = content


    def parseMsg(self, msg: str):
        data = json.loads(msg)
        self._content = data['content']
        self._headers = data['headers']

    def setContent(self, msg):
        self._content = msg
        
    def getHeaders(self):
        return self._headers

    def getHeader(self, header):
        return self._headers[header]


    def getContent(self):
        return self._content


    def getData(self):
        data = {'headers': self._headers, 'content': self._content}
        return json.dumps(data)


    def setHeader(self, header: str, content: str):
        self._headers[header] = content