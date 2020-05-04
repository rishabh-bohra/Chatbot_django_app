from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from chatbot import Chat, reflections, multiFunctionCall
import requests, os
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation
from bs4 import BeautifulSoup


def whoIs(query, sessionID="general"):
    if query[-2] == '?':
        query = query[:len(query)-2]
    try:
        response = requests.get('http://api.stackexchange.com/2.2/tags/' + query + '/wikis?site=stackoverflow')
        data = response.json()
        return data['items'][0]['excerpt']
    except:
        pass
    return "Oh, You misspelled somewhere!"


def results(query, sessionID="general"):
    query_list = query.split(' ')
    query_list = [x for x in query_list if x not in ['posted', 'questions', 'recently', 'recent', 'display', '', 'in', 'of', 'show']]
    # print(query_list)
    if len(query_list) == 1:
        # print('con 1')
        try:
            response = requests.get('https://api.stackexchange.com/2.2/questions?pagesize=5&order=desc&sort=activity&tagged=' + query_list[0] + '&site=stackoverflow')
            data = response.json()
            data_list = [str(i+1)+'. ' + data['items'][i]['title'] for i in range(5)]
            return '<br/>'.join(data_list)
        except:
            pass
    elif len(query_list) == 2 and 'unanswered' not in query_list:
        # print('con 2')
        query_list = sorted(query_list)
        n = query_list[0]
        tag = query_list[1]
        try:
            response = requests.get('https://api.stackexchange.com/2.2/questions?pagesize='+ n +'&order=desc&sort=activity&tagged=' + tag + '&site=stackoverflow')
            data = response.json()
            data_list = [str(i+1)+'. ' + data['items'][i]['title'] for i in range(int(n))]
            return '<br/>'.join(data_list)
        except:
            pass

    else:
        # print('con 3')
        query_list = [x for x in query_list if x not in ['which', 'where', 'whos', 'who\'s' 'is', 'are', 'answered', 'not', 'unanswered', 'for']]
        # print(query_list)
        if len(query_list) ==1:
            try:
                response = requests.get(
                    'https://api.stackexchange.com/2.2/questions/no-answers?pagesize=5&order=desc&sort=activity&tagged=' + query_list[0] + '&site=stackoverflow')
                data = response.json()
                data_list = [str(i+1)+'. ' + data['items'][i]['title'] for i in range(5)]
                return '<br/>'.join(data_list)
            except:
                pass
        elif len(query_listint) == 2:
            query_list = sorted(query_list)
            n = query_list[0]
            tag = query_list[1]
            try:
                response = requests.get(
                    'https://api.stackexchange.com/2.2/questions/no-answers?pagesize='+ n +'&order=desc&sort=activity&tagged=' + tag + '&site=stackoverflow')
                data = response.json()
                data_list = [str(i+1)+'. ' + data['items'][i]['title'] for i in range((n))]

                return '<br/>'.join(data_list)
            except:
                pass
    return "Oh, You misspelled somewhere!"


#Display recent 3 python questions which are not answered
firstQuestion = "Hi, How may i help you?"

call = multiFunctionCall({"whoIs": whoIs,
                              "results": results})

chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "chatbotTemplate",
                         "Example.template"
                         ),
            reflections, call=call)


def Home(request):
    return render(request, "alpha/home.html", {'home': 'active', 'chat': 'chat'})


@csrf_exempt
def Post(request):
    while len(chat.conversation["general"])<2:
        chat.conversation["general"].append('initiate')
    if request.method == "POST":
        query = request.POST.get('msgbox', None)
        response = chat.respond(query)
        chat.conversation["general"].append('<br/>'.join(['ME: '+query, 'BOT: '+response]))
        if query.lower() in ['bye', 'quit', 'bbye', 'seeya', 'goodbye']:
            chat_saved = chat.conversation["general"][2:]
            response = response + '<br/>' + '<h3>Chat Summary:</h3><br/>' + '<br/><br/>'.join(chat_saved)
            chat.conversation["general"] = []
            return JsonResponse({'response': response, 'query': query})
        #c = Conversation(query=query, response=response)
        return JsonResponse({'response': response, 'query': query})
    else:
        return HttpResponse('Request must be POST.')


'''
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(message=msg)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': 'user'})
    else:
        return HttpResponse('Request must be POST.')'''

@csrf_exempt
def rail_info(request):
    if request.method == "POST":
        try:
            pnr=request.POST.get("chat-msg")
        #     return JsonResponse({'response': pnr})
        # else:
        #     return HttpResponse('Request must be POST.')

            url1 = 'https://www.travelkhana.com/travelkhana/PNRresult?pnr={}'.format(pnr)
            headers = {

                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'

            }
            data = {
                "dataTime": 1571296566808,
                "eventType": "train_pnr_submitted",
                "appVersion": "1.0.0",
                "customerId": "",
                "payload": {"event_category": "train_pnr",
                            "event_action": "train_pnr_submitted",
                            "event_layer": "2202587451",
                            "train_pnr_number": "2202587451",
                            "user_id": "",
                            "event": "train_pnr_submitted",
                            "vertical_name": "trains",
                            "gtm.uniqueEventId": 65},
                "deviceId": '',
                "messageVersion": 1

            }

            response = requests.get(url1)
            doc = BeautifulSoup(response.text, "html.parser")
            row1 = []
            row2 = []
            row = doc.find('td', {"class": 'text-center'})
            for my_tag in doc.find_all(class_="hidden-xs"):
                row1.append(my_tag.text.strip())
            for el in doc.find_all('ul', {"class": 'dept-tabel PNR-info'}):
                for li in el.find_all(class_='dept-head'):
                    li.decompose()
                for li in el.find_all('li'):
                    row2.append(li.text.strip())
            user_info = {
                'pnr_details':
                    {
                        "Name": row.text,
                        "Current-statuts": row1[4],
                        "PNR": row2[0],
                        "Train": row2[1],
                        "From": row2[2],
                        'To': row2[3],
                        'On': row2[4],
                        'Coach-Class': row2[5]}
                    }
        except:

            user_info = {
                'pnr_details':
                    {
                        "Name": 'ritik',
                        "Current_status": 'confirmed',
                        "PNR": pnr,
                        "Train": 'rajdhani express' ,
                        "From": 'mumbai',
                        'To': 'jaipur',
                        'On': '2 may 2020',
                        'Coach_Class': 'sleeper'}
                    }
        return render(request, 'alpha/base.html', user_info)
    else:
        return HttpResponse('Request must be POST.')

