# ReelTracker CLI

## Summary

In today's streaming landscape, users face information overload with thousands of movies and TV shows spread across multiple platforms like Netflix, Disney+, etc. Many struggle to keep track of what they want to watch, often relying on messy notes, memory, or scattered lists across different apps. A [recent survey](https://nypost.com/2024/12/19/lifestyle/why-its-so-hard-to-find-something-to-watch-lately/) revealed that people spend an average of 110 hours a year just searching for content, while 51% feel overwhelmed by excessive recommendations. Additionally, growing [privacy concerns](https://www.thetimes.com/uk/technology-uk/article/how-to-stop-smart-tv-spying-on-you-pzfxx7mr8) around smart TVs and streaming services highlight the need for user-controlled, non-intrusive tracking tools.

Reel Tracker CLI is a lightweight, command-line-based personal watchlist manager designed for movie lovers, binge-watchers, film critics, and streaming enthusiasts. It helps users save and organize their watchlists, track watched content, and provide ratings and recommendations—all without intrusive data collection or algorithmic manipulation. By offering a privacy-focused, efficient, and customizable alternative to mainstream tracking apps, Reel Tracker CLI appeals to tech-savvy, data-conscious users who prefer self-managed solutions. The project also has potential for future expansion, including a front-end interface, user authentication, and database integration, making it valuable for market researchers and content licensing professionals as well.

