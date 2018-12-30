import bookgen
from botbuddy import BotBuddy

credentials = {
    BotBuddy.creds_file_key : "creds.json"
}
    
buddy = BotBuddy()
buddy.setup(bookgen.write_tweet, retry=True, credentials=credentials)
buddy.post()
