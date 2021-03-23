
<div>
  <p align="center">
    <img width="300" src="https://cdn.worldvectorlogo.com/logos/rolling-stone-1.svg"></img>
  </p>
  <h1 align="center">
    Application to display chart data from RollingStone Magazine
  </h1>
</div>

Final Project for Nguyen CIS41B Winter 2021. 

Authors: [Fawaz Al-Harbi](https://github.com/monsieurCat), [Kaede Hamada](https://github.com/KaeMaple9), and [Jacqueline Nguyen](https://github.com/jacquelinennguyen).

## 🎶 Overview
>***UPDATE 3/23/2021***
> Upon first opening the GUI application, the user will have to select the week they want to get the data from. After the user locks their choice, the GUI makes 2 calls: one to the backendWebScraper and one to update the database. This call will web scrape and update the  database. After that happens, then the user is allowed to access the 3 top charts. We thought this would make more sense so the user isn't making too many calls to the web scraper in one session. 
>
> We also decided on using GitHub (we know you said to do it after) because it made it easier for us to share our code and work on different features simultaneously. Fawaz and Kaede will probably upload a copy to their GitHubs after we submit this final if they choose to do so.
>***end of update***

This GUI application will allow the user to access 3 top charts on the Rolling Stones website. We use web scraping to get the data, store it in a database, and then from there the user can interact with the GUI to display the data in whatever sorted way they like.

The Top 200 Albums and Top 100 Songs charts on the Rolling Stones website that we used here are sorted by a weighted Units score that accounts for sales and streams for that particular item. So the AlbumsDB Table in our database is sorted by default by the Album Units and the SongsDB Table is sorted by the Song Units.

As for the Top 500 Artists table, that table is sorted by the number of total streams the artists have accumulated.

To view any of the tables used in this application, click [here](https://www.rollingstone.com/charts/).

## 🎶 Contents

|--🎸  **`Media`** - images

|--🎸  **`backendWebScraper.py`** - gets all the data from 3 Top charts from the Rolling Stones website

|--🎸  **`backendDB.py`** - converts the dictionaries from backendWebScrapper into a SQL database

|--🎸  **`backendQuery.py`** - functions that make SQL queries for the sorting aspect of the program

|--🎸  **`weeks.py`** - Script to get all of the available input weeks that Rolling Stones will let you webscrape from

|--🎸  **`GUI.py`** - frontend of the program

|--🎸  **`rollingstones.db`** - Contains 4 Tables (Top 500 Artists, Top 200 Albums, Top 100 Songs, Artist Name Keys). Pictured below.

## 🎶 Samples from the database
Here we display the top 1 item from each table. (As of Friday, March 19)

### Top 200 Albums
| Album Title | Artist ID | Album Sales | Song Sales | Peak Position | Weeks on Chart | Top 3 Songs | Record Label | Song Streams |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dangerous: The Double Album | 1 | 2.8K | 8.3K | 1 | 11 | Wasted on You, Sand in My Boots, More Than My Hometown | Republic | 65000000 |

### Top 100 Songs
| Song Title | Artist ID | Units Trend | Peak Position | Label | Top Cities | Weeks on Chart | Streams |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Wants and Needs | 31 | [["2021-02-26 00:00:00.000",12340],["2021-03-05 00:00:00.000",321132],["2021-03-12 00:00:00.000",140674]] | 1 | Republic/Cash Money | 1 New York, NY 2 Los Angeles, CA 3 Chicago, IL | 2 | 17600000 |

### Top Artist 500
| Artist Name | Song Streams (default ranking) | Weeks on Chart | Top Song |
| --- | --- | --- | --- |
| Drake | 137700000 | 318 | What’s Next |

### Artist Names
| Artist Name | ID |
| --- | --- |
| Morgan Wallen | 1 |
| Pop Smoke | 2 |

## 🎶 What are the sizes of the tables? 
* **`Top 200 Albums`**: 200 with 9 fields
* **`Top 100 Songs`**: 100 with 8 fields
* **`Top Artist 500`**: 500 with 4 fields

## 🎶 Flow Logic
### Graphic Representation
* *Top 500 Artists and Top 100 Songs will also have an option to display rankings graphically (Weeks on Chart).*
* *These are only samples to illustrate the flow of our program. They do not represent the final UI of our program.*
![](https://i.imgur.com/g335cyp.png)

### More detailed structure
This is from the Project Proposal
```
|-- Start: Rolling Stones Charts
    |-- Select week (this is the first thing the user is asked to do.)
    |-- Choice 1: Look at top 100 songs
    |    |-- Choice 1.1: Default - shows the default ranking, ranked by song units
    |    |    |-- List top 100 songs by rank (song units)
    |    |          
    |    |-- Choice 1.2: Weeks on Chart - compares the selected songs’ weeks on chart in a bar chart
    |    |    |-- Compares user selected songs’ weeks on chart in a bar chart
    |    |
    |    |-- Choice 1.3: Song Units - compares the selected songs’ song units in a bar chart
    |         |-- Compares user selected songs' sales in a bar chart
    |
    |-- Choice 2: Look at top 200 albums
    |    |-- Choice 2.1: Default - shows the default ranking, ranked by album units
    |    |    |-- Displays the listbox of all the album names in the order of Rolling Stone’s ranking
    |    |
    |    |-- Choice 2.2: Album Sales - shows album names ranked by the number of album sales
    |    |    |-- Displays a listbox of album names ranked by the number of album sales
    |    |
    |    |-- Choice 2.3: Song Sales - shows album names ranked by the number of songs sales
    |    |    |-- Displays a listbox of album names ranked by the number of songs sales
    |    |
    |    |-- Choice 2.4: Song Streams - shows album names ranked by the number of song streams
    |    |    |-- Displays a listbox of album names ranked by the number of song streams
    |    |
    |    |-- Choice 2.5: Top Albums of Labels - shows the top albums within the selected record labels based on album units
    |         |-- Opens another page where the user can select from a list of record labels 
    |             Once they do, a LB will show the top albums within that record label
    |    
    |
    |-- Choice 3: Look at top 500 artists
        |-- Choice 3.1: Default - shows the default ranking, ranked by song streams
        |    |-- Displays artists names in listbox sorted by ranking (song streams)
        |
        |-- Choice 3.2: Weeks on Chart - compares the selected artists’ weeks on chart in bar chart
        |    |-- Compares artists’ weeks on chart in bar chart
        |
        |-- Choice 3.3: Song Streams - compares the selected artists’ song streams in bar chart
             |-- Compares user-selected artists’ # of streams in bar chart
```
