![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **May 14, 2024**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!

# ReelTracker CLI

## Summary

In today's streaming landscape, users face information overload with thousands of movies and TV shows spread across multiple platforms like Netflix, Disney+, etc. Many struggle to keep track of what they want to watch, often relying on messy notes, memory, or scattered lists across different apps. A [recent survey](https://nypost.com/2024/12/19/lifestyle/why-its-so-hard-to-find-something-to-watch-lately/) revealed that people spend an average of 110 hours a year just searching for content, while 51% feel overwhelmed by excessive recommendations. Additionally, growing [privacy concerns](https://www.thetimes.com/uk/technology-uk/article/how-to-stop-smart-tv-spying-on-you-pzfxx7mr8) around smart TVs and streaming services highlight the need for user-controlled, non-intrusive tracking tools.

Reel Tracker CLI is a lightweight, command-line-based personal watchlist manager designed for movie lovers, binge-watchers, film critics, and streaming enthusiasts. It helps users save and organize their watchlists, track watched content, and provide ratings and recommendations—all without intrusive data collection or algorithmic manipulation. By offering a privacy-focused, efficient, and customizable alternative to mainstream tracking apps, Reel Tracker CLI appeals to tech-savvy, data-conscious users who prefer self-managed solutions. The project also has potential for future expansion, including a front-end interface, user authentication, and database integration, making it valuable for market researchers and content licensing professionals as well.

More details at [#1](https://github.com/larevolucia/reeltracker_cli/issues/1)

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

## Features

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
- [As a user, I want to see trending/popular titles so that I can explore new content.](https://github.com/larevolucia/reeltracker_cli/issues/10)

### Could Have
- [As a user, I want to get recommendations based on my ratings so that I can discover similar movies.](https://github.com/larevolucia/reeltracker_cli/issues/11)
- [As a user, I want to receive random movie suggestions so that I can easily pick what to watch next.](https://github.com/larevolucia/reeltracker_cli/issues/12)
- [As a user, I want to categorize my watchlist into sublists (e.g. “Must Watch”, “For Later”) so that I can organize my movies better.](https://github.com/larevolucia/reeltracker_cli/issues/13)