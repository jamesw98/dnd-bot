# dnd-bot
Adventurer Companion, a Dungeons and Dragons Discord bot.  
You can add it to your server by visiting this link: https://top.gg/bot/782772961366507611 (at the moment, 11/30/2020, it is still being approved)

## Current Features  
### Help command. 
- show the help message: `!dnd help`
### Dice rolling. 
- basic roll: `!dnd roll [number of dice]d[die type]` (1d4, 2d8, 33d20, etc.)
- roll with modifier: `!dnd roll [num]d[type] [+/-] [modifier]` (2d4 + 2, 1d20 - 2, 33d20 + 330, etc.)
- roll with advantage or disadvantage: `!dnd roll [num]d[type] [a/d]`, `!dnd roll [num]d[type] [+/-] [mod] [a/d]` where `a` signifies advantage and `d` signifies disadvantage (2d4 a, 1d20 + 2 d, etc.)
- note: `roll` can be replaced with `r`
### Searching. Uses [DnD 5e API](https://www.dnd5eapi.co/)
- `!dnd search [query]`
- note: `search` can be replaced with `s`
### Initiative Tracking.
- start tracking initiative: `!dnd initiative start [name1]:[init#],[name2]:[init#],[name3]:[init#],...` (... start Volo:16,Strahd:18,Drizzt:20,jombles:1)
  - names and initiative numbers must be separated by colon characters ':'
  - there cannot be any spaces between the names
- cycle to next player in initiative: `!dnd initiative next`
- remove player from initiative: `!dnd initiative remove [name]`
- add player(s) to initiative: `!dnd initiative add [name1]:[init#],[name2]:[init#],...`
- view initiative: `!dnd initiative`
- stop tracking initiative: `!dnd initiative clear` 
- note: `initiative` can be replace with `init` or `i` in all these commands
### Re-run the last command
- re-runs the last command `!dnd`


