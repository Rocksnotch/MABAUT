# terminalCommandsWindows.py
# Purpose: Control overall terminal items (like background color)

import sys
import os
import subprocess

def setBackgroundColor(bgRGB):
    rBg, gBg, bBg = bgRGB

    ansiCode = f"\033[48;2;{rBg};{gBg};{bBg}m\033[2J\033[H"

    print(ansiCode)

def setTextColor(textRGB):
    rTxt, gTxt, bTxt = textRGB
    
    ansiCode = f"\033[38;2;{rTxt};{gTxt};{bTxt}m"
    
    print(ansiCode)

def setTopCenter(text="============================MERIDIAN-ARCH//BACKDOOR_ACCESS//UTILITY TOOLS============================"):
    terminalSize = os.get_terminal_size()
    columns = terminalSize.columns

    if len(text) > columns:
        text = text[:columns]

    centeredText = text.center(columns)

    print("\033[1;1H")
    print(centeredText)

def printCentered(text, header="", indent=4, headerPadding=5):
    columns, lines = os.get_terminal_size()

    # Clear screen and draw the fixed top banner
    clearConsole()
    setTopCenter()
    
    # Add padding lines below the top banner to push the header down
    print("\n" * headerPadding, end="")

    indentSpaces = " " * indent
    
    # Indent and print the header
    if header:
        indentedHeader = "\n".join(indentSpaces + line for line in header.splitlines())
        print(indentedHeader)
        headerLines = header.count('\n') + 1
    else:
        headerLines = 0

    # Calculate total empty lines left in the console
    totalUsedLines = 1 + headerPadding + headerLines + 1 + 1
    remainingLines = lines - totalUsedLines

    # Split remaining lines: top half goes above text, bottom half goes below
    linesAboveText = lines // 2
    topVerticalPadding = linesAboveText - (1 + headerPadding + headerLines)
    bottomVerticalPadding = remainingLines - topVerticalPadding

    # Ensure padding numbers never drop below zero on small screens
    topVerticalPadding = max(0, topVerticalPadding)
    bottomVerticalPadding = max(0, bottomVerticalPadding)

    # Center text using full width
    rawCenteredText = text.center(columns)
    if rawCenteredText.startswith(" " * indent):
        indentedText = rawCenteredText
    else:
        strippedText = text.center(columns - (indent * 2))
        indentedText = indentSpaces + strippedText

    # Output with decoupled, independent top and bottom padding sizes
    print("\n" * topVerticalPadding, end="")
    print(indentedText)
    print("\n" * bottomVerticalPadding, end="")


def waitKey(prompt="Press any key to continue..."):
    print(prompt, end="", flush=True)
    
    if os.name == "nt":
        # Windows configuration
        import msvcrt
        msvcrt.getch()

def clearConsole():
    # Detect the operating system
    command = 'cls' if os.name == 'nt' else 'clear'
    
    # Run the system command safely
    subprocess.run([command], shell=True)

def resetTerminal():
    print("\033[0m")
