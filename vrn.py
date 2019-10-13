import json
import http.client

# FIXME: move to a config file
server = 'www.st-petersburg.vybory.izbirkom.ru'
target = '/region/st-petersburg?'


# FIXME: make it async
def request(params):
    global server
    global target

    cx = http.client.HTTPConnection(server)
    cx.request('GET', target + '&'.join(('%s=%s' % x for x in params.items())))
    # FIXME: get encoding from the headers
    data = json.loads(cx.getresponse().read().decode('cp1251'))
    cx.close()
    return data


def get_index():

    # FIXME: get the root vrn from the real index
    params = {'action': 'ikTree',
              'region': '78',
              'vrn': '27820001006425',
              'id': '%23'}

    index = request(params)
    for tik in index[0]['children']:
        params = {'action': 'ikTree',
                  'region': '78',
                  'vrn': tik['id'],
                  'onlyChildren': 'true',
                  'id': tik['id']}
        for ik in request(params):
            if 'id' and 'text' in ik:
                print('%s, "%s"' % (ik['id'], ik['text'].replace('"', "'")))


get_index()
