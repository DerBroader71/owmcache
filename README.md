# owmcache
Local network cache for OpenWeatherMap

Having many devices displaying weather information around my house has led to me occasionally exceeding my API limits when testing.

To this end, I have implemented an endpoint on a device in my home that gets the data from OpenWeatherMap, once every 15 minutes and then serves it up to any clients that request it.

main.go is written in Golang  
main.py is written in CPython (or Python to normal people)

Before using/compiling, ensure your latitude, longitude and API KEY are edited  

The CPython version has additional endpoints to cater for memory constrained devices:  
/ - provides the full response from OpenWeatherMap  
/short - provides a reduced response (sans daily, minutely and alerts)  
/current - provides just the current weather  
/hour/X - provides the weather for X hour(s) in the future. X must be an number between 1 and 47. For example, a request made at 10:34 to /hour/3 would provide the weather for 13:00. 
