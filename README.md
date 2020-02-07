![Actions Status](https://github.com/wtheisen/TerminusBrowser/workflows/Python%20application/badge.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)



# TerminusBrowser - a terminal 4chan/Reddit browser
1. [Introduction](#introduction)
2. [Screenshots](#screenshots)
3. [Hotkeys](#hotkeys)
4. [Configuration](#config)
5. [Contributing](#contrib)
6. [TODO List](#todoList)

## Introduction <a name="introduction"></a>

Previously known as commandChan.

Created out of a desire to browse 4chan at work, TerminusBrowser is turning into a general framework for browsing
sites in the terminal using a single program.
This is currently a terminal browsing application for [4chan](https://www.4chan.org/), [Reddit](https://www.reddit.com/), [Hacker News](https://news.ycombinator.com/), and [lainchan](https://www.lainchan.org/).
Built using the [urwid](https://github.com/urwid/urwid/) library for python.
It also makes use of the [4chan API](https://github.com/4chan/4chan-API), the [Reddit API](https://www.reddit.com/dev/api/), a third-party [Hacker News API](https://hn.algolia.com/api), and the [lainchan API](https://github.com/vichan-devel/vichan-API/). Development for all sites are still on-going so while basic browsing will work there may be smaller bugs or features than you may notice. Please feel free to notify the dev team by opening an issue, or PRs are always welcome!

To run, first install the dependencies in requirements.txt

```
pip3 install -r requirements.txt
```

And then run `./TerminusBrowser.py`

## Screenshots <a name="screenshots"></a>

Click on photo for more detail

### 4chan

|      Board Index   |  Board View         | Thread view   |
| ------------- |-------------| -----|
|![](./screenshots/fchan_boards.png?raw=true) | ![](./screenshots/fchan_threads.png?raw=true) |![](./screenshots/fchan_post.png?raw=true)  |


### Reddit

| Subreddit Index | Subreddit View | Post View |
| ------- | ---------- | -------|
|![](./screenshots/reddit_subs.png?raw=true) | ![](./screenshots/reddit_threads.png?raw=true)| ![](./screenshots/reddit_comments.png?raw=true)

### Lainchan
| Board Index | Board view | Thread View |
| ------- | ------ | ------- |
| ![](./screenshots/lchan_boards.png?raw=true) | ![](./screenshots/lchan_threads.png?raw=true) | ![](./screenshots/lchan_post.png?raw=true) | 

## Hotkeys <a name="hotkeys"></a>

- ':'   - Puts you in command mode where you can type full commands
- 'esc' - Puts you in normal mode where the usual hotkeys will work
- HJKL  - Normal vim like navigation for selectable objects
## Commands <a name="commands"></a>

- (q)uit(a)ll - Close the program
- (t)hread [THREAD NUMBER] - open the thread on the current board with the specified number
- view [PATTERN] - [PATTERN] being [4chan/reddit/hackernews/lainchan/history] currently it will open that site in the current view
- (h)istory - will go back one level in the history list
- (s)earch [PATTERN] - will search the current view for the pattern, if pattern is blank it will reset the current view
- add [reddit/4chan] [PATTERN] - will add the subreddit or board [PATTERN] to the site index specified.

## Configuration <a name="config"></a>

- To change the default site you can modify the config.json file [FCHAN/REDDIT]
- The config.json file also contains the boards list and the subreddit list

## Contributing <a name="contrib"></a>

Development on TerminusBrowser is active and on-going. If there are any features
you want or you're just interested in joining in the discussion the dev team
is most active on [#TerminusBrowser on the Freenode IRC server](https://kiwiirc.com/nextclient/chat.freenode.org/#TerminusBrowser)

## TODO List <a name="todoList"></a>

- [X] Display images links on posts
- [X] Board and Thread fetch information in the footer
- [ ] Filtering options on all pages with information in the footer
- [X] HJKL movement
- [ ] Full suite of commands
    - [X] Search command for current view
    - [X] Thread command to view thread by number
    - [X] Toggle to show or hide stickied reddit posts
    - [ ] Download image(s) for later viewing
    - [ ] Filtering reddit comments based on score
- [ ] Toggleable display modes(boxes, tree, cascade)
- [X] Display comment replies in the info bar at the top of the comment
- [ ] History Frame
- [ ] Quote button full interaction
    - [X] Quotes of OP have the (OP) designator
    - [X] Interacting with Quotes displays a preview of said Quote
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
