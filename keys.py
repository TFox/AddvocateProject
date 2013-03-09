import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

def createConfig():
    cfgfile = ConfigParser.ConfigParser()
    cfgfile.add_section('Twitter')
    cfgfile.set('Twitter', 'consumer_key', '')
    cfgfile.set('Twitter', 'consumer_secret', '')
    cfgfile.set('Twitter', 'access_key', '')
    cfgfile.set('Twitter', 'access_secret', '')
    cfgfile.add_section('SQL')
    cfgfile.set('SQL', 'host', '')
    cfgfile.set('SQL', 'user', '')
    cfgfile.set('SQL', 'passwd', '')
    cfgfile.set('SQL', 'dbid', '')
    cfgfile.add_section('Klout')
    cfgfile.set('Klout', 'key', '')
    with open('config.cfg', 'wb') as configfile:
        cfgfile.write(configfile)
def getSetting(section,setting):
    return config.get(section,setting)