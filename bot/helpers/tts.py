import os
import sys
import time
import wave
import logging
from pathlib import Path
from typing import Any, Dict
from piper import PiperVoice
from piper.download import ensure_voice_exists, find_voice, get_voices

current_dir = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(current_dir, "../models")


async def tts(text: str, output_file: str):
    model = _get_model()
    try:
        if not os.path.exists(models):
            os.makedirs(models)
        elif not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        await _ptts(
            text=text,
            model=model,
            data_dirs=models,
            download_dir=models,
            output_file=output_file,
        )
    except Exception as e:
        logging.error(e)
        raise e


def _get_model(lang="es_es", gender="female") -> str:
    mdn = ""
    if gender == "female":
        match lang.lower():
            case "en_us":
                mdn += "en_US-amy-medium"
            case "en_gb":
                mdn += "en_GB-alba-medium"
            case "es_es":
                mdn += "es_ES-davefx-medium"
            case "es_mx":
                mdn += "es_MX-ald-medium"
            case "fr_fr":
                mdn += "fr_FR-siwis-medium"
            case "pt_br":
                mdn += "pt_BR-faber-medium"
            case "pt_pt":
                mdn += "pt_PT-tugão-medium"
            case "ru_ru":
                mdn += "ru_RU-irina-medium"
        return mdn
    if gender == "male":
        match lang.lower():
            case "en_us":
                mdn += "en_US-amy-medium"
            case "en_gb":
                mdn += "en_GB-alba-medium"
            case "es_es":
                mdn += "es_ES-davefx-medium"
            case "es_mx":
                mdn += "es_MX-ald-medium"
            case "fr_fr":
                mdn += "fr_FR-siwis-medium"
            case "pt_br":
                mdn += "pt_BR-faber-medium"
            case "pt_pt":
                mdn += "pt_PT-tugão-medium"
            case "ru_ru":
                mdn += "ru_RU-irina-medium"
        return mdn
    return ValueError("Wrong country code, not found model")


async def _ptts(
    text: str,
    model: str,
    data_dirs: str,
    download_dir: str,
    output_file: str,
    output_dir="",
    output_raw="",
    use_cuda=False,
    update_voices=False,
    speaker="",
    length_scale="",
    noise_scale="",
    noise_w="",
    sentence_silence="",
):
    mdp = Path(model)
    if not mdp.exists():
        # Load voice info
        voices_info = get_voices(
            download_dir=download_dir, update_voices=update_voices
        )

        # Resolve aliases for backwards compatibility with old voice names
        aliases_info: Dict[str, Any] = {}
        for voice_info in voices_info.values():
            for voice_alias in voice_info.get("aliases", []):
                aliases_info[voice_alias] = {"_is_alias": True, **voice_info}

        voices_info.update(aliases_info)
        ensure_voice_exists(
            name=model,
            data_dirs=data_dirs,
            download_dir=download_dir,
            voices_info=voices_info,
        )
        model_path, config_path = find_voice(name=model, data_dirs=data_dirs)
        print(model_path)
    # Load voice
    voice = PiperVoice.load(
        model_path=model_path, config_path=config_path, use_cuda=use_cuda
    )
    synthesize_args = {
        "speaker_id": speaker,
        "length_scale": length_scale,
        "noise_scale": noise_scale,
        "noise_w": noise_w,
        "sentence_silence": sentence_silence,
    }
    if output_raw:
        # Read line-by-line
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            # Write raw audio to stdout as its produced
            audio_stream = voice.synthesize_stream_raw(line, **synthesize_args)
            for audio_bytes in audio_stream:
                sys.stdout.buffer.write(audio_bytes)
                sys.stdout.buffer.flush()
    elif output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Read line-by-line
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            wav_path = output_dir / f"{time.monotonic_ns()}.wav"
            with wave.open(str(wav_path), "wb") as wav_file:
                voice.synthesize(line, wav_file, **synthesize_args)

            logging.info("Wrote %s", wav_path)
    else:
        if (not output_file) or (output_file == "-"):
            # Write to stdout
            with wave.open(sys.stdout.buffer, "wb") as wav_file:
                voice.synthesize(text, wav_file, **synthesize_args)
        else:
            # Write to file
            with wave.open(output_file, "wb") as wav_file:
                voice.synthesize(text, wav_file, **synthesize_args)
