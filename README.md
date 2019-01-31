# ig-followers-tracker-discord
![description](https://i.imgur.com/FkXsr2E.png)

A Discord Bot for tracking instagram followers and send summary to discord channels

## Setup

### Instagram Setup

 1. Login to [Instagram](https://www.instagram.com/) Using firefox.
 2. Copy [cookies.sqlite](https://support.mozilla.org/en-US/questions/904767) into session-converter folder
 3. run savesession.py using python
 4. Move cookies.sqlite to bot folder
 5. Edit bot.py  `USER =  'usernamehere'` (Line 10) Change usernamehere to your session username

### Database Setup
1. import igtracker.sql to your mysql database
2. Edit bot.py. Line number 16-19 edit to your database config

### Bot Setup
1. Goto [Discord Developer Dashboard](https://discordapp.com/developers/applications/)
2. Login and [Create a bot account](https://discordpy.readthedocs.io/en/rewrite/discord.html)
3. Edit bot token at bot.py file line 199 (or the buttom of the file)
4. Run bot.py using python

### Bot Tracker Setup
1. [Invite your bot account to your server](https://discordpy.readthedocs.io/en/rewrite/discord.html#inviting-your-bot)
2. Create a channel for bot to bound on that channel
3. Type a command `.adduser yourinstagramusername` for adding username to database for tracking
4. Bot will track your followers and sent it to channel every 11:30 PM

## Disclaimer
**This project using for practice my Python language experience**
If you help me improve my code please make a pull request with edited code in it (Add description explaining will much help)

**Don't pull request or make issues like your code is f__king s_it because i know and as a tell you it is my FIRST experience with Python**

**You can help me fix README typo too. Sorry for that typo i know it bad**

## License
This project is licensed under the [MIT License](https://github.com/Holfz/ig-followers-tracker-discord/blob/master/LICENSE).
