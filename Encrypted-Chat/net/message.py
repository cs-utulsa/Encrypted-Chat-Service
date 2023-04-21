import json

class Message:
    """
    This class outlines the messaging and control protocol for the chat client.
    The message has two sections defined as HEADERS and CONTENT.

    The header section contains parameters useful for message processing in the future.
    """

    _MAX_CONTENT_SIZE = 2046
    _MAX_MESSAGE_SIZE = 2048
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

    def getHeader(self, header) -> str:
        return self._headers[header]


    def getContent(self) -> str:
        return self._content

    def setHeader(self, header: str, content: str):
        self._headers[header] = content

    def setHeaders(self, headers:dict):
        self._headers = headers

    def getData(self) -> list:
        data = {'headers': self._headers, 'content': self._content}
        self.setHeader('seg', '0:0')
        raw_data = json.dumps(data)
        if len(raw_data) >= self._MAX_MESSAGE_SIZE:
            print("Oversized Message - Fragmenting")

            # Bundle of segments
            seg_bundle = []
            # Bundle of data parts
            data_bundle = []

            # Create data parts
            counter = 0
            tmp_data = ""
            for c in self._content:
                if counter == self._MAX_CONTENT_SIZE-1:
                    tmp_data += c
                    data_bundle.append(tmp_data)
                    counter = 0
                    tmp_data = ""
                    continue
                tmp_data += c
                counter +=1
            if tmp_data != '':
                data_bundle.append(tmp_data)

            # Create data segments
            max_segments = len(data_bundle)
            for cur_seg in range(0, max_segments):
                self.setHeader('seg', str(cur_seg)+':'+str(max_segments-1))
                seg_bundle.append(json.dumps({'headers': self._headers, 'content': data_bundle[cur_seg]}))
                cur_seg +=1
            return seg_bundle
        else:
            return [raw_data]