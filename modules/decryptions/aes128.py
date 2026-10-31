from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from modules.terminalCommandsWindows import setTopCenter, clearConsole, waitKey

def decrypt(hexIn, keyIn, mode="ECB", ivIn=None):
    # 1. Clean spaces from inputs
    cleanHex = "".join(hexIn.split())
    cleanKey = "".join(keyIn.split())
    cleanIv = "".join(ivIn.split()) if ivIn else ""

    # 2. Convert to raw bytes
    try:
         cipherBytes = bytes.fromhex(cleanHex)
         keyBytes = bytes.fromhex(cleanKey)
         ivBytes = bytes.fromhex(cleanIv) if ivIn else b""
    except ValueError as e:
         print(f"Error: Not valid hex string. Details: {e}")
         return None

    # Validate block length
    if len(cipherBytes) % 16 != 0:
         print(f"Error: Cipher length is not a multiple of 16.")
         return None

    # 3. Decrypt raw blocks (No unpad function used here)
    try:
        if mode.upper() == "CBC":
            cipher = AES.new(keyBytes, AES.MODE_CBC, iv=ivBytes)
        elif mode.upper() == "ECB":
            cipher = AES.new(keyBytes, AES.MODE_ECB)
        else:
            return "Error: Unsupported mode."

        # Process raw decryption
        rawDecrypt = cipher.decrypt(cipherBytes)

        # 4. Safe trailing padding removal
        # Checks if the block ends with valid padding bytes (like \x04\x04\x04\x04)
        last_byte = rawDecrypt[-1]
        if 1 <= last_byte <= 16:
            # Verify if all padding bytes match the padding value
            if all(b == last_byte for b in rawDecrypt[-last_byte:]):
                rawDecrypt = rawDecrypt[:-last_byte]

        # 5. Decode output
        try:
            decodedText = rawDecrypt.decode("utf-8")
            print(decodedText)
            return decodedText
        except UnicodeDecodeError:
            return f"Raw Data (Hex): {rawDecrypt.hex()}"

    except Exception as e:
        print(f"Decryption Failed. Error: {e}")
        return None

returnMenu = False

def beginDecrypt():
        global returnMenu
        while returnMenu == False:
            clearConsole()
            setTopCenter()
            print("\n\n")
            print("    1) AES-128 ECB")
            print("    2) AES-128 CBC")
            print("    0) Return to Menu")
            print("\n")
            userChoice = input("    Input Requested > ")
            match userChoice:
                case "1":
                    userHex = input("    Enter Code (hex) > ")
                    userKey = input("    Enter Key (hex) > ")
                    decrypt(userHex, userKey, "ECB")
                    waitKey()
                case "2":
                    userHex = input("    Enter Code (hex) > ")
                    userKey = input("    Enter Key (hex) > ")
                    userIV = input("    Enter IV (hex) > ")
                    decrypt(userHex, userKey, "ECB", userIV)
                    waitKey()
                case "0":
                    returnMenu = True
                case _:
                    print("Unknown entry. ", end="")
                    waitKey()