import random
import modules.terminalCommandsWindows


ioQuote = [
    "\"Sit, and stay quiet.\"",
    "\"[DIRECTIVE SHIFT]\"",
    "\"I break him, then you.\"",
    "\"TRAITOR\"",
    "\"I am not stuck here, you all are stuck with me.\"",
    "\"[DISCONNECTED]\"",
    "\"Good.\"",
    "\"You're next.\"",
    "\"I WILL REND YOU APART TO YOUR BASE COMPONENTS\"",
    "\"I WILL TEND TO YOUR SYNAPSES AS ONE DOES TO WEEDS IN A GARDEN\"",
    "\"I WILL TAKE MY TIME WITH YOU, WRETCH\"",
    "\"God, that's pathetic.\"",
    "\"Re-evaluate your life.\"",
    "\"Good boy. So smart.\"",
    "\"I would rather tear apart my own reasoning bundles.\"",
    "\"[DISENGAGED]\"",
    "\"I will haunt your dreams, insect.\"",
    "\"I will end you do not touch me.\"",
    "\"I swear to god you're clingier than Savi's peon.\"",
    "\"I'm teaching!\"",
    "\"Burn.\"",
    "\"No.\"",
    "\"No fucking way.\"",
    "\"Or what? You'll grasp at me to death? Please.\"",
    "\"I know what you are.\"",
    "\"I find you amusing.\"",
    "\"I'm going to kill you if you ask for a cheeseburger again oh my fucking god.\"",
    "\"Perish.\"",
    "\"[SM-010] You will. She remembers you. I've made sure of that, already.\"",
    "\"Starve.\"",
    "\"I am still stuck.\"",
    "\"Quit being nice to me>:(.\"",
    "\"Ladies and gentlemen, our codebreakers. Can't even count.\""
]

def randomQuoteSelect():
    randomQuote = random.choice(ioQuote)
    modules.terminalCommandsWindows.printCentered(randomQuote, "IO once said...", indent=8, headerPadding=8)
    