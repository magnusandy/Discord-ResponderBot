#a simple discord bot that will speak a response phrase into the channel any time a trigger phrase is uttered
#I.e. if the trigger is "press F to pay respects" and the response is "F" any time 'press F to pay respects' is found in a message, the bot will say 'F' once

import discord
import asyncio
import re
import random
import randPhrases

client = discord.Client()

#-----------------------------HANGMAN Start
isHangmanEnabled = True
hangmanMessagePrefix = '```Hangman\n'
hangmanMessageSuffix = '```'
hangmanMaxTries = 6
hangmanGuessCommand = '!hangmanGuess '
hangmanGuessAllCommand = '!hangmanGuessAll '
hangmanStartCommand = '!hangmanStart'
hangmanHelpCommand = '!hangmanHelp'
hangmanToggleCommand = '!hangmanToggle'

hangmanIsStarted = False
hangmanPuzzle = [] #will be array of tuples, (letter char, visible bool)
hangmanCurrentGuesses = []
hangmanCurrentTries = 0

#disables the hangman module
def hangmanToggle():
    global isHangmanEnabled
    resetHangman()
    isHangmanEnabled = not isHangmanEnabled
    if isHangmanEnabled:
        return "hangman has been enabled"
    else:
        return "hangman is now disabled"

#starts a new hangman puzzle, or displays the current puzzle
def hangmanStart():
    global hangmanIsStarted, hangmanCurrentTries, hangmanPuzzle, hangmanCurrentGuesses
    if hangmanIsStarted:
        return hangmanMessagePrefix+'there is already a game in progress:\n'+getVisiblePuzzle()+hangmanMessageSuffix
    else:
        #set up the new game
        hangmanIsStarted = True
        hangmanPuzzle = []
        hangmanCurrentTries = hangmanMaxTries
        hangmanCurrentGuesses = []
        puzzle = generatePuzzleString()
        print(puzzle)
        #loop through and add everything into the main loop, if there are spaces, they should be visible
        for chars in puzzle:
            if chars == ' ':
                hangmanPuzzle.append(list([chars, True]))
            else:
                hangmanPuzzle.append(list([chars, False]))
        print(hangmanPuzzle)
        return hangmanMessagePrefix+"New Puzzle started:\n"+getVisiblePuzzle()+hangmanMessageSuffix

#guesses a single letter, if the letter was already guesssed nothing happens, if its a new find, reveal it and add to list, otherwise lower count and add to list
#handles when the game ends
def hangmanGuess(rawMessage):
    global hangmanCurrentTries
    cleaned = str(rawMessage).rstrip()[len(hangmanGuessCommand):]
    guess = cleaned.lower()
    gotOneRight = False

    if hangmanIsStarted == False:
        return hangmanMessagePrefix + getVisiblePuzzle() + hangmanMessageSuffix

    if len(guess) != 1:
        return "if you want to guess the whole message, use !guessAll, otherwise guess only one character"

    else:
        #handle normal guessing
        if guess in hangmanCurrentGuesses: #already been guessed
            return hangmanMessagePrefix+"You have already guessed that!\n"+getVisiblePuzzle()+hangmanMessageSuffix

        for tups in hangmanPuzzle: #otherwise we need to look through to see if its a correct guess
            if (guess == tups[0]): #correct guess
                gotOneRight = True
                tups[1] = True

        if gotOneRight == True:
            hangmanCurrentGuesses.append(guess)
            if isPuzzleComplete():
                returnMessage = hangmanMessagePrefix + "You have completed The puzzle!\n" + getVisiblePuzzle() + hangmanMessageSuffix
                resetHangman()
                return returnMessage
            else:
                return hangmanMessagePrefix+"Correct!\n"+getVisiblePuzzle()+hangmanMessageSuffix
        else: #no right answers
            hangmanCurrentGuesses.append(guess)
            hangmanCurrentTries = hangmanCurrentTries - 1
            if hangmanCurrentTries == 0:
                returnMessage = hangmanMessagePrefix + "Nice try but you failed!\n" + getVisiblePuzzle() + hangmanMessageSuffix
                resetHangman()
                return returnMessage
            else:
                return hangmanMessagePrefix + "Wrong Guess!\n" + getVisiblePuzzle() + hangmanMessageSuffix

