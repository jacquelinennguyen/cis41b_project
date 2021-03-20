
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
This GUI application will allow the user to access 3 top charts on the Rolling Stones website. We use web scraping to get the data, store it in a database, and then from there the user can interact with the GUI to display the data in whatever sorted way they like.

## 🎶 Contents
🎸 Media - images

🎸 backendWebScraper - gets all the data from 3 Top charts from the Rolling Stones website

🎸 backendDB - converts the dictionaries from backendWebScrapper into a SQL database

🎸 GUI.py - frontend of the program

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
* **`Top 200 Albums`**: 200 with 7 fields
* **`Top 100 Songs`**: 100 with 7 fields
* **`Top Artist 500`**: 500 with 4 fields

## 🎶 Flow Logic
### Graphic Representation
* *Top 500 Artists and Top 100 Songs will also have an option to display rankings graphically (Weeks on Chart).*
* *These are only samples to illustrate the flow of our program. They do not represent the final UI of our program.*
![](https://i.imgur.com/g335cyp.png)

### More detailed structure
This is from the Project Proposal
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
