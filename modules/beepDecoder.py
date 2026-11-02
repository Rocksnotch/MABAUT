from pathlib import Path
import numpy as np


def _tones_active_at(timeSlot, timeColumnList, tonePower, tones, timeWindow):
    # Grabs the time index that is closest to the wanted time
    timeIndex = np.argmin(abs(timeColumnList - timeSlot))
    
    # All spectrogram columns that fall inside the window around time_slot
    mask = (timeColumnList >= timeSlot - timeWindow) & (timeColumnList <= timeSlot + timeWindow)
    
    # Grabs the avg power of each tone in the window
    avgPower = tonePower[:, mask].mean(axis=1)

    # So far there has always been at least one bit on
    onThreshold = 0.5 * avgPower.max() 

    # Pair each tone with its average power
    toneFrequencyPowerPairs = list(zip(tones, avgPower))
    
    # Returns the tones that are on at that time slot
    return [toneFrequency for toneFrequency, tonePower in toneFrequencyPowerPairs if tonePower > onThreshold]


def decodeBeeps(inputAudioPath):
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
    
    
    sampleRate, audioData = wavfile.read(inputAudioPath)
    frequencyList, timeColumnList, spectrogram = signal.spectrogram(audioData.astype(float), fs=sampleRate, nperseg=4096)

    # All the main bit tones
    tones = [250, 500, 750, 1000, 1250, 1500, 1750] 


    # Maps the tones to the indexes in the spectrogram
    # Grabs the index that is closest to the frequency of each tone
    toneIndexes = [np.argmin(abs(frequencyList - tone)) for tone in tones]

    # Grab the power of the tones at each time slot
    tonePower = spectrogram[toneIndexes, :]

    # The start time
    startReadTime = 0
    # The beep length
    beepLength = 0.2

    # Time around the middle of the beeep to find the active tones
    timeWindow = 0.05

    # The number of beeps in the video
    duration = len(audioData) / sampleRate
    numberOfSlots = round((duration - startReadTime) / beepLength)

    bytesArray = []
    text = ""
    for beepNumber in range(numberOfSlots):
        # Middle of the beep
        timeSlot = startReadTime + beepNumber * beepLength + beepLength / 2
        
        activeTonesAtTimeSlot = _tones_active_at(timeSlot, timeColumnList, tonePower, tones, timeWindow)
        
        # Remake the binary string from the active tones
        bits = "".join("1" if tone in activeTonesAtTimeSlot else "0" for tone in tones)
        bytesArray.append("0" + bits)
        
        # Convert the binary string to int
        code = int(bits, 2)
        
        REPLACEMENT_CHAR = 0xFFFD # used for invalid characters
        text += chr(code) if 32 <= code < 127 else chr(REPLACEMENT_CHAR)


    headerSplitText = []
    headerSplitBytes = []
    
    headerRepeatAmount = 8
    
    # The header is 01111111 which leads and ends each part
    headers = _look_for_header_indexes(bytesArray, "01111111", headerRepeatAmount) 
    
    while len(headers) > 0:
        headerIndex = headers.pop(0)
        if len(headers) > 0:
            nextHeaderIndex = headers[0]
            headerSplitBytes.append(bytesArray[headerIndex+headerRepeatAmount:nextHeaderIndex])
            headerSplitText.append(text[headerIndex+headerRepeatAmount:nextHeaderIndex])
    

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
