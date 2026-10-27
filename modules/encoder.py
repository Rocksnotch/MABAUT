import modules.fileHandler as fileHandler
from modules.terminalCommandsWindows import setTopCenter, clearConsole

def messagePayload(textStr: str, encodeType: str = "utf-8") -> bytes:
    hexList = []

    # Turn the text into binary
    byteData = textStr.encode(encodeType)

    # Add a 1 in front of each byte and join them to a continuous string
    binaryNineStr = "".join("1" + f"{b:08b}" for b in byteData)

    #Chunk it into groupings of 8 now
    chunkedBinary = [binaryNineStr[i:i+8] for i in range(0, len(binaryNineStr), 8)]

    # Verify that the last block is 8 bits, otherwise pad with 0
    lastLength = len(chunkedBinary[len(chunkedBinary) - 1])
    bitsMissing = 8 - lastLength
    if bitsMissing > 0:
        # Get the actual binary
        currentByte = chunkedBinary[len(chunkedBinary) - 1]

        # Add the missing bits here
        newByte = currentByte.ljust(8, "0")

        # Replace now
        chunkedBinary[len(chunkedBinary) - 1] = newByte

    for chunk in chunkedBinary:
        hexList.append(hex(int(chunk, 2)))

    return hexList


def structureFile(payload: list):
    # We need to build the file structure now
    # Start with 0x02, or 'Start of Text'
    wholeFile = ["0x02"]
    fileEnd = ["0x03", "0x04"]

    # Append the hex list to it
    wholeFile += payload

    # Append the ending bytes
    wholeFile += fileEnd

    return wholeFile

def beginEncode():
    clearConsole()
    setTopCenter()
    print("\n")
    userMessage = input("Enter message to encode to Basil: ")
    definedPath = input("Enter full file path for saving: ")
    payload = messagePayload(userMessage)
    formattedPayload = structureFile(payload)
    fileHandler.writeFile(formattedPayload, definedPath)