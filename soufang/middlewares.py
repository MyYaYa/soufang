import random
import base64
from .settings import USER_AGENTS

class RandomUserAgentMiddleware(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def process_request(self, request, spider):
        agent = random.choice(USER_AGENTS)
        # print("**************************" + agent)
        request.headers.setdefault('User-Agent', agent)

class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = "http://45.76.150.178:5552"
        encoded_user_pass = base64.b64encode(b'fangchan:Boyiding123')
        request.headers['Proxy-Authorization'] = b'Basic ' + encoded_user_pass
        # print(request.headers['Proxy-Authorization'])
