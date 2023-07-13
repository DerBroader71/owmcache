// OWMCache
// Package that implements the a caching mechanism for openweathermap API

package main

import (
        "fmt"
        "io/ioutil"
        "log"
        "net/http"
        "time"
        "github.com/gin-gonic/gin"
        "github.com/robfig/cron/v3"
)

func main() {
        fmt.Println("OWM Cache Server: ", time.Now().Format(time.RFC3339))
        fmt.Println("Waiting to answer requests")

        // Run owmcache on startup
        owmcache()

        // Start a cron job to refresh the data every 15 minutes
        c := cron.New()
        c.AddFunc("@every 15m", owmcache)
        c.Start()

        // Setup the gin-gonic environment
        gin.SetMode(gin.ReleaseMode)
        r := gin.Default()
        r.SetTrustedProxies(nil)

        // Define the endpoint
        r.GET("/", genOWM)

        // Start an HTTP server on port 8080
        r.Run()
}

// Config for OpenWeatherMap
// CHANGE THESE
const LAT = ""
const LON = ""
const OPENWEATHERMAP_API_KEY = ""

// Set up constants and global variables
const ONE_HIT_URL = "https://api.openweathermap.org/data/2.5/onecall?lat=" + LAT + "&lon=" + LON + "&units=metric&appid=" + OPENWEATHERMAP_API_KEY
var owmCacheData string

// Function for owmcache (openweathermap cache)
func owmcache() {
        resp, err := http.Get(ONE_HIT_URL)
        if err != nil {
                log.Fatal(err)
        }
        defer resp.Body.Close()
        data, err := ioutil.ReadAll(resp.Body)
        if err != nil {
                log.Fatal(err)
        }
        //fmt.Println(string(data))
        fmt.Println("Got data from OWM")
        owmCacheData = string(data)
}

// Function to return the cached data when requested
func genOWM(c *gin.Context) {
        c.String(http.StatusOK, owmCacheData)
}
