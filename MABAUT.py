import time

from modules.terminalCommandsWindows import *
from modules.encoder import beginEncode
from modules.decoder import beginDecode
from modules.ioQuotes import randomQuoteSelect

# Global Variables
endProgram = False

if __name__ == "__main__":
    setBackgroundColor((8, 13, 28))
    setTextColor((152, 192, 240))
    while endProgram == False:
        clearConsole()
        setTopCenter()
        print("\n\n")
        print("    1) BASIL Encoder")
        print("    2) BASIL Decoder")
        print("    3) IO Random Quote Selector")
        print("    0) Close Program")
        print("\n")
        userChoice = input("    Input Requested > ")

        match userChoice:
            case "1":
                beginEncode()
                waitKey()
            case "2":
                beginDecode()
            case "3":
                randomQuoteSelect()
                waitKey()
            case "0":
                print("Closing program...")
                time.sleep(2)
                resetTerminal()
                clearConsole()
                endProgram = True
            case _:
                print("Unknown entry. ", end="")
                waitKey()
                
