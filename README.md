# Requirements

* yfinance
* discord.py


Heaplevel Github

## Credentials file should be at top-level 

The name for the credentials file is specified in 'helpers/helpers.py'
```
premium_search_args = load_credentials(filename="../search_tweets_creds_example.yaml",
                                       yaml_key="search_tweets_ent_example",
                                       env_overwrite=False)
                                       ```
