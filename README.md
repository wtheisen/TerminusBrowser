<p align="center">
    # commandChan - a terminal 4chan browser
</p>

1. [Introduction](#introduction)
2. [Screenshots](#screenshots)
3. [Hotkeys](#hotkeys)
4. [TODO List](#todoList)
5. [Bug List](#bugList)

## Introduction <a name="introduction"></a>

Created out of a desire to browse 4chan at work.
This is a terminal browsing application for [4chan](https://www.4chan.org/).
Built using the [urwid](https://github.com/urwid/urwid/) library for python and the [4chan JSON API](https://github.com/4chan/4chan-API).

## Screenshots <a name="screenshots"></a>

![Board Index](./screenshots/boardIndex.png?raw=true "Board Index")

![Board View](./screenshots/boardView.png?raw=true "Board View")

![Thread View](./screenshots/threadView.png?raw=true "Thread View")

## Hotkeys <a name="hotkeys"></a>

- 'q' - go up a level, or quit the program if viewing the board index
- 'u' - in-place update either the catalog or the thread in focus
- 'w' - watch the currently focused thread
- 'e' - view the thread watcher

## TODO List <a name="todoList"></a>

- [X] Display images links on posts
- [X] Board and Thread fetch information in the footer
- [] Filtering options on all pages with information in the footer
- [] Display comment replies in the info bar at the top of the comment
- [] Save threads to a custom hotkey menu
    - [X] Watch threads from the board view
    - [X] Watch thread from within the thread
    - [] Hotkey to delete thread from watcher
    - [] Auto-prune threads that get archived
- [] Quote button full interaction
    - [X] Quotes of OP have the (OP) designator
    - [X] Interacting with Quotes displays a preview of said Quote
    - [] Size of preview depends on size of quote being previewed
    - [] Chain Quote Previews together to view up the quote tree
- [] Split view based on hotkeys
- [] Timed updating of threads
- [] Posting from the client


## Bugs List <a name="bugList"></a>

| Cause                                              | Effect                       | Fix
|:--------------------------------------------------:|:----------------------------:|:--------------------------------:|
| Posts get incorrectly flagged as containing images | Program fatally crashes      | Changed where the image links were being parsed|
| Cross Thread Links                                 | Program fatally crashes      |                                  |
| Unknown                                            | Image links aren't displayed | Replaced the code I accidentally erased|


If you wish to contribute or know more please feel free to contact me!
