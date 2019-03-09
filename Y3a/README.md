# Calendar archive
These scripts are made to make an archive calendar for me to subscribe to. The reason that this is needed is that the university calendar subscription service TimeEdit only allows you to see events younger than two weeks in your calendar. I don't think this feels very intuitive so I tried to fix this...

The strategy I eventually took is this:
 1. Download a CSV file of the whole school year. (CSV since .ICS-export option only covers latest two weeks)
 2. Truncate all events younger than two weeks. (So this archive celendar doesn't interfere with my regular subscribed schedule)
 3. Parse CSV into ICS file.
 4. Upload ICS to my personal webserver via FTP.
 5. Subscribe to calendar url from my calendar program.


## Issues

* Every event in an ICS-file needs an UID identification string. Since the downloaded CSV doesn't contain an ID for the events I had to construct one. I just hashed all the data for one event to bodge together a UID-string. This isn't a great solution since I suspect I might get duplicate activities in my calendar if TimeEdit decides to update an old event. A solution to this (as I later recognized) could be to parse the HTML from TimeEdit since it actually contains the same ID number you usually find in the events when you subscribe to TimeEdit. This however seems to be a bit more work than to parse a simple CSV-file.


## Quick reference for launchctl
I used launchctl on the mac to schedule this script every sunday night. Here are some notes:

The code is written in `local.martinclason.timeedit-kalender-uppdatering.plist` located in:
`/Users/martinclason/Library/LaunchAgents`


The following commands are quite handy:
```bash
launchctl load local.martinclason.timeedit-kalender-uppdatering.plist
launchctl unload local.martinclason.timeedit-kalender-uppdatering.plist
launchctl start local.martinclason.timeedit-kalender-uppdatering
```

You can also look for output in the `*.stdout` and `*.stderr` files.

