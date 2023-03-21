import numpy
import pyaudio
import math
import json
from Music.Notes import Notes
 
 
class Audio():
    def __init__(self, samplerate=44100, frames_per_buffer=4410):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False
        self.samples = {}
        self.loadFrequencies()

    def loadFrequencies(self):
        with open('Music/frequencies.json') as f:
            self.samples = json.load(f)
            # for k, v in data.items():
                # self.samples[k] = v
 
    def sinewave(self):
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            # We don't need a full buffer or audio so pad the end with 0's
            xs = numpy.arange(self.buffer_offset,
                              self.x_max)
            tmp = self.amplitude * numpy.sin(xs * self.omega)
            out = numpy.append(tmp,
                               numpy.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = numpy.arange(self.buffer_offset,
                              self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * numpy.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer
        return out
 
    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(numpy.float32)
            return (data.tostring(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)
 
    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False
 
    def play(self, sound, notename=Notes.QUARTER_NOTE, amplitude = 0.5):
        freq = self.samples.get(sound, None) 
        if freq is None: raise Exception("The specified sound does not exist")

        self.omega = float(freq) * (math.pi * 2) / self.samplerate
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * notename.value[0]) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.samplerate, output=True, frames_per_buffer=self.frames_per_buffer, stream_callback=self.callback)