# This Ale's For You!
<strong>An exploration of the DC/Maryland/Virginia (DMV) beer scene and a beer recommender system</strong>

## Executive Summary

### Introduction
Imagine you're sitting at a bar trying to figure out what to drink next...the bartender is too busy dealing with the mobs of people at the other end of the bar but you could really use some help choosing a beer. As a homebrewer, I'm often the person trying to give suggestions, but can I build a recommender system to save me time and energy?

### Problem Statements 
* Explore the DC/MD/VA (DMV) beer scene
* Build beer recommender(s)
  - Content: based on styles and other attributes
  - Content: based on textual analysis of reviews
  - Collaborative: based on user reviews
  - Content: textual and able to accept general queries
* Can we classify good beers? Or beer style categories?

## Data Gathering

#### The Universe of Beer Reviews and Beer-Related Databases

There is a bevy of beer review data on the Internet. Some of the main beer review website/applications include: 
* [BeerAdvocate](https://www.beeradvocate.com) 
* [RateBeer](https://www.ratebeer.com)
* [Untappd](https://untappd.com/home)

Additionally, there are more specialized Beer-focused publications that include reviews, typically with a more limited selection of esoteric or limited-release beers:
* [The Beer Connoiseur](https://beerconnoisseur.com)
* [Craft Beer and Brewing](https://beerandbrewing.com)
* [The Full Pint](https://thefullpint.com/beer-reviews/)
* [All About Beer](http://allaboutbeer.com)
* [Draft Magazine](https://draftmag.com)

General brewery databases:
* [Open Brewery DB](https://www.openbrewerydb.org)
* [BreweryDB](https://www.brewerydb.com/developers)

Both [RateBeer](https://www.ratebeer.com/api-documentation.asp) and [Untappd](https://untappd.com/api/register#) have developer APIs, but both require explicit approval for API keys. Untappd in particular places restrictions on API access for pure research and analytics purposes. Given the turnaround time for API key access, I'm relying heavily on web scraping, which is not explicitly prohibited per each website's Robots Exclusion Protocol page. I have avoided scraping BeerAdvocate given reports of the owner's proclivity towards legal action against prior web scrapers.

In addition to scraping beer review data, I also tried to incorporate data from the very cool beer databases [Open Brewery DB](https://www.openbrewerydb.org) and [BreweryDB](https://www.brewerydb.com).

#### Beer Style Guidelines

* [BJCP](https://www.bjcp.org/docs/2015_Guidelines_Beer.pdf)
* [Brewers Association](https://www.brewersassociation.org/press-releases/brewers-association-releases-2019-beer-style-guidelines/)

I also consulted the leading beer style guidelines. At first, I considered maybe this could be a source of features for the model, but given the diversity of beers even within the same style category, the style guides themselves were not helpful except for aiding in manual mapping of beers to broader categories.

As is the adage in data science, data gathering took up a majority of my time on this project to date. Given that the data had to be scraped rather than called via an API, this took a little bit of persistence and creativity. RateBeer's website uses a fair bit of 

## Conclusions / Further Improvements

Scraping over 100,000 beer reviews was probably what I'm most proud about in this project.

Additionally, I was able to create multiple variations of recommender systems with certain pros/cons:
* Content - style / ABV / review counts etc. 
    - This gives you very similar beers (i.e. pale lagers with pale lagers)
* Review Content - NLP analysis of review text
    - My favorite version though also tilts towards similarity vs. interesting suggestions
* Collaborative - Based on user ratings
    - Not terribly interesting; despite pulling a large body of reviews, there are many users that haven't rated a significant number of beers in the dataset

Unfortunately, I've had a bit of a technical snafu at the last minute and in my desperation to get a working demo, some of the organization and functionality stopped working recently. I'm working to fix the basic functionality asap.

Additionally, I'd like to explore further the possibility of using Doc2Vec on the review text to make more general recommendations (not require a starting beer as comparison).

I'd like to deploy the model and dataset as a web app with Flask. Hopefully the web application can also include cool funtionality, including links to the breweries, directions, graph of key words, and more filtering options.

At this stage the beer journey continues ...