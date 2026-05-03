import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio

load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()


async def text_to_speech(text, instructions) -> None:

    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
        instructions=instructions,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:  # Mic Access
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2
        print("Say something!")
        audio = r.listen(source)
        # recognize speech using Google Speech Recognition
    try:
        transcript = r.recognize_google(audio)
        print("You said : \n\n" + transcript)
        SYSTEM_PROMPT = """
You are an expert voice agent . You are given the transcript of what user has said using voice .
You need to output as if you were an voice agent and whatever you speak will be converted back to audio using AI and played back to user .

"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": transcript},
                {"role": "system", "content": SYSTEM_PROMPT},
            ],
        )
        text = response.choices[0].message.content
        instructions = """Tone : Calm Old man"""
        print("AI Response :  \n\n", text)
        asyncio.run(text_to_speech(text=text, instructions=instructions))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )


main()
