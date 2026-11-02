from pathlib import Path
import numpy as np



# All the main bit tones
TONES = [250, 500, 750, 1000, 1250, 1500, 1750]

def _tonesActiveAtTime(middleOfBeepInSeconds, timeColumns, tonePower, timeWindow):
    
    
    # All spectrogram columns that fall inside the window around middleOfBeepInSeconds
    timeWindowMask: list[bool] = (timeColumns >= middleOfBeepInSeconds - timeWindow) & (timeColumns <= middleOfBeepInSeconds + timeWindow)
        
    # Grabs the avg power of each tone in the window
    avgPower = tonePower[:, timeWindowMask].mean(axis=1)

    # So far there has always been at least one bit on
    # Grab the highest power seen on a single tone
    onThreshold = 0.5 * avgPower.max() 

    # Pair each tone with its average power
    toneFrequencyPowerPairs = list(zip(TONES, avgPower))
    
    # Returns the tones that are on at that time slot
    return [toneFrequency for toneFrequency, tonePower in toneFrequencyPowerPairs if tonePower > onThreshold]


def decodeBeeps(inputAudioPath: str | Path, startReadTime: float = 0, beepLength: float = 0.2, timeWindow: float = 0.05):
    inputAudioPath = Path(inputAudioPath)
    
    # Check if the file exists
    if not inputAudioPath.is_file():
        print(f"File not found: {inputAudioPath}")
        return None, None
    
    # Check if scipy is installed
    try:
        import scipy.io.wavfile as wavfile
        import scipy.signal as signal
    except ImportError:
        print("scipy is required for decoding beeps")
        return None, None
    
    # The time to start reading the beeps from
    startReadTime = startReadTime
    # The length of each beep in seconds
    beepLength = beepLength
    # Time around the middle of the beeep to find the active tones
    timeWindow = timeWindow

    sampleRate, audioData = wavfile.read(inputAudioPath)
    
    frequencyRows, timeColumns, spectrogram = signal.spectrogram(audioData.astype(float), fs=sampleRate, nperseg=4096)


    # Maps the tones to the indexes in the spectrogram
    # Grabs the index that is closest to the frequency of each tone
    toneToSpectrogramMappings = [np.argmin(abs(frequencyRows - tone)) for tone in TONES]

    # Grab the power as a row for each tone in TONES
    powerRows = spectrogram[toneToSpectrogramMappings, :]



    # The durration of the audio in seconds
    duration = len(audioData) / sampleRate
    
    # the number of beeps in the audio file
    numberOfSlots = round((duration - startReadTime) / beepLength)

    rawDecodedBinary = []
    rawDecodedText = ""
    for beepNumber in range(numberOfSlots):
        
        
        beepOffset = beepNumber * beepLength
        
        # get the Middle of the beep
        middleOfBeepInSeconds = startReadTime + beepOffset + beepLength / 2
        
        # Get the active tones
        activeTonesAtTime = _tonesActiveAtTime(middleOfBeepInSeconds, timeColumns, powerRows, timeWindow)
        
        # Remake the binary string from the active tones
        bits = "".join("1" if tone in activeTonesAtTime else "0" for tone in TONES)
        rawDecodedBinary.append("0" + bits)
        
        # Convert the binary string to int
        code = int(bits, 2)
        
        REPLACEMENT_CHAR = 0xFFFD # used for invalid characters
        rawDecodedText += chr(code) if 32 <= code < 127 else chr(REPLACEMENT_CHAR)


    headerSplitText = []
    headerSplitBytes = []
    
    headerRepeatAmount = 8
    
    # The header is 01111111 which leads and ends each part
    headers = _look_for_header_indexes(rawDecodedBinary, "01111111", headerRepeatAmount) 
    
    while len(headers) > 0:
        headerIndex = headers.pop(0)
        if len(headers) > 0:
            nextHeaderIndex = headers[0]
            headerSplitBytes.append(rawDecodedBinary[headerIndex+headerRepeatAmount:nextHeaderIndex])
            headerSplitText.append(rawDecodedText[headerIndex+headerRepeatAmount:nextHeaderIndex])
    

    return headerSplitBytes, headerSplitText


def _look_for_header_indexes(listOfBinaryBytes: list[str], header: str, headerBeeps: int) -> list[int]:
    """
    Returns all positions of the header in the bytes_array
    """
    header = header*headerBeeps
    
    headerIndexes = []
    for index, binary in enumerate(listOfBinaryBytes):
        
        fullHeader = "".join(listOfBinaryBytes[index:index+headerBeeps])
        if fullHeader == header:
            headerIndexes.append(index)
    return headerIndexes


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Needs full path to the audio file")
        sys.exit(1)
    
    bytes_array, text = decodeBeeps(sys.argv[1])
    print("Decoded bytes:", bytes_array)
    print("Decoded text:", text)
