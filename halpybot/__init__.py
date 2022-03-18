from halpybot.packages.configmanager import config

__version__ = "1.5.3"

DEFAULT_USER_AGENT = "HalpyBOT/" + __version__ + " (" + config['IRC']['nickname'] + ") "\
                     + config['UserAgent']['agent_comment']
