from collections import Counter
import logging
import queue
import speech_recognition as sr

r = sr.Recognizer()
r.pause_threshold = 0.1
r.non_speaking_duration = 0.1

# Words that sphinx should listen closely for. 0-1 is the sensitivity
# of the wake word.
keywords = [("up", 1), ("down", 1), ("left", 1), ("right", 1)]

# Queue for direction results
direction_queue = queue.Queue()


def callback(recognizer, audio):  # this is called from the background thread

    speech_as_text = ""
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
        speech_as_text = speech_as_text.strip()
        logging.info(speech_as_text)
    except sr.UnknownValueError:
        pass

    frequency_list = Counter(speech_as_text.split()).most_common()

    if len(frequency_list) == 1:
        # If there was only one word recognized (probably "up"), use it
        direction = frequency_list[0][0]
        direction_queue.put(direction)
    elif len(frequency_list) > 1:
        # If there was more than one, prefer the last one that is not "up"
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


def get_direction():
    try:
        direction = direction_queue.get_nowait()
        return direction
    except queue.Empty:
        return None


start_recognizer()
