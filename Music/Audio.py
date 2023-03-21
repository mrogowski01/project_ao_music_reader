from pysine import sine
import json
from Music.Notes import Notes
import threading

class Audio:
    def __init__(self):
        self.samples = {}
        # self.notes = notes
        # self.durations = durations
        self.loadFrequencies()
        self.event = threading.Event()
        self.musicThread = None

    def loadFrequencies(self):
        with open('Music/frequencies.json') as f:
            self.samples = json.load(f)

    def set(self, notes, durations):
        self.notes = notes
        self.durations = durations

    def setEvent(self):
        self.event.set()

    def play(self, playButton, stopButton, rate):
        self.musicThread = threading.Thread(target=self._play, args=(self.event, playButton, stopButton, rate ))
        self.musicThread.start()

    def stop(self):
        # try:
        self.setEvent()
        self.musicThread.join()
        self.event.clear()
        # except:
            # print("Error - during pressing stop button")
        # self.event.wait()

    def _play(self, event, playButton, stopButton, rate):
        oneBeat = 120 / rate
        print("Start playing music")
        for i in range(len(self.notes)):
            if event.is_set(): 
                print("Terminating music")
                return
            freq = self.samples.get(self.notes[i], None) 
            # if freq is None: raise Exception("The specified sound does not exist")
            if freq is None: freq = 0
            sine(frequency=freq, duration=self.durations[i].value[0] * oneBeat)
        
        playButton.setEnabled(True)
        stopButton.setEnabled(False)
        print("End of music")