# flightscraper

This is a quick-and-dirty hack to pull flight schedule information for Cape Town airport.

I wanted to webscrape the info that I found here: https://capetown-airport.co.za/flights/arrivals/
but it turns out this is a request to a standard widget on flightstats.com.  I think that this
is using the API key that was probably purchased by the capetown-airport.co.za devs, so please
don't abuse this.

The code will work for any IATA airport code, but needs some improvements...

- the widget returns a three hour window of either arrivals or departures.  So the scraper
  runs 16 times (once for arrivals, once for departures for each of the 8 x 3-hour blocks in
  a 24-hour day).
- it doesn't sort the stuff by time...
- it should extract the remote IATA code for each flight.
- I have figured out that flights with a '^' after the flight number are codeshare flights
  and this should be indicated in the CSV output.
  
  ...any other ideas?
