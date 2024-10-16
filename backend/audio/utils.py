import io
from openai import OpenAI

def transcribes_audio_into_text(audio):
    client = OpenAI()

    valid_formats = ['audio/flac', 'audio/m4a', 'audio/mp3', 'audio/mp4', 'audio/mpeg', 'audio/mpga', 'audio/oga',
                     'audio/ogg', 'audio/wav', 'audio/webm']
    if audio.content_type not in valid_formats:
        raise ValueError("Unsupported file format.")

    audio_file = io.BytesIO(audio.read())
    audio_file.name = audio.name
    audio_file.content_type = audio.content_type

    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
    )
    transcript_text = transcription.text

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user',
             'content': f"Транскрипція аудіо: {transcript_text}. Розділи цей текст на короткі смислові промти"},
        ]
    )

    output = response.choices[0].message.content
    re_output = output.split('\n')
    filtered = list(filter(None, re_output))
    return filtered
