# owmcache
Local network cache for OpenWeatherMap

Having many devices displaying weather information around my house has led to me occasionally exceeding my API limits when testing.

To this end, I have implemented an endpoint on a device in my home that gets the data from OpenWeatherMap, once every 15 minutes and then serves it up to any clients that request it.

This first release is in Go but versions for Python and CircuitPython are in the works.

Before using/compiling, ensure your latitude, longitude and API KEY are edited
