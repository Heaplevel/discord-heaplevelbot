import logging
from searchtweets import load_credentials, collect_results, gen_rule_payload

logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

premium_search_args = load_credentials(filename="./search_tweets_creds_example.yaml",
                 yaml_key="search_tweets_ent_example",
                 env_overwrite=False)


def read_tweets(term):
    rule = gen_rule_payload(term, results_per_call=100) # testing with a sandbox account
    print(rule)
    tweets = collect_results(rule, 100, premium_search_args)
    return tweets[:10]
