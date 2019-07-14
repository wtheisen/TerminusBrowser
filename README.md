# commandChan - a terminal 4chan browser

1. [Introduction](#introduction)
2. [Screenshots](#screenshots)
3. [Hotkeys](#hotkeys)
4. [TODO List](#todoList)
5. [Bug List](#bugList)

## Introduction <a name="introduction"></a>

Created out of a desire to browse 4chan at work.
This is a terminal browsing application for [4chan](https://www.4chan.org/).
Built using the [urwid](https://github.com/urwid/urwid/) library for python and the [4chan API](https://github.com/4chan/4chan-API).
To run `python3 commandChanVim.py`

## Screenshots <a name="screenshots"></a>

![Board Index](./screenshots/boardIndex.png?raw=true "Board Index")

![Board View](./screenshots/boardView.png?raw=true "Board View")

![Thread View](./screenshots/threadView.png?raw=true "Thread View")

## Hotkeys <a name="hotkeys"></a>

- 'q'   - go up a level, or quit the program if viewing the board index
- 'r'   - in-place update either the catalog or the thread in focus
- ':'   - puts you in command mode where you can type full commands
- 'esc' - puts you in normal mode where the usual hotkeys will work

## Commands <a name="commands"></a>

- (s)earch [PATTERN] - filters the current view to only items containing [PATTERN], if [PATTERN] is empty it will reset the search and refresh the current view
- (t)hread [THREAD NUMBER] - open the thread on the current board with the specified number
- reddit - switch client to reddit mode
- 4chan - switch client to 4chan mode

## Setup <a name="setup"></a>
To run, either run:

1. Install dependencies / module with `python3 setup.py develop`
    - `python3 src/commandChan/commandChanVim.py`
    - Whenever you update a package/code need to run `python3 setup.py develop` to build package
2. install package with `python3 setup.py install`
    - run with `commandChan` in terminal

## TODO List <a name="todoList"></a>

- [X] Display images links on posts
- [X] Board and Thread fetch information in the footer
- [X] Filtering options on all pages with information in the footer
- [] HJKL movement (HL work right now, JK don't for some reason)
- [] Full suite of commands
    - [X] Search command for current view
    - [X] Thread command to view thread by number
- [] Toggleable display modes(boxes, tree, cascade)
- [] Display comment replies in the info bar at the top of the comment
- [] Save threads to a custom hotkey menu
    - [] Watch threads from the board view
    - [] Watch thread from within the thread
    - [] Hotkey to delete thread from watcher
    - [] Auto-prune threads that get archived
- [] Quote button full interaction
    - [] Quotes of OP have the (OP) designator
    - [] Interacting with Quotes displays a preview of said Quote
    - [] Size of preview depends on size of quote being previewed
    - [] Chain Quote Previews together to view up the quote tree
- [] Split view based on hotkeys
- [] Timed updating of threads
- [] Posting from the client
- [] Full Reddit Functionality
    - [] Pagination
    - [] Tree comment structure

## Bugs List <a name="bugList"></a>

| Cause                                              | Effect                       | Fix
|:--------------------------------------------------:|:----------------------------:|:--------------------------------:|
| Posts get incorrectly flagged as containing images | Program fatally crashes      |Fixed regex for images|
| Cross Thread Links                                 | Program fatally crashes      |                                  |
| Unknown                                            | Image links aren't displayed | Replaced the code I accidentally erased|


If you wish to contribute or know more please feel free to contact me!
