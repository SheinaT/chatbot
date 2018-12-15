"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import requests
from random import shuffle, randint


@route('/', method='GET')
def index():
    return template("chatbot.html")


response_bank={
    'travel': ["France", "Italy", "Jamaica", "US", "Australia", "New Zealand", "Russia", "Thailand"],
    'swear_response': ["wash your mouth", "get your sh*t together"],
    'greetings_response': ["hi", "hello", "what's up", "shalom"],
    'time_of_day': ["morning", "noon", "night"], 'food_categories': ["Olivery", "Brooklyn", "Su Su & Sons", "Malka", "Meatos", "Abu Adham", "Hakosem", "Anastasia", "The Old Man and the Sea", "Sabich Frishman", "Yakimono", "Ze", "Nam"],
    'music_recs':["The Strokes", "B.B. King" , "Louis Armstrong", "Childish Gambino", "Bach", "Tiesto", "Robyn"],
    'articles': None
}

questions_bank={
    'travel': ["travel", "vacation"],
    'swear_word': ["fuck","" "shit", "cunt","bitch", "bullshit", "asshole", "motherfucker", "shitface", "shithead"],
    'greetings': ["hi", "hello", "what's up", "shalom", "what's up?", "sup"],
    'food_generic_terms': ["food", "hungry", "restaurant"],
    'food_categories': ["italian", "pizza", "american", "kosher", "bbq", "hummus", "falafel", "vegan", "mediterannean", "sabich", "asian", "sushi", "thai"],
    'music_genre':["rock", "blues", "jazz", "rap", "hip hop", "classical", "electronic", "pop"]

}

emotion_animations={
    'afraid': ["bugs", "creepy", "afraid", "cockroaches", "guns", "shooting", "terrorist", "gunman", "kidnap"],
    'bored':["so boring", "I'm bored", "What should I do today?", "indoors"],
    'confused':["math", "problem set", "nuclear science", "biochem", "confused", "I don't get it"],
    'crying': ["tears", "break up", "ended things", "dog died", "cancer", "sick", "dead", "died", "suicide", "can't"],
    'dancing': ["music","song" , "beat", "jam", "spotify","rock", "blues", "jazz", "rap", "hip hop", "classical", "electronic"],
    'dog':["bestie", "best friend", "together", "animals", "companion", "dog", "puppy"],
    'excited':["birthday", "celebration", "so excited", "so happy"],
    'giggling':["snickering", "giggle", "ha"],
    'heartbroke':["over", "broken", "heartache", "heartbreak"],
    'laughing':["laughing", "cracking up", "so funny", "hilarious", "Sarah Silverman"],
    'money':["business", "currency", "trade", "dollars", "greed", "getting paper"],
    'no':["fuck","" "shit", "cunt","bitch", "bullshit", "asshole", "motherfucker", "shitface", "shithead"],
    'ok':["deal", "satisfied"],
    'takeoff':["plane", "flight", "travel", "trip", "launching", "launch"],
    "waiting":["wait", "delay", "be late", "loading", "to load"]


}

def get_animation(input):
    if any(input.find(s) >= 0 for s in emotion_animations['afraid']):
        return "afraid"
    elif any(input.find(s) >= 0 for s in emotion_animations['bored']):
        return "bored"
    elif any(input.find(s) >= 0 for s in emotion_animations['confused']):
        return "confused"
    elif any(input.find(s) >= 0 for s in emotion_animations['crying']):
        return "crying"
    elif any(input.find(s) >= 0 for s in emotion_animations['dancing']):
        return "dancing"
    elif any(input.find(s) >= 0 for s in emotion_animations['dog']):
        return "dog"
    elif any(input.find(s) >= 0 for s in emotion_animations['excited']):
        return "excited"
    elif any(input.find(s) >= 0 for s in emotion_animations['giggling']):
        return "giggling"
    elif any(input.find(s) >= 0 for s in emotion_animations['heartbroke']):
        return "heartbroke"
    elif any(input.find(s) >= 0 for s in emotion_animations['laughing']):
        return "laughing"
    elif any(input.find(s) >= 0 for s in emotion_animations['money']):
        return "money"
    elif any(input.find(s) >= 0 for s in emotion_animations['no']):
        return "no"
    elif any(input.find(s) >= 0 for s in emotion_animations['ok']):
        return "ok"
    elif any(input.find(s) >= 0 for s in emotion_animations['takeoff']):
        return "takeoff"
    elif any(input.find(s) >= 0 for s in emotion_animations['waiting']):
        return "waiting"


