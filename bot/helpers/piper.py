import sys
import time
import wave
import logging
from pathlib import Path
from piper import PiperVoice
from typing import Any, Dict, Generator, Tuple, Union
from piper.download import ensure_voice_exists, get_voices


async def ptts(
    text: str,
    model: str,
    output_file: str,
    data_dir=[str(Path.cwd())],
    download_dir="",
    output_dir="",
    output_raw=False,
    debug=False,
    use_cuda=False,
    update_voices=False,
    speaker=0,
    length_scale=0.0,
    noise_scale=0.0,
    noise_w=0.0,
    sentence_silence=0.0,
):
    _LOGGER = logging.getLogger(Path(__file__).stem)
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    _LOGGER.debug(ptts)
    if not download_dir:
        # Download to first data directory by default
        download_dir = data_dir
    model_path = Path(model)
    data_dirs = Path(data_dir).glob("*.onnx")
    for d in data_dirs:
        print(d)
    if not model_path.exists():
        # Load voice info
        voices_info = get_voices(download_dir, update_voices=update_voices)

        # Resolve aliases for backwards compatibility with old voice names
        aliases_info: Dict[str, Any] = {}
        for voice_info in voices_info.values():
            for voice_alias in voice_info.get("aliases", []):
                aliases_info[voice_alias] = {"_is_alias": True, **voice_info}

        voices_info.update(aliases_info)
        ensure_voice_exists(
            model,
            data_dirs=data_dirs,
            download_dir=download_dir,
            voices_info=voices_info,
        )

        model_path, config_path = _find_voice(model, data_dirs=data_dirs)
        print(model_path)

    # Load voice
    voice = PiperVoice.load(
        model_path, config_path=config_path, use_cuda=use_cuda
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

            _LOGGER.info("Wrote %s", wav_path)
    else:
        if (not output_file) or (output_file == "-"):
            # Write to stdout
            with wave.open(sys.stdout.buffer, "wb") as wav_file:
                voice.synthesize(text, wav_file, **synthesize_args)
        else:
            # Write to file
            with wave.open(output_file, "wb") as wav_file:
                voice.synthesize(text, wav_file, **synthesize_args)


def _find_voice(
    name: str, data_dirs: Generator[Union[str, Path]]
) -> Tuple[Path, Path]:
    for data_dir in data_dirs:
        data_dir = Path(data_dir)
        onnx_path = data_dir / f"{name}.onnx"
        config_path = data_dir / f"{name}.onnx.json"

        if onnx_path.exists() and config_path.exists():
            return onnx_path, config_path

    raise ValueError(f"Missing files for voice {name}")


def get_model(lang="es_es", gender="female") -> str:
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
