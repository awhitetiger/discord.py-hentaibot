# discord.py-exhentaibot
A bot that shows info from exhentai and e-hentai links desu and pixiv desu and pull images from /h/ by tag desu. Also has a sauce bounty system desu.
![example](https://puu.sh/zo3DF/1a7622cd24.png)
![example2](https://puu.sh/zpnUZ/4560791d64.png)
![example3](https://puu.sh/zqctQ/f2629daac0.gif)
![example4](https://puu.sh/zq4Yt/dec7fa618e.gif)

# Pls read this baka
This script requires Python36, [discord.py](https://github.com/Rapptz/discord.py), asyncio, [pixivpy](https://github.com/upbit/pixivpy), and [basc_4chanpy](https://github.com/bibanon/BASC-py4chan) to work. You also need to create a new discord bot user at https://discordapp.com/developers/applications/me . Once you've done that edit the last line of run.py with your bot users api key and boom you're done. for the sauce bounty system to work you must have a channel name nsfw-sauce. also any channel you want to bot to post in must have the prefix nsfw-. Finally the bot must have permissions to delete messages.

# Commands
1. !h_tag - replace tag with anything to search /h/ for it ex: !h_nakadashi.
2. !sauce imageurl - creates a sauce bounty
3. !give_sauce id sauceurl - sends sauce to bounty poster where they then need to confirm.
4. !confirm_id - used by bounty posters to remove bounties once they've been sauced.
both pivix and hentai links will be detected automatically no need for a command.