More details at [#1](https://github.com/larevolucia/reeltracker_cli/issues/1)

Deployed at [Heroku](https://reeltrackercli-ff0190b86239.herokuapp.com/)
Titles Data available for read at [Google Sheets](https://docs.google.com/spreadsheets/d/1t0eogZL-QBFHBdLL0oipMXqyZ8MA3sZ8TJJPvrBvdYk/edit?usp=sharing)

## Project Goals
1. Address Information Overload in Entertainment
2. Develop a Personal Watchlist Tracker
3. Cater to Target Users with a CLI-Based Solution
4. Focus on Privacy and User-Controlled Data
5. Build a Scalable and Expandable Tool

## User Goals
1. Effortless Watchlist Management
2. Track Viewing History Easily
3. Make Better Viewing Choices
4. Stay in Control of Their Data & Privacy
5. Optimize Their Viewing Experience Across Multiple Platforms

## User Stories

### Must Have (MVP)
- [As a user, I want to search for a title so that I can find relevant information.](https://github.com/larevolucia/reeltracker_cli/issues/3)
- [As a user, I want to add a title to my Watchlist or Viewing History so that I can track what I plan to watch or have already watched.](https://github.com/larevolucia/reeltracker_cli/issues/4)
- [As a user, I want to view my Watchlist or Viewing History so that I can review the titles I saved or watched.](https://github.com/larevolucia/reeltracker_cli/issues/5)
- [As a user, I want to remove a title from my Watchlist or Viewing History so that my lists remain accurate and updated.](https://github.com/larevolucia/reeltracker_cli/issues/6)
- [As a user, I want to move title between different lists (e.g., from Watchlist to Viewing History), so that I can maintain accurate tracking of my viewing progress.](https://github.com/larevolucia/reeltracker_cli/issues/7)
- [As a user, I want to exit the app when I’m done so that I can close the session properly.](https://github.com/larevolucia/reeltracker_cli/issues/8)

### Should Have
- [As a user, I want to update details of an item in my Viewing History so that I can maintain accurate records.](https://github.com/larevolucia/reeltracker_cli/issues/14)
- [As a user, I want to rate a watched title so that I can track how much I enjoyed it.](https://github.com/larevolucia/reeltracker_cli/issues/9)

### Could Have
- [As a user, I want to see trending/popular titles so that I can explore new content.](https://github.com/larevolucia/reeltracker_cli/issues/10)
- [As a user, I want to get recommendations based on my ratings so that I can discover similar movies.](https://github.com/larevolucia/reeltracker_cli/issues/11)
- [As a user, I want to receive random movie suggestions so that I can easily pick what to watch next.](https://github.com/larevolucia/reeltracker_cli/issues/12)
- [As a user, I want to categorize my watchlist into sublists (e.g. “Must Watch”, “For Later”) so that I can organize my movies better.](https://github.com/larevolucia/reeltracker_cli/issues/13)


## Features

### 🎯 Core Functionality

#### Search titles via TMDb API

Users can search for movies or TV shows by keyword. The app returns results from The Movie Database (TMDb) API, including title, type, release year, and a short overview.
Related user story:  [#3 Search for a title](https://github.com/larevolucia/reeltracker_cli/issues/3)

#### Add to watchlist
Users can add any title from the search results directly to their personal watchlist for future viewing.
Related user story:  [#4 Add to watchlist or Viewing History](https://github.com/larevolucia/reeltracker_cli/issues/4)

#### Mark titles as watched and assign ratings
Users can mark a title as watched and give it a personal rating from 1 to 10. This allows them to track both progress and preferences.
Related user story:  [#5 View lists](https://github.com/larevolucia/reeltracker_cli/issues/5), [#9 Rate watched title](https://github.com/larevolucia/reeltracker_cli/issues/9), [#14 Update title](https://github.com/larevolucia/reeltracker_cli/issues/14)

####  Move titles between lists
A title can be moved from the Watchlist to the Viewing History once watched, preserving metadata such as date added.
When moving a title from Viewing History to Watchlist, watched data and rating are reset. 
Related user story:  [#7 Move title between lists](https://github.com/larevolucia/reeltracker_cli/issues/7), [#14 Update title](https://github.com/larevolucia/reeltracker_cli/issues/14)

#### Delete title from lists
Users can delete a title from the lists.
Related user story:  [#6 Remove a title from lists](https://github.com/larevolucia/reeltracker_cli/issues/6)

### 📁 Data Storage & Sync

#### Google Sheets integration 
All user data (watchlist, history, ratings) is stored in a personal Google Sheet via the Sheets API. This ensures cloud persistence and makes data accessible outside the CLI.
- Uses `gspread` and `google-auth` for integration
- Credentials are safely loaded from a `.json` file and hidden using `.gitignore`

#### Reload and reconstruct data
The app can rebuild `Title` objects from the spreadsheet using the `from_sheet_row()` method. This ensures data continuity across sessions.

### 📈 Smart Sorting & Discovery

#### Weighted popularity sorting

A custom `calculate_weighted_popularity()` function ensures titles are ranked based on both `TMDb popularity` and `vote count`. This prevents obscure titles with low votes from unfairly topping the list. Search output uses this function to display most relevant item on top with the use of `sort_items_by_popularity`.

Consulted references:
- [Python Math](https://docs.python.org/3/library/math.html)
- [W3School sorted( )](https://www.w3schools.com/python/ref_func_sorted.asp)
- [FreeCodeCamp lambda sort list in Python](https://www.freecodecamp.org/news/lambda-sort-list-in-python/)

### 🧰 Interface & Code Design

#### Clean and readable terminal output
The UI adapts to Heroku CLI constraints (80x24), avoiding broken formatting and wrapping issues. Multi-line outputs (like overviews) are carefully indented for clarity.

#### Modular code architecture 
The codebase is structured in modules by responsibility. This improves readability, scalability, and maintainability.

```bash
.
├── run.py             # Entry point for the CLI
├── menus.py           # Menu logic and user navigation
├── sheets.py          # Google Sheets integration
├── tmdb.py            # TMDb API interaction
├── ui.py              # User interface formatting and display
├── utils.py           # Helper functions (e.g., sorting, formatting)
├── title.py           # Title model and data transformation
├── user_data.py       # User-specific metadata (ratings, watched logs and status)
```

#### Classes Overview
`Title`
Represents a movie or TV title. Holds attributes like name, type, release date, overview, popularity, vote count.
Includes methods for:
- `to_sheet_row`: formats the title data for saving to Google Sheets
- `from_sheets_row`: reconstructs a `Title` object from saved sheet data

`UserTitleData`
Stores user-generated data about a title:
- `watched` status: edited using the `toggle_watched` method
- Personal `rating`: edited using the `set_rating` method
- `added_date` log: populated with timestamp when object creation
- `watched_date` log: populated with timestamp when `watched` status is changed to `True`

Consulted references:
- [PyNative](https://pynative.com/python-class-method-vs-static-method-vs-instance-method)
- [BuiltIn](https://builtin.com/software-engineering-perspectives/python-cls)
- [GeeksForGeeks](https://www.geeksforgeeks.org/classmethod-in-python/)

## Requirements

### Python  

- Script was coded using Python version 3.12.8
- To install dependencies run `pip3 freeze > requirements.txt`

### Google API

This project uses Google Sheets to store personal viewing history and watchlist. You'll need to enable Drive and Google Sheets API on your Google Cloud to be able to configure your personal list.

#### 1. Creating a project

- Start by navigating to [Google Cloud Console](https://console.cloud.google.com/). If you don't have a Google account, you'll to create one.
- Create a new project. [Check the official documentation on new project creation](https://developers.google.com/workspace/guides/create-project).

#### 2. Enable APIs
- Go to your project home and navigate to _APIs and Services > Library_.
- Search for Google Drive API, navigate to its page and click on **Enable**.
- Follow the same process to activate Google Sheets API.

#### 3. Get Credentials
- In your project view, navigate to _APIs and Services > Credentials_.
- Click on **Create credentials** button, select **Help me choose**.
- On the form, select **Google Drive API** on the dropdownlist os APIs.
- Select **App Data** regarding the type of data to be used.
- Fill in the name of the service account and the account ID (_You'll need this to configure your script_).
- Click and create and continue. 

#### 4. Save credentials information
- You'll be redirect to a credential screen. Select the e-mail address under **Service Account** and click on the edit button.
- Navigate to Keys and click go to _Add Key > Create New Key_
- Select JSON and create.
- The create will automatically trigger a download of the json file.

#### 5. Project configuration
- Move the downloaded file to the root folder of your project. You can name it **creds.json** as I did, or give it another name. Just be sure that the name is matching in your `run.py` file.
- On your Google account, create a new Google Sheets document. You can name it `reeltracker_cli` as I did, or give it another unique name. Just be sure that the name is matching in your `run.py` file.
- On your new file, click on the share button and copy&paste the e-mail address that can be found in your creds.json.
- If you haven't yet, install `gspread` and `google-auth` libraries.
- Add the following code to your project to set up your Google API connection:

    ```python
    import gspread
    from google.oauth2.service_account import Credentials

    SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

    CREDS = Credentials.from_service_account_file('<your_creds_file_name>.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET =  GSPREAD_CLIENT.open('<your_google_sheet_name>')
    ```

### TMDB API

This project uses TMDB API to fetch data of movies and TV Shows. You'll need to create an account and request an API Key.

#### 1. Requesting the API Key

- Go to [TMDB Signup](https://www.themoviedb.org/signup)
- Once signed in, request an API key at [TMDB API page](https://www.themoviedb.org/settings/api).

#### 2. Project Configuration
-  If you haven't yet, install `requests` and `python-dotenv` libraries.
- Create a .env file on your root folder and add your API key `TMDB_API_KEY=your_actual_tmdb_api_key_here`.
- Add .env to your .gitignore file to ensure it's never pushed to GitHub.
- Load API Key from .env file:

    ```python
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Access TMDB API key
    api_key = os.getenv('TMDB_API_KEY')

    if api_key is None:
       raise ValueError("TMDB_API_KEY not found. Check your .env file.")
    ```

#### 3. Test API Request
- Test your configuration by sending an API request:
    ```python
    TMDB_URL ='https://api.themoviedb.org/3'
    LANGUAGE ='language=en-US'
    tmdb_api_key = os.getenv('TMDB_API_KEY')

    url = f'{TMDB_URL}/movie/popular?api_key={api_key}&{LANGUAGE}&page=1'
    response = requests.get(url,timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

    ```
- You can install `rich` library for an easier read of the json response
    ```python
    import json
    from rich import print_json

    url = f'{TMDB_URL}/movie/popular?api_key={api_key}&{LANGUAGE}&page=1'
    response = requests.get(url,timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    ```

## Deployment

### Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

### Config Var
You must then create a _Config Var_ called `PORT`. Set this to `8000`
You must then create a _Config Var_ called `CREDS`. Copy&Paste your `creds.json` file contents.
You must then create a _Config Var_ called `TMDB_API_KEY`. Copy&Paste your API Key value.

Connect your GitHub repository and deploy.