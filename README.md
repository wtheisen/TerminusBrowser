# commandChan

CLI curses 4chan browser
======


Created out of a desire to browse 4chan at work.
This is a terminal browsing application for [4chan](https://www.4chan.org/).
Built using the [urwid](https://github.com/urwid/urwid/) library for python, it uses the [4chan JSON API](https://github.com/4chan/4chan-API).

### Screenshots

![alt](./screenshots/boardIndex.png?raw=true "Board Index")

![alt](./screenshots/boardView.png?raw=true "Board View")

![alt](./screenshots/threadView.png?raw=true "Thread View")


### TODO List

- [] Display images links on posts
- [X] Board and Thread fetch information in the footer
- [] Filtering options on all pages with information in the footer
- [] Display comment replies in the info bar at the top of the comment
- [X] Quotes of OP have the (OP) designator
- [] Save threads to a custom hotkey menu
- [X] Interacting with Quotes displays a preview of said Quote
    - [] Size of preview depends on size of quote being previewed
    - [] Chain Quote Previews together to view up the quote tree
- [] Split view based on hotkeys
- [] Timed updating of threads
- [] Posting from the client


Known Bugs
------
| Cause                                              | Effect                       |
|:--------------------------------------------------:|:----------------------------:|
| Posts get incorrectly flagged as containing images | Program fatally crashes      |
| Cross Thread Links                                 | Program fatally crashes      |
| Unknown                                            | Image links aren't displayed |
