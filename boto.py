"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import requests
from random import shuffle




def containQ(question):
    if "?" in question:
        return "Say whaaaaaaaaaaaaaaaaaattt {}".format(question)

@route('/', method='GET')
def index():
    return template("chatbot.html")


response_bank={
    'travel': ["France", "Italy", "Jamaica", "US", "Australia", "New Zealand", "Russia", "Thailand"],
    'swear_response': ["wash your mouth", "get your sh*t together"],
    'greetings': ["hi", "hello", "what's up", "shalom"],
    'time_of_day': ["morning", "noon", "night"],
    'food_categories': ["Olivery", "Brooklyn", "Su Su & Sons", "Malka", "Meatos", "Abu Adham", "Hakosem", "Anastasia", "The Old Man and the Sea", "Sabich Frishman", "Yakimono", "Ze", "Nam"],
    'music_recs':["music","song" , "beat", "jam", "spotify"],


}




questions_bank={
    'travel': ["travel", "vacation"],
    'swear_word': ["fuck","" "shit", "cunt","bitch", "bullshit", "asshole", "motherfucker", "shitface", "shithead"],
    'greetings': ["hi", "hello", "what's up", "shalom"],
    'time_of_day': ["morning", "noon", "night"],
    'food_categories': ["restaurant","breakfast","lunch", "dinner", "italian", "pizza", "american", "kosher", "bbq", "hummus", "falafel", "vegan", "mediterannean", "sabich", "asian", "sushi", "thai"],
    'music_recs':["music","song" , "beat", "jam", "spotify","rock", "blues", "jazz", "rap", "hip hop", "classical", "electronic"],


}



def secondary_function(input):
    if any(input.find(s)>=0 for s in questions_bank['food_categories']):
        new_list = response_bank['food_categories']
        if questions_bank['food_categories'][0]:
            return new_list[0]



def talk_to_robot(input):
    if any(input.find(s)>=0 for s in questions_bank['swear_word']):
        new_list = response_bank['swear_response']
        shuffle(new_list)
        return new_list[0]
    else:
        return secondary_function(input)


test_sample = 'where should i travel to?'
print(talk_to_robot(test_sample))

# def travel_words(input)

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    print("chat received {}".format(user_message))
    return json.dumps({"animation": "excited", "msg": talk_to_robot(user_message)})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()


