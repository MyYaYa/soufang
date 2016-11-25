import random
from .settings import USER_AGENTS

class RandomUserAgentMiddleware(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def process_request(self, request, spider):
        agent = random.choice(USER_AGENTS)
        print("**************************" + agent)
        request.headers.setdefault('User-Agent', agent)
