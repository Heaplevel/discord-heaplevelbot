import logging
from searchtweets import load_credentials, collect_results, gen_rule_payload
from collections import namedtuple

logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

premium_search_args = load_credentials(filename="./search_tweets_creds_example.yaml",
                 yaml_key="search_tweets_ent_example",
                 env_overwrite=False)

tweet = namedtuple('tweet', 'text screen_name')


def read_tweets(term):
    rule = gen_rule_payload(term, results_per_call=100) # testing with a sandbox account
    print(rule)
    tweets = collect_results(rule, 100, premium_search_args)
    print(tweets[:10])
    output = '\n\n'.join([f'@{t.screen_name}: {t.all_text}' for t in tweets[:10]])
    return output