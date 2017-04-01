import bookgen
from botbuddy import BotBuddy

credentials = {
    BotBuddy.creds_file_key : "creds.json"
}
    
body = BotBuddy()
body.setup(bookgen.write_tweet, interval="1h", retry=True, credentials=credentials)
body.launch()