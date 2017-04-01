import bookgen
from BotBuddy import BotBuddy

credentials = {
    
    BotBuddy.consumer_key_key : "W8mx3eg7mA4J8pZjSE3gkPplN",
    BotBuddy.consumer_secret_key : "iHh2ZWXcTrRtbToTV8q1QdkdsEZ9KIjsN7RgonfzOsyheyZkjt",
    BotBuddy.access_token_key : "798422658425778176-at7rlU1vIugbbZ3hvvVIVLXvV93tNKB",
    BotBuddy.access_token_secret_key : "N7ZlfS2yVI3JFNsO0osPz6VewV4KVXS6O0mhy9nCvFHKi"
}
    
body = BotBuddy()
body.setup(bookgen.write_tweet, interval="1h", retry=True, credentials=credentials)
body.launch()