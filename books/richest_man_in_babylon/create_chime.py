import os
from pydub import AudioSegment
from pydub.generators import Sine

def make_bell(freq, duration_ms, volume_db=-10):
    """
    Simulate a realistic bell by layering the fundamental + overtones,
    with a sharp attack and long natural decay.
    """
    # Real bells have a fast attack and very slow exponential decay
    # Layer fundamental + 2nd, 3rd, 4th harmonics at lower volumes
    fundamental = Sine(freq).to_audio_segment(duration=duration_ms)
    harmonic2   = Sine(freq * 2.76).to_audio_segment(duration=duration_ms) - 6
    harmonic3   = Sine(freq * 5.40).to_audio_segment(duration=duration_ms) - 12
    harmonic4   = Sine(freq * 8.93).to_audio_segment(duration=duration_ms) - 16

    bell = fundamental.overlay(harmonic2).overlay(harmonic3).overlay(harmonic4)

    # Sharp attack (5ms), then very long fade out = natural bell decay
    bell = bell.fade_in(5).fade_out(int(duration_ms * 0.9))
    bell = bell + volume_db
    return bell

def generate_soft_bell_E():
    """Single soft bell - E4 (329 Hz) - warm, low, 4 seconds"""
    bell = make_bell(329.63, 4000, volume_db=-12)
    bell.export("chime_E_soft_low.mp3", format="mp3")
    print("Generated chime_E_soft_low.mp3")

def generate_soft_bell_F():
    """Single soft bell - A4 (440 Hz) - classic pitch, 4 seconds"""
    bell = make_bell(440.00, 4000, volume_db=-12)
    bell.export("chime_F_soft_mid.mp3", format="mp3")
    print("Generated chime_F_soft_mid.mp3")

def generate_soft_bell_G():
    """Soft bell - C5 (523 Hz) - brighter, crisp, 4 seconds"""
    bell = make_bell(523.25, 4000, volume_db=-12)
    bell.export("chime_G_soft_bright.mp3", format="mp3")
    print("Generated chime_G_soft_bright.mp3")

def generate_soft_bell_H():
    """Two-tone monastery bell - low then high, very soft, meditative"""
    bell1 = make_bell(220.00, 3000, volume_db=-12) # A3 - deep
    silence = AudioSegment.silent(duration=800)
    bell2 = make_bell(440.00, 3000, volume_db=-14) # A4 - same note, octave up
    chime = bell1 + silence + bell2
    chime.export("chime_H_monastery.mp3", format="mp3")
    print("Generated chime_H_monastery.mp3")

if __name__ == "__main__":
    generate_soft_bell_E()
    generate_soft_bell_F()
    generate_soft_bell_G()
    generate_soft_bell_H()
    print("Done! 4 soft long bell samples generated.")
