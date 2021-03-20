from collections import namedtuple
from searchtweets import load_credentials, gen_rule_payload, collect_results

premium_search_args = load_credentials(filename="./search_tweets_creds_example.yaml",
                                       yaml_key="search_tweets_ent_example",
                                       env_overwrite=False)


def read_tweets(term):
    """
    @return: string output split into 2000 messages.
    """
    rule = gen_rule_payload(term, results_per_call=100)  # testing with a sandbox account
    print(rule)
    tweets = collect_results(rule, 100, premium_search_args)
    print(tweets[:10])
    output = '\n\n'.join([f'@{t.screen_name}: {t.all_text}' for t in tweets[:10]])
    output = split_2000(output)
    return output


def split_2000(message):
    if len(message) > 2000:
        n = 2000  # chunk length
        message = [message[i:i + n] for i in range(0, len(message), n)]
    else:
        message = [message]
    return message


tweet = namedtuple('tweet', 'text screen_name')
