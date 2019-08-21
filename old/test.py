import ConfigParser
config=ConfigParser.ConfigParser()

config.read('config/airlines.cfg')

print config.get('DEFAULT','filteredcountries').replace('\n','').split(",")

#print config.get('DEFAULT','filteredhexcodes').replace('\n','').split(",")

#print config.get('DEFAULT','filteredhexcodes').replace('\n','').split(",")
#print config.get('DEFAULT','filteredhexcodes').replace('\n','').split(",")
#print config.get('DEFAULT','filteredhexcodes').replace('\n','').split(",")

