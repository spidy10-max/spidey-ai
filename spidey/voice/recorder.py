"""
Spidey AI — Audio Recorder
Records audio from microphone
"""
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import time
from datetime import datetime
from spidey.config import DATA_DIR
from spidey.logger import app_logger, log_event, log_error


AUDIO_DIR = os.path.join(DATA_DIR, "audio")


class AudioRecorder:
    """Records audio from microphone"""

    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.audio_data = []
        os.makedirs(AUDIO_DIR, exist_ok=True)
        app_logger.info("AudioRecorder initialized")

    def record_fixed(self, duration=5):
        """Record for fixed duration"""
        print(f"   🎤 Recording for {duration} seconds...")
        print(f"   🎤 Speak now!", end=" ", flush=True)

        try:
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32"
            )
            sd.wait()
            print("✅ Done!")

            filepath = self._save_audio(audio)
            log_event("Audio recorded", f"{duration}s → {filepath}")
            return filepath

        except Exception as e:
            log_error(str(e), "AudioRecorder.record_fixed")
            print(f"\n   ❌ Recording error: {e}")
            return None

    def record_until_enter(self):
        """Record until user presses Enter"""
        print("   🎤 Recording... Press ENTER to stop.")
        print("   🎤 Speak now!")

        self.audio_data = []
        self.is_recording = True

        try:
            stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                callback=self._audio_callback
            )

            stream.start()
            input()
            stream.stop()
            stream.close()
            self.is_recording = False

            if not self.audio_data:
                print("   ❌ No audio recorded.")
                return None

            audio = np.concatenate(self.audio_data, axis=0)
            duration = len(audio) / self.sample_rate
            print(f"   ✅ Recorded {round(duration, 1)} seconds")

            filepath = self._save_audio(audio)
            log_event("Audio recorded", f"{round(duration, 1)}s")
            return filepath

        except Exception as e:
            log_error(str(e), "AudioRecorder.record_until_enter")
            print(f"\n   ❌ Recording error: {e}")
            self.is_recording = False
            return None

    def record_with_silence_detection(self, max_duration=30, silence_threshold=0.01, silence_duration=2.0):
        """Record and auto-stop on silence"""
        print("   🎤 Recording... (auto-stops on silence)")
        print("   🎤 Speak now!")

        try:
            audio_chunks = []
            silence_start = None
            start_time = time.time()

            stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                blocksize=int(self.sample_rate * 0.1)
            )

            stream.start()

            while True:
                data, overflowed = stream.read(int(self.sample_rate * 0.1))
                audio_chunks.append(data.copy())

                volume = np.abs(data).mean()

                if volume < silence_threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > silence_duration:
                        print("\n   🔇 Silence detected — stopping.")
                        break
                else:
                    silence_start = None

                elapsed = time.time() - start_time
                if elapsed >= max_duration:
                    print(f"\n   ⏰ Max duration ({max_duration}s) reached.")
                    break

            stream.stop()
            stream.close()

            if not audio_chunks:
                print("   ❌ No audio recorded.")
                return None

            audio = np.concatenate(audio_chunks, axis=0)
            duration = len(audio) / self.sample_rate
            print(f"   ✅ Recorded {round(duration, 1)} seconds")

            filepath = self._save_audio(audio)
            log_event("Audio recorded (auto-stop)", f"{round(duration, 1)}s")
            return filepath

        except Exception as e:
            log_error(str(e), "AudioRecorder.record_with_silence")
            print(f"\n   ❌ Recording error: {e}")
            return None

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for streaming recording"""
        if self.is_recording:
            self.audio_data.append(indata.copy())

    def _save_audio(self, audio_data):
        """Save audio to WAV file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(AUDIO_DIR, f"recording_{timestamp}.wav")
        sf.write(filepath, audio_data, self.sample_rate)
        return filepath

    def list_microphones(self):
        """List available microphones"""
        devices = sd.query_devices()
        mics = []
        for i, device in enumerate(devices):
            if device["max_input_channels"] > 0:
                mics.append({
                    "id": i,
                    "name": device["name"],
                    "channels": device["max_input_channels"],
                    "sample_rate": device["default_samplerate"]
                })
        return mics

    def test_microphone(self, duration=2):
        """Quick mic test"""
        print("   🎤 Testing microphone...")

        try:
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32"
            )
            sd.wait()

            volume = np.abs(audio).mean()
            max_volume = np.abs(audio).max()

            print(f"   📊 Average volume: {round(volume, 4)}")
            print(f"   📊 Max volume: {round(max_volume, 4)}")

            if max_volume > 0.01:
                print("   ✅ Microphone is working!")
                return True
            else:
                print("   ⚠️ Very low volume. Check microphone.")
                return False

        except Exception as e:
            print(f"   ❌ Microphone error: {e}")
            return False