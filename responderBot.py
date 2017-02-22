#a simple discord bot that will speak a response phrase into the channel any time a trigger phrase is uttered
#I.e. if the trigger is "press F to pay respects" and the response is "F" any time 'press F to pay respects' is found in a message, the bot will say 'F' once

import discord
import asyncio
import re

client = discord.Client()

#key value tuples (<trigger phrase>, <response>)
phrases = [('yeah haha', 'Yeah haha.'), ('big guy', 'For you.')]

#returns the response phrase if the trigger phrase is found
def findResponse(messageContents):
    m = messageContents.lower()
    for set in phrases:
        if m.find(set[0]) >= 0: #substring exists in the message
            return set[1]
    return ''

#if the add command is called this will check the validity of the input and add the phrase/response combo if it all checks out
def addPhrase(rawMessage):
    pA = re.findall(r"\'(.*?)\'",rawMessage)#creates a list of all strings wrapped in '
    #print(pA)
    if len(pA) != 2:
        return 'error in command, bad arguments, watch your !\'s'
    phrase = pA[0].rstrip().lstrip().lower() #strips leading/trailing whitespace and lowercases everything
    resp = pA[1].rstrip().lstrip()
    if(phrase == '') or (resp == ''):
        return "cannot add empty phrase or response"

    #finally add the phrase
    phrases.append((phrase, resp))
    return 'added successfully'

#lists all the phrases to the channel
def listPhrases():
    retMess = '```List of current triggers and responses:\n'
    for i, set in enumerate(phrases):
        retMess = retMess + '['+str(i)+'] trigger: \''+set[0]+'\' response: \''+set[1]+'\'\n'
    retMess = retMess + "```"
    return retMess

def deletePhrase(rawMessage):
    cleaned = str(rawMessage).rstrip().split(" ")
    try:
        indexToDelete = int(cleaned[1])
        if(indexToDelete >= 0) and (indexToDelete < len(phrases)):
            del phrases[indexToDelete]
            return "deleted successfully"
        else:
            return "index out of bounds"
    except ValueError:
        return "Pass in the integer index you wish to delete"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#main loop of the program
@client.event
async def on_message(message):
    messageToSend = ''
    if message.content.startswith('!yhadd '):
        messageToSend = addPhrase(message.content)
#       handle adding a new set of values
#       trigger cant be the same as phrase
    elif message.content == '!yhlist':
        messageToSend = listPhrases()
    elif message.content.startswith('!yhdelete '):
        messageToSend = deletePhrase(message.content)
#       delete given value
    elif message.content == ('!yhhelp'):
        messageToSend = "```!yhadd '<trigger phrase>' '<response' i.e. !yhadd 'big guy' 'for you'.\n!yhlist lists all phrases with their id number\n!yhdelete <phrase id number from !list>```"
    else: #general case, look for responses
        messageToSend = findResponse(message.content)

    #if (message.content.lower() == 'yeah haha'):
    #    messageToSend = "Yeah haha."
    #if((message.content.lower().find('big guy') >= 0) and (message.content.lower().find('for you') == -1)):
#        print('this worked')
    #    messageToSend = "For you."
    if (messageToSend != '') and message.author.id != '283444723836780545':
        #print( message.author.id)
        await client.send_message(message.channel, messageToSend)
client.run('MjgzNDQ0NzIzODM2NzgwNTQ1.C41KFA.JHl7X5nYZWSR1U_3ATrDnftH6K8')