#gives the option of trying to guess the whole message, if correct you win, if wrong, lose a life and nothing is revealed
def hangmanGuessAll(rawMessage):
    global hangmanCurrentTries
    cleaned = str(rawMessage).rstrip()[len(hangmanGuessAllCommand):]
    guess = cleaned.lower()
    if len(guess) <= 1: #bad
        return "try using !hangmanGuess instead"

    #regular case
    if guess == puzzleAsString():
        returnMessage = hangmanMessagePrefix + "Wow Great Job, Thats Right!\n" + guess +"\n"+ hangmanMessageSuffix
        resetHangman()
        return returnMessage
    else:
        hangmanCurrentTries = hangmanCurrentTries - 1
        if hangmanCurrentTries == 0:
            returnMessage = hangmanMessagePrefix + "Nice try but you failed!\n" + getVisiblePuzzle() + hangmanMessageSuffix
            resetHangman()
            return returnMessage
        else:
            return hangmanMessagePrefix + "Wrong Guess!\n" + getVisiblePuzzle() + hangmanMessageSuffix


#returns the string value of the original puzzle
def puzzleAsString():
    s = ""
    for c in hangmanPuzzle:
        s = s + str(c[0])
    return s

#resets the various globals of the game
def resetHangman():
    global hangmanIsStarted, hangmanCurrentTries, hangmanPuzzle, hangmanCurrentGuesses
    #set up the new game
    hangmanIsStarted = False
    hangmanPuzzle = []
    hangmanCurrentTries = hangmanMaxTries
    hangmanCurrentGuesses = []

#returns true if everything is revealed
def isPuzzleComplete():
    isComp = True
    for t in hangmanPuzzle:
        if t[1] == False:
            isComp = False
    return isComp


#will return the puzzle string with newline appended, showing only the visible characters and _ for the rest
def getVisiblePuzzle():
    puzzleString = ''
    guessString = 'Current Guesses:'
    if hangmanIsStarted:
        for tups in hangmanPuzzle:
            if tups[1]: #if visible is true
                puzzleString = puzzleString + tups[0]
            else:
                puzzleString = puzzleString + '_'
        for c in hangmanCurrentGuesses:
            guessString = guessString + ' '+c+' '
        return puzzleString+"\nGuesses left: "+str(hangmanCurrentTries)+"\n"+guessString
    else:
        return 'No puzzle started yet, try !hangmanStart to play\n'

#fetches a new puzzle string
def generatePuzzleString():
    return randPhrases.getRandomPhrase()

def hangmanHelp():
    return hangmanMessagePrefix+"!hangmanStart starts a new game\n!hangmanGuess <single letter> will attempt a guess on the current game\n!hangmanGuessAll <whole phrase> allows for you to attempt to solve the puzzle"+hangmanMessageSuffix
#-----------------------------HANGMAN END

#-----------------------------MAGIC 8 BALL Start

def roll8Ball():
    choices = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
    return choices[random.randint(0,19)]
#-----------------------------MAGIC 8 BOT End


#------------------------ RESPONDER BOT START
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
#-----------------------------RESPONDER BOT END



#-----------------------------MAIN LOOPS
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
    #hangmanCommands
    if message.content == hangmanStartCommand and isHangmanEnabled:
        messageToSend = hangmanStart()
    elif message.content.startswith(hangmanGuessCommand) and isHangmanEnabled:
        messageToSend = hangmanGuess(message.content)
    elif message.content.startswith(hangmanGuessAllCommand) and isHangmanEnabled:
        messageToSend = hangmanGuessAll(message.content)
    elif message.content == hangmanHelpCommand and isHangmanEnabled:
        messageToSend = hangmanHelp()
    elif message.content == hangmanToggleCommand:
        messageToSend = hangmanToggle()
    elif message.content == ('!8ball'):
        messageToSend = roll8Ball()
    elif message.content.startswith('!yhadd '):
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