from collections import Counter
from instructions import Instructions
import exceptions
import logging
import queue
import speech_recognition as sr

r = sr.Recognizer()

# After this amount of silence, run recognition
r.pause_threshold = 0.1

# Amount of non-speech audio to keep in audio sample
r.non_speaking_duration = 0.1

# Words to listen for. 0-1 is the sensitivity
KEYWORDS = [("up", 1), ("down", 1), ("left", 1), ("right", 1)]

# Queue for direction results. The recognizer runs on a separate thread and puts results on this queue
direction_queue = queue.Queue()

# Cmd to instruction
DIRECTION_TO_INSTRUCTION = {
    "left": Instructions.TURN_LEFT,
    "right": Instructions.TURN_RIGHT,
}


def callback(recognizer, audio):  # this is called from the background thread

    speech_as_text = ""
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=KEYWORDS)
        speech_as_text = speech_as_text.strip()
        logging.debug(speech_as_text)
    except sr.UnknownValueError:
        pass

    # Sphinx often doesn't cleanly recognize the word spoken, or recognizes more than one
    # We do some processing to make sense of the recognized words.
    frequency_list = Counter(speech_as_text.split()).most_common()

    # If there was only one word recognized (probably "up"), use it
    if len(frequency_list) == 1:
        direction = frequency_list[0][0]
        direction_queue.put(direction)
    # If there was more than one, prefer the last one that is not "up" because "up" is often mis-recognized
    elif len(frequency_list) > 1:
        count = len(frequency_list)
        last = frequency_list[count-1][0]
        if not last == "up":
            direction_queue.put(last)
        else:
            second_last = frequency_list[count-2][0]
            direction_queue.put(second_last)


def start_recognizer():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
    stop_listening = r.listen_in_background(source, callback)


def get_instruction():
    direction = None
    try:
        direction = direction_queue.get_nowait()
    except queue.Empty:
        pass

    if direction in DIRECTION_TO_INSTRUCTION:
        return DIRECTION_TO_INSTRUCTION[direction]

    raise exceptions.NoInputException


start_recognizer()
