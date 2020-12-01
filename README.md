# dnd-bot
Adventurer Companion, a Dungeons and Dragons Discord bot.  
You can add it to your server by visiting this link: https://top.gg/bot/782772961366507611 (at the moment, 11/30/2020, it is still being approved)

# Current Features  
- Help command. Shows the available commands:
  - `!dnd help`
- Dice rolling. With many formats, which can be seen below:
  - basic roll: `!dnd roll [number of dice]d[die type]` (1d4, 2d8, 33d20, etc.)
  - roll with modifier: `!dnd roll [num]d[type] [+/-] [modifier]` (2d4 + 2, 1d20 - 2, 33d20 + 330, etc.)
  - roll with advantage or disadvantage: `!dnd roll [num]d[type] [a/d]`, `!dnd roll [num]d[type] [+/-] [mod] [a/d]` where `a` signifies advantage and `d` signifies disadvantage (2d4 a, 1d20 + 2 d, etc.)
  - note: `roll` can be replaced with `r`
- Searching. You can search for equipment, spells, monsters, and magic items. If the bot can find it in the [DnD 5e API](https://www.dnd5eapi.co/), it will give you info about it. 
  - `!dnd search [query]`
  - note: `search` can be replaced with `s`
- Initiative Tracking. Lets you track player initiative, advance the initiative counter, and remove players/monsters from the initiative (all initiative commands can only be run in a direct message with the bot)
  - start tracking initiative: `!dnd initiative start [name1]:[init#],[name2]:[init#],[name3]:[init#],...` (... start Volo:16,Strahd:18,Drizzt:20,jombles:1)
    - names and initiative numbers must be separated by colon characters ':'
    - there cannot be any spaces between the names
  - cycle to next player in initiative: `!dnd initiative next`
  - remove player from initiative: `!dnd initiative remove [name]`
  - add player(s) to initiative: `!dnd initiative add [name1]:[init#],[name2]:[init#],...`
  - view initiative: `!dnd initiative`
  - stop tracking initiative: `!dnd initiative clear` 
  - note: `initiative` can be replace with `init` or `i` in all these commands
- Re-run the last command. Assuming you have run a command with this bot, it will re-run the last command
  - `!dnd`


