import pprint
import praw

app_ua='/u/ecrunch'

app_id='cLS9zPhdNBwckw'
app_secret='NHz6jb_qUYBZ5nCRXlnftC0WcFQ'
app_uri='https://127.0.0.1:65010/authorize_callback'

app_refresh =''

app_account_code = 'PtBD5My18hz-cIwbbCEYZnyyfjw'
app_scopes = 'account creddits edit flair history identity livemanage modconfig modcontributors modflair modlog modothers modposts modself modwiki mysubreddits privatemessages read report save submit subscribe vote wikiedit wikiread'


def login():
    r = praw.Reddit(app_ua)
    return r