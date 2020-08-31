# MTG API
Christopher W. Evans, 2020

An API to retrieve the up to date play data of MTG cards in pro play. A client to view the data can be found http://mtgclient.chriswevans.com

Powered by NGINX and Flask.

There are two parts to the API: 
 - The Service hosted at http://mtgapi.chriswevans.com
 - The Data Management Module the module docs hosted here

## Server and API Reference

The server is Flask and MySQL. The API root is http://mtgapi.chriswevans.com.

#### `Card` JSON
```
{
  "id": < integer >,
  "title": < title >,
  "release_date": < date >,
  "rotation_date": < date >,
  "set": "/set/< set abbreviation >/< set name>/",
  "rarity": < card rarity >
}
```

#### `Plays` JSON
```
{
  "tot_occ":{
    < unix date > : < integer >, // Total number of occurances that day, capped at top 16 decks per event
    ...
  }, 
  "deck_nums":{
    < unix date > : < integer >, // Total number of decks played that day, capped at 16 per event.
    ...
  },
  "norm_occ":{
    < unix date > : < floating point>, // Number of occurances scaled by number of decks played 
    ...
  }

}
```

--------

#### `/search/cards/< search term >`

&nbsp;&nbsp;&nbsp;&nbsp; Search for cards by title.

_Parameters_: search term - <string> A term to search by.

_Returns_: <JSON>Array of <JSON> `Card` 

  

--------

#### `/card/< cardname >`

&nbsp;&nbsp;&nbsp;&nbsp; Get the card information of a specific card by title.

_Parameters_: cardname - <string> The exact title of the desired card.

_Returns_: <JSON> `Card` 

  

--------

#### `/cards`

&nbsp;&nbsp;&nbsp;&nbsp; Get all cards.

_Returns_: <JSON> Array of <JSON> `Card`


--------

#### `/df/plays/< id >/< format >`

&nbsp;&nbsp;&nbsp;&nbsp; Get card play data formatted from a Python dataframe.

_Parameters_: 
 - id - <integer> The id of the desired card.
 - format - <string> The event format ("standard", "modern", "pioneer"). Leave blank for aggregate of all three.

_Returns_: <JSON>`Play`


--------

## The Data Management Module

The module API reference can be found at http://mtgdocs.chriswevans.com

__Gathers events that have happened since last collected__

__Collects tallies play data for each rare and mythic card appearance and writes it to Database__

![Script Running](https://raw.githubusercontent.com/ChrisWeldon/MTG-Database-API/master/docs/images/Lots%20of%20data.png?token=AEYN33YYBYIMN72FLMHLAK27K2VSU)

