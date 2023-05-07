AUTHOR = 'gbaru'
SITENAME = "gbaru's blog"
SITEURL = ''
AVATAR = '/theme/images/icons/avatar.png'
PATH = 'content'

TIMEZONE = 'Europe/Rome'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

SIDEBAR_DIGEST = 'Binary Exploitation Lessons'

MENUITEMS = (('Articles', '/'),
             ('Tags', SITEURL+'/tags/'))

# Social widget
SOCIAL = (('mail-128','mailto:blog.gbarut@riskreduction.net'),
          ('twitter', 'http://twitter.com/GanbaruTobi'),
          ('github', 'http://github.com/GanbaruTobi'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
