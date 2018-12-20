try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
global intent

def lambda_handler(event, context):
    global intent
    
    if event["request"]["type"] =="LaunchRequest":
        output="Welcome to the Chatbot."
        session_end_status=False
    elif event["request"]["type"] =="IntentRequest":
        if event["request"]["intent"]["name"] =="getQueryData":
            #Retrieves whatever was queried
            query=event["request"]["intent"]["slots"]["Query"]["value"]
            splitQuery=query.split()
            inputString=""
            #This for loop formats the query so that the web-api will support it
            for word in splitQuery:
                commaCheck=word[-1]
                formattedWord=word[:-1]
                if(word==splitQuery[-1]):
                    inputString+=str(word)
                else:
                    if(commaCheck==","):
                        inputString+=str(formattedWord)+"%2C%20"
                        continue
                    inputString+=str(word)+"%20"
            #Inputs the formatted query to the end of the web-api and opens the url and
            #Stores the output of the webpage as the output 
            baseurl="http://10.87.74.154:5555/chat/"
            yqlurl=baseurl+str(inputString)
            finalurl=Request(yqlurl,headers={'User-Agent':'Mozilla/5.0'})
            queryResult=urlopen(finalurl).read()
            output=str(queryResult)

            intent="getQueryData"
            session_end_status=False
        else:
            output="I am exiting from intent "+event["request"]["intent"]["name"]
            session_end_status=True
            
    
    # TODO implement
    return  {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": output
                },
                "card": {
                    "type": "Simple",
                    "title": "Chatbot Information",
                    "text": output
                },
                "reprompt": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": ""
                 }
            },
            "shouldEndSession": session_end_status
            },
            "sessionAttributes": {}
        }