def greeting_function(message):
        message_list = message.split()
        if "is" in message:
            in_index = len(message_list) - 1 - message_list[::-1].index('is')
            if len(message_list) > in_index + 1:
                name = message_list[in_index + 1]
        return "Hey there {0}.What can I help you with today?".format(name)

def get_city(message):
    message_list = message.split()
    if "in" in message:
        in_index = len(message_list) - 1 - message_list[::-1].index('in')
        if len(message_list) > in_index+1:
            city = message_list[in_index+1]
        else:
            city = "Dallas"
        return city
    elif "of" in message:
        of_last_index = len(message_list) - 1 - message_list[::-1].index('of')
        if len(message_list) > of_last_index+1:
            city = message_list[of_last_index + 1]
        else:
            city = "Dallas"
        return city
    elif "for" in message:
        for_last_index = len(message_list) - 1 - message_list[::-1].index('for')
        if len(message_list) > for_last_index+1:
            city = message_list[for_last_index + 1]
        else:
            city = "Dallas"
        return city
    else:
        return "Dallas"

def get_weather(message):
    choose_city = get_city(message)
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'
                     .format(choose_city, "e3b24d902d335691023a8b85fe0f6f00"))
    weather_content = json.loads(r.content)
    temp = (weather_content['main']['temp'])
    humidity = (weather_content['main']['humidity'])
    description = (weather_content['weather'][0]['description'])
    weather_sentence = "The weather in {} is {} with a temp of {}C  and humidity of {}%"\
        .format(choose_city, description, temp, humidity)
    return weather_sentence

def get_jokes():
    r = requests.get('https://api.yomomma.info')
    parsed_joke = json.loads(r.content)
    return parsed_joke["joke"]

def get_news():
    if response_bank['articles'] is not None:
        return response_bank['articles'][randint(0, len(response_bank['articles']))]['title']

    else:

        r = requests.get('https://newsapi.org/v2/everything?'
           'q=Apple&'
           'from=2018-12-15&'
           'sortBy=popularity&'
           'apiKey=e9d65348e2c1407aa3dec727cb8874f5')
        parsed_r = r.json()
        response_bank['articles'] = parsed_r['articles']

    return get_news()


def vactaion_travel():
    new_list = response_bank['travel']
    shuffle(new_list)
    return "You should travel to {0} ".format(new_list[0])

def music_function(input):
        input = input.lower()
        music_list = response_bank['music_recs']
        request_list = questions_bank['music_genre']
        for i in range(len(request_list)):
            if request_list[i] in input:
                return "You would like to listen to {0}".format(music_list[i])


def food_rec_function(input):
        input=input.lower()
        new_list = response_bank['food_categories']
        q_list = questions_bank['food_categories']
        for i in range(len(q_list)):
            if q_list[i] in input:
                return "I would recommend {0}".format(new_list[i])

def talk_to_robot(input):
    message= input.lower()
    if any(input.find(s)>=0 for s in questions_bank['swear_word']):
        new_list = response_bank['swear_response']
        shuffle(new_list)
        return new_list[0]
    elif "food" in input or "restaurant" in input or "hungry" in input:
        return food_rec_function(input)
    elif any(input.find(s)>=0 for s in questions_bank['travel']):
        return vactaion_travel()
    elif "weather" in message or "temp" in message or "forecast" in message:
        return get_weather(message)
    elif "joke" in input:
        return get_jokes()
    elif " name " in message:
        return greeting_function(message)
    elif "song" in input or "music" in input or "beat" in input:
        return music_function(input)
    elif any(input.find(s)>=0 for s in questions_bank['greetings']):
        new_list = response_bank['greetings_response']
        shuffle(new_list)
        return new_list[0]
    elif "news" in input:
        return 'This just in: {0}'.format(get_news())
    else:
        return "Come Again? Please try something else."

test_sample = 'where should i travel to?'
print(talk_to_robot(test_sample))

# def travel_words(input)

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    print("chat received {}".format(user_message))
    return json.dumps({"animation": get_animation(user_message), "msg": talk_to_robot(user_message)})


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


