import numpy as np
from scipy.io import wavfile
from scipy.signal import chirp


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def encode_audio(input_audio_path, message, output_audio_path, seed=42):
    # Read the input audio file
    rate, data = wavfile.read(input_audio_path)
    if data.dtype != np.int16:
        raise ValueError("Audio file must be 16-bit PCM.")

    # Convert message to binary
    message_bits = text_to_bits(message) + '11111111'

    # Generate a pseudo-random noise sequence
    np.random.seed(seed)
    noise = np.random.normal(0, 1, len(data))

    # Modulate the message into the noise
    modulated_signal = np.zeros_like(data, dtype=np.float32)
    bit_length = len(data) // len(message_bits)

    for i, bit in enumerate(message_bits):
        if bit == '1':
            modulated_signal[i * bit_length:(i + 1) * bit_length] = noise[i * bit_length:(i + 1) * bit_length]

    # Normalize and add the modulated signal to the original audio
    max_int16 = np.iinfo(np.int16).max
    modulated_signal = modulated_signal / np.max(np.abs(modulated_signal)) * max_int16 * 0.01  # Modulation index
    new_audio = data.astype(np.float32) + modulated_signal
    new_audio = np.clip(new_audio, -max_int16, max_int16).astype(np.int16)

    # Save the output audio file
    wavfile.write(output_audio_path, rate, new_audio)


# Example usage:
encode_audio(r'C:\Users\colek\OneDrive\Desktop\Stegonagraphy_1.wav', 'Super Secret Message', r'C:\Users\colek\OneDrive\Desktop\Stegonagraphy_2.wav')
