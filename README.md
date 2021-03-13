
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

## Overview
This GUI application will allow the user to access 3 top charts on the Rolling Stones website. We use web scraping to get the data, store it in a database, and then from there the user can interact with the GUI to display the data in whatever sorted way they like.

## Samples from the database
Here we display the top 1 item from each table.

### Top 200 Albums
| Album Title | Artist Name | Record Label | Album Units | Album Sales | Song Sales | Song Streams |
| --- | --- | --- | --- | --- | --- | --- |
| Dangerous: The Double Album | Morgan Wallen | Republic | 51.2K | 2.8K | 8.3K | 59.6M |

### Top 100 Songs
| Song Title | Artist Name | Song Units | Song Streams | Weeks on Chart |
| --- | --- | --- | --- | --- |
| What’s Next | Drake | 293.1K | 34.7M | 1 |

### Top Artist 500
| Artist Name | Song Streams (default ranking) | Weeks on Chart | Top Song |
| --- | --- | --- | --- |
| Drake | 167.7M | 317 | What’s Next |

## What are the sizes of the tables? 
Top 200 Albums: 200 with 7 fields
Top 100 Songs: 100 with 5 fields
Top Artist 500: 500 with 4 fields

## Flow Logic
Top 200 album -> Pick search filters -> display ranking

Top 100 songs -> Pick search filters -> display ranking

Top 500 artists -> Pick search filters -> display ranking

```
|-- Start: Rolling Stone Charts
    |
    |-- Choice 1: Look at top 200 albums
    |    |-- Choice 1.1: Default - show by ranking (album units)
    |    |    |-- Displays the listbox of all the album names in the order of Rolling Stone’s ranking
    |    |
    |    |-- Choice 1.2: Sort by record label
    |    |    |-- Opens another page where the user can select from a list of record labels 
    |    |         Once they do, a LB will show the top albums within that record label
    |    |
    |    |-- Choice 1.3: Sort by album sales
    |    |    |-- Displays a listbox of album names ranked by the number of album sales
    |    |
    |    |-- Choice 1.4: Sort by song sales
    |    |    |-- Displays a listbox of album names ranked by the number of songs sold
    |    |
    |    |-- Choice 1.5: Sort by song streams
    |    |    |-- Displays a listbox of album names ranked by the number of song streams
    |
    |-- Choice 2: look at top 100 songs
    |    |-- Choice 2.1: Top 100
    |    |    |-- List top 100 songs by rank (song units)
    |    |          
    |    |-- Choice 2.2: Compare weeks on chart
    |    |    |-- Compares user selected artists’ weeks on chart in a bar chart
    |    |
    |    |-- Choice 2.3: Compare sale units
    |    |    |-- Compares user selected songs sales in a bar chart
    |
    |-- Choice 3: look at top 500 artists
        |-- Choice 3.1: By ranking (song streams)
        |    |-- Displays artists names in listbox sorted by ranking (song streams)
        |
        |-- Choice 3.2: Weeks on chart
        |    |-- Compares artists’ weeks on chart in bar chart
        |
        |-- Choice 3.3: By # of streams
             |-- Compares user-selected artists’ # of streams in bar chart
```
