import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read('.env')

XX, OO = 'X', 'O'
if config.has_section('pieces'):
    XX, OO = config.get('pieces', 'xx'), config.get('pieces', 'oo')

