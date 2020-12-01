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
- Searching. You can search for equipment, spells, monsters, and magic items. If the bot can find it in the [DnD 5e API](https://www.dnd5eapi.co/), it will give you info about it.  
  - `!dnd search [query]`
