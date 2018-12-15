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
    'food_categories': ["italian", "pizza", "american", "kosher", "bbq", "hummus", "falafel", "vegan", "mediterannean", "sabich", "asian", "sushi", "thai"],
    'music_recs':["music","song" , "beat", "jam", "spotify","rock", "blues", "jazz", "rap", "hip hop", "classical", "electronic"],


}






def greeting_function(name):
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

# def jokes_function():
 #   r =requests.get('https://antijokes.paineleffler.com')




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

#not working
def vactaion_travel(input):
    print("working")




# need q mark
# iteration not working
def food_rec_function(input):
        input=input.lower()
        if "food" in input or "restaurant" in input or "hungry" in input:
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
    elif any(input.find(s)>=0 for s in questions_bank['food_categories']):
        return food_rec_function(input)
    elif any(input.find(s)>=0 for s in questions_bank['travel']):
        return vactaion_travel(input)
    elif "weather" in message or "temp" in message or "forecast" in message:
        return get_weather(message)

    else:
        return greeting_function(input)




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


