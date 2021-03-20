from collections import namedtuple


def split_2000(message):
    if len(message) > 2000:
        n = 2000  # chunk length
        message = [message[i:i + n] for i in range(0, len(message), n)]
    else:
        message = [message]
    return message


tweet = namedtuple('tweet', 'text screen_name')
