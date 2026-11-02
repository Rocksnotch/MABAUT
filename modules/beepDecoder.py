from pathlib import Path
import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal


def tones_active_at(time_slot, time_column_list, tone_power, tones, time_window):
    # grabs the time index that is closest to the wanted time
    time_index = np.argmin(abs(time_column_list - time_slot))
    
    # all spectrogram columns that fall inside the window around time_slot
    mask = (time_column_list >= time_slot - time_window) & (time_column_list <= time_slot + time_window)
    
    # grabs the avg power of each tone in the window
    avg_power = tone_power[:, mask].mean(axis=1)

    on_threshold = 0.5 * avg_power.max() # so far there has always been at least one on


    tone_frequency_power_pairs = list(zip(tones, avg_power))
    
    # returns the tones that are on at that time slot
    return [tone_frequency for tone_frequency, tone_power in tone_frequency_power_pairs if tone_power > on_threshold]


def decodeBeeps(input_audio_file_path):
    input_audio = Path(input_audio_file_path)

    sample_rate, data = wavfile.read(input_audio)
    frequency_list, time_column_list, spectrogram = signal.spectrogram(data.astype(float), fs=sample_rate, nperseg=4096)

    # takes the readings at 244 500 750 1000 1250 1500 1750
    # converts them to ascii

    tones = [250, 500, 750, 1000, 1250, 1500, 1750] # all the main bit tones


    # maps the tones to the indexes in the spectrogram
    # grabs the index that is closest to the frequency of each tone
    tone_indexes = [np.argmin(abs(frequency_list - tone)) for tone in tones]

    # grab the power of the tones at each time slot
    tone_power = spectrogram[tone_indexes, :]

    # the start time
    start_time = 0
    # the beep length
    beep_length = 0.2

    # time around the middle of the beeep to find the active tones
    time_window = 0.05

    # the number of beeps in the video
    duration = len(data) / sample_rate
    number_of_slots = round((duration - start_time) / beep_length)

    bytes_array = []
    text = ""
    for beep_number in range(number_of_slots):
        # middle of the beep
        time_slot = start_time + beep_number * beep_length + beep_length / 2
        
        active_tones = tones_active_at(time_slot, time_column_list, tone_power, tones, time_window)
        
        # remake the binary string from the active tones
        bits = "".join("1" if tone in active_tones else "0" for tone in tones)
        bytes_array.append("0" + bits)
        
        # convert the binary string to int
        code = int(bits, 2)
        
        REPLACEMENT_CHAR = 0xFFFD # used for invalid characters
        text += chr(code) if 32 <= code < 127 else chr(REPLACEMENT_CHAR)


    split_text_array = []
    split_byte_array = []
    
    header_beeps_repeat = 8
    
    
    headers = look_for_header_indexes(bytes_array, "01111111", header_beeps_repeat) # the header is 01111111 which leads and ends each part
    
    while len(headers) > 0:
        header_index = headers.pop(0)
        if len(headers) > 0:
            next_header_index = headers[0]
            split_byte_array.append(bytes_array[header_index+header_beeps_repeat:next_header_index])
            split_text_array.append(text[header_index+header_beeps_repeat:next_header_index])
    

    return split_byte_array, split_text_array


def look_for_header_indexes(bytes_array: list[str], header: str, header_beeps: int) -> list[int]:
    """
    returns all positions of the header in the bytes_array
    """
    header = header*header_beeps
    
    header_indexes = []
    for index, binary in enumerate(bytes_array):
        
        full_header = "".join(bytes_array[index:index+header_beeps])
        if full_header == header:
            header_indexes.append(index)
    return header_indexes


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("give file path")
        sys.exit(1)
    
    bytes_array, text = decodeBeeps(sys.argv[1])
    print("decoded bytes:", bytes_array)
    print("decoded text:", text)
