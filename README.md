# kmhm-auto
This project is designed to be an automated tool for a browser game. 
To make this less detectable, it uses PyChromeDevTools and remote debug feature of the Chrome developer tools, 
which should be totally transparent to the server. 
This is at the cost of consuming more time and resources than light-weight browser/package solutions.

It is still being developed, uploaded for my own record.

## Limitations

### Resource consuming
Non browser client solutions are always much more light weight on resource consuming. 
The only advance it have (maybe) is that it is harder for the server to be detected by the
server since real browser runs on the client. 
Generally, this tradeoff is not worth it since in no browser solutions, theoretically
you can make it as close to real browser in perspective of the server as you want, and for many page games
they don't really care about if you run a non browser. (If they can make money from you)

### Monitor scaling
Many OSs have the feature to scaling the display for a high resolution monitors. I believe you can detect it with
some Python packages, but for now I only tested it in a FHD secondary monitor and didn't take scale into account. 
Since the game has a fixed number of pixels in display and resides on certain area of the screen, I am pretty sure
it doesn't work for scaling. That's might be something in TODO list if necessary.

### Not able to run background
This project use ChromeDevTools' `Page.captureScreenshot` to take screenshots regularly to
analyze status of the game and do the next step. Seems like it does a real system call to do that,
which means it needs to bring the page to front. The plan to interact with the game is also to use API
provided by ChromeDevTools, which I believe the same. User probably can't do other tasks on the mean time.

### ChromeDevTools reactions on SIGINT
That package seems to return `None` instead of throw KeyboardInterrupt to caller. Not causing trouble for now. 
But need to keep this in mind.