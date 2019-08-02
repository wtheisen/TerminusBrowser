[![Build Status](https://travis-ci.com/wtheisen/commandChan.svg?branch=master)](https://travis-ci.com/wtheisen/commandChan)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

# commandChan - a terminal 4chan/Reddit browser
1. [Introduction](#introduction)
2. [Screenshots](#screenshots)
3. [Hotkeys](#hotkeys)
4. [Configuration](#config)
5. [TODO List](#todoList)

## Introduction <a name="introduction"></a>

Created out of a desire to browse 4chan at work, commandChan is turning into a general framework for browsing
sites in the terminal using a unified program.
This is currently a terminal browsing application for [4chan](https://www.4chan.org/), and now [Reddit](https://www.reddit.com/).
Built using the [urwid](https://github.com/urwid/urwid/) library for python.
It also makes use of the [4chan API](https://github.com/4chan/4chan-API) and the [Reddit API](https://www.reddit.com/dev/api/)
To run `python3 commandChanVim.py`

## Screenshots <a name="screenshots"></a>

![Board Index](./screenshots/boardIndex.png?raw=true "Board Index")

![Board View](./screenshots/boardView.png?raw=true "Board View")

![Thread View](./screenshots/threadView.png?raw=true "Thread View")

## Hotkeys <a name="hotkeys"></a>

- ':'   - puts you in command mode where you can type full commands
- 'esc' - puts you in normal mode where the usual hotkeys will work

## Commands <a name="commands"></a>

- (q)uit(a)ll - Close the program
- (t)hread [THREAD NUMBER] - open the thread on the current board with the specified number
- view [PATTERN] - [PATTERN] being either 4chan or reddit currently it will open that site in the current view
- (h)istory - will go back one level in the history list
- (s)earch [PATTERN] - will search the current view for the pattern, if pattern is blank it will reset the current view

## Configuration <a name="config"></a>

- To change the default site you can modify the config.json file [FCHAN/REDDIT]
- The config.json file also contains the boards list and the subreddit list

## TODO List <a name="todoList"></a>

- [X] Display images links on posts
- [X] Board and Thread fetch information in the footer
- [ ] Filtering options on all pages with information in the footer
- [X] HJKL movement
- [ ] Full suite of commands
    - [X] Search command for current view
    - [X] Thread command to view thread by number
    - [X] Toggle to show or hide stickied reddit posts
- [ ] Toggleable display modes(boxes, tree, cascade)
- [X] Display comment replies in the info bar at the top of the comment
- [ ] History Frame
- [ ] Quote button full interaction
    - [ ] Quotes of OP have the (OP) designator
    - [ ] Interacting with Quotes displays a preview of said Quote
    - [ ] Size of preview depends on size of quote being previewed
    - [ ] Chain Quote Previews together to view up the quote tree
- [ ] Split view based on hotkeys
- [ ] Timed updating of threads
- [ ] Posting from the client
- [ ] Full Reddit Functionality
    - [ ] Pagination
    - [X] Tree comment structure
- [ ] Hacker News Functionality
- [ ] Lobster.rs Functionality
