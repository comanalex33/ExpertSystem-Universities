from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

from ChannelsManager import ChannelsManager

'''
    POC:
        - generate an id for the first call, can be used another call like /start
        - this should return a response in the next format:
            {
                "token": A_NUMERICAL_ID    -   this id will be used as an identifier to simulate a communication channel    (it works)
            }
            
        - there should be another call like
            - /execute?token=NUMERICAL_ID                  - This will return the first question                            (it works)
            - /execute?token=NUMERICAL_ID&answer=true      - This will return the next question/answer if answer was true   (it works)
            - /execute?token=NUMERICAL_ID&answer=false     - This will return the next question/answer if answer was false  (it works)
        - Exemplu raspuns:
            {
                "question": true or false
                "text": "Question text or answer text"
            }
            
        - cleanUp token data after 1 hour
        - return suggestions
            - filter programs and universities based on check (check is a query in jmespath query language format)
            - after all filters are applied, iterate through universities and return only the universities that have programs in the programs list
            - those universities are the suggested universities
'''


class InferenceMachine(BaseHTTPRequestHandler):
    """
        HTTP server request handler
    """
    
    def _send_response(self, code, response):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if code == 200:
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            res = {
                "message": response
            }
            self.wfile.write(json.dumps(res, indent=2).encode())
    
    def _process_parameters(self, parameters):
        token = None
        answer = None
        if 'token' in parameters:
            tokenValue = str(parameters['token'][0])
            if tokenValue.isdigit():
                token = int(tokenValue)
        if 'answer' in parameters:
            answerValue = str(parameters['answer'][0])
            if answerValue == 'true':
                answer = True
            elif answerValue == 'false':
                answer = False
            else:
                print('Wrong answer')
        return token, answer

    def _process_start(self):
        channelsManager = ChannelsManager().instance
        
        # Generate token and create response
        token = channelsManager.generate_uniqueToken()
        response = {
            "token": token
        }
        
        self._send_response(code=200, response=response)
        
    def _process_execute(self, parameters):
        channelsManager = ChannelsManager().instance
        
        token, answer = self._process_parameters(parameters=parameters)
        if token is None:
            self._send_response(code=400, response="Token is required")
            return
        if answer is None:
            if channelsManager.check_tokenPresent(token=token):
                response = channelsManager.get_responseForToken(token=token)
                
                self._send_response(code=200, response=response)
            else:
                self._send_response(code=400, response="This token does not exist")
                return
        else:
            if channelsManager.check_tokenPresent(token=token):
                channelsManager.update_responses(token=token, response=answer)
                response = channelsManager.get_responseForToken(token=token)
                
                self._send_response(code=200, response=response)
            else:
                self._send_response(code=400, response="This token does not exist")
                return
                
    def _process_results(self, parameters):
        channelsManager = ChannelsManager().instance
        token, answer = self._process_parameters(parameters=parameters)
        if token is None:
            self._send_response(code=400, response="Token is required")
            return
        if not channelsManager.check_tokenPresent(token=token):
            self._send_response(code=400, response="This token does not exist")
            return
        if not channelsManager.check_questionsAnswered(token=token):
            self._send_response(code=400, response="All questions must be answered")
            return
        
        response = channelsManager.get_results(token=token)
        self._send_response(code=200, response=response)

    def do_GET(self):
        query = urlparse(self.path).query
        path = urlparse(self.path).path
        parameters = parse_qs(query) if query else {}

        if path == "/start":
            self._process_start()
        elif path == "/execute":
            self._process_execute(parameters=parameters)
        elif path == "/results":
            self._process_results(parameters=parameters)
        else:
            self._send_response(code=404, response="This path does not exist, only /start, /execute and /results can be used")


if __name__ == "__main__":
    webserver = HTTPServer(("0.0.0.0", 8000), InferenceMachine)
    print(f"Server started on http://127.0.0.1:8000")

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    webserver.server_close()
    print("Server stopped.")
