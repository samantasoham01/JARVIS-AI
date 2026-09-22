import os
import datetime
import subprocess
import webbrowser
import speech_recognition as sr
from groq import Groq


# ============================================================
# JARVIS SETTINGS
# ============================================================

MODEL = "openai/gpt-oss-20b"

API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    print("ERROR: GROQ_API_KEY is not set.")
    print("Set your Groq API key first.")
    exit()


client = Groq(api_key=API_KEY)


# ============================================================
# SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5


# ============================================================
# JARVIS SPEAK
# ============================================================

def speak(text):

    if not text:
        return

    print("\nJARVIS:", text)

    # PowerShell speech engine
    safe_text = text.replace("'", "''")

    command = f"""
Add-Type -AssemblyName System.Speech
$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voice.Rate = 0
$voice.Volume = 100
$voice.Speak('{safe_text}')
"""

    try:

        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                command
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except Exception as e:

        print("Speech error:", e)


# ============================================================
# MICROPHONE CALIBRATION
# ============================================================

def calibrate_microphone():

    print("\nCalibrating microphone...")

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

        print("Microphone ready.")

    except Exception as e:

        print("Microphone error:", e)


# ============================================================
# LISTEN
# ============================================================

def listen():

    try:

        with sr.Microphone() as source:

            print("\nJARVIS is listening...")

            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=10
            )

        try:

            command = recognizer.recognize_google(
                audio
            )

            command = command.lower().strip()

            print("You:", command)

            return command

        except sr.UnknownValueError:

            print("JARVIS: Sorry, I couldn't understand you.")

            return ""

        except sr.RequestError as e:

            print("Speech recognition error:", e)

            return ""

    except Exception as e:

        print("Microphone error:", e)

        return ""


# ============================================================
# TIME
# ============================================================

def tell_time():

    now = datetime.datetime.now()

    current_time = now.strftime("%I:%M %p")

    print("\nCurrent time:", current_time)

    speak(
        f"The current time is {current_time}."
    )


# ============================================================
# DATE
# ============================================================

def tell_date():

    today = datetime.datetime.now()

    current_date = today.strftime(
        "%A, %d %B %Y"
    )

    print("\nToday's date:", current_date)

    speak(
        f"Today is {current_date}."
    )


# ============================================================
# OPEN CHROME
# ============================================================

def open_chrome():

    print("Opening Chrome...")

    try:

        subprocess.Popen(
            "start chrome",
            shell=True
        )

        speak(
            "Opening Google Chrome."
        )

    except:

        webbrowser.open(
            "https://www.google.com"
        )

        speak(
            "Opening Google."
        )


# ============================================================
# OPEN GOOGLE
# ============================================================

def open_google():

    print("Opening Google...")

    webbrowser.open(
        "https://www.google.com"
    )

    speak(
        "Opening Google."
    )


# ============================================================
# OPEN YOUTUBE
# ============================================================

def open_youtube():

    print("Opening YouTube...")

    webbrowser.open(
        "https://www.youtube.com"
    )

    speak(
        "Opening YouTube."
    )


# ============================================================
# OPEN VS CODE
# ============================================================

def open_vscode():

    print("Opening Visual Studio Code...")

    try:

        subprocess.Popen(
            "code",
            shell=True
        )

        speak(
            "Opening Visual Studio Code."
        )

    except:

        speak(
            "I couldn't open Visual Studio Code."
        )


# ============================================================
# OPEN CALCULATOR
# ============================================================

def open_calculator():

    print("Opening Calculator...")

    try:

        subprocess.Popen(
            "calc.exe"
        )

        speak(
            "Opening Calculator."
        )

    except:

        speak(
            "I couldn't open Calculator."
        )


# ============================================================
# OPEN NOTEPAD
# ============================================================

def open_notepad():

    print("Opening Notepad...")

    try:

        subprocess.Popen(
            "notepad.exe"
        )

        speak(
            "Opening Notepad."
        )

    except:

        speak(
            "I couldn't open Notepad."
        )


# ============================================================
# GROQ AI
# ============================================================

conversation = [

    {
        "role": "system",
        "content": """
You are JARVIS, a personal AI assistant for Soham.

Be friendly, intelligent and helpful.

Keep spoken answers reasonably short and natural.

You can answer:
- General questions
- Programming questions
- C
- C++
- Python
- Mathematics
- Science
- Technology
- College questions
- Normal conversation

Do not pretend to have real-time information unless it
is provided to you.
"""
    }

]


# ============================================================
# ASK GROQ
# ============================================================

def ask_ai(question):

    conversation.append(
        {
            "role": "user",
            "content": question
        }
    )

    print("\nJARVIS AI is thinking...")

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=conversation,

            temperature=0.6,

            max_completion_tokens=500,

            include_reasoning=False
        )

        answer = response.choices[0].message.content

        if not answer:

            answer = "Sorry, I couldn't generate an answer."

        conversation.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer.strip()

    except Exception as e:

        print("\nGROQ ERROR:")
        print(e)

        return (
            "Sorry Soham, I'm having trouble "
            "connecting to my AI brain right now."
        )


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_command(command):

    if not command:

        return True


    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    if (
        command == "stop"
        or "jarvis stop" in command
        or "stop jarvis" in command
        or "shutdown jarvis" in command
        or "exit jarvis" in command
        or "quit jarvis" in command
    ):

        speak(
            "Okay Soham. Goodbye."
        )

        return False


    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    if (
        "what time is it" in command
        or "what is the time" in command
        or "what's the time" in command
        or "tell me the time" in command
        or "current time" in command
        or "time right now" in command
        or "time now" in command
        or command == "time"
        or command.endswith(" time")
    ):

        tell_time()

        return True


    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    if (
        "what is the date" in command
        or "what's the date" in command
        or "tell me the date" in command
        or "today's date" in command
        or "todays date" in command
        or command == "date"
    ):

        tell_date()

        return True


    # --------------------------------------------------------
    # CHROME
    # --------------------------------------------------------

    if (
        "open chrome" in command
        or "launch chrome" in command
        or "start chrome" in command
    ):

        open_chrome()

        return True


    # --------------------------------------------------------
    # GOOGLE
    # --------------------------------------------------------

    if (
        "open google" in command
        or "launch google" in command
        or "start google" in command
    ):

        open_google()

        return True


    # --------------------------------------------------------
    # YOUTUBE
    # --------------------------------------------------------

    if (
        "open youtube" in command
        or "launch youtube" in command
        or "start youtube" in command
    ):

        open_youtube()

        return True


    # --------------------------------------------------------
    # VISUAL STUDIO CODE
    # --------------------------------------------------------

    if (
        "open vs code" in command
        or "open vscode" in command
        or "open visual studio code" in command
        or "launch vs code" in command
        or "start vs code" in command
    ):

        open_vscode()

        return True


    # --------------------------------------------------------
    # CALCULATOR
    # --------------------------------------------------------

    if (
        "open calculator" in command
        or "open calc" in command
        or "launch calculator" in command
    ):

        open_calculator()

        return True


    # --------------------------------------------------------
    # NOTEPAD
    # --------------------------------------------------------

    if (
        "open notepad" in command
        or "launch notepad" in command
    ):

        open_notepad()

        return True


    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if (
        command == "hello"
        or command == "hi"
        or command == "hey"
        or "hello jarvis" in command
        or "hi jarvis" in command
        or "hey jarvis" in command
    ):

        speak(
            "Hello Soham. How can I help you?"
        )

        return True


    # --------------------------------------------------------
    # AI QUESTION
    # --------------------------------------------------------

    answer = ask_ai(command)

    speak(answer)

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 55)
    print("              JARVIS AI ASSISTANT")
    print("=" * 55)
    print()

    print("Model:", MODEL)
    print("Status: Starting...")
    print()


    # --------------------------------------------------------
    # TEST GROQ
    # --------------------------------------------------------

    try:

        test = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "user",
                    "content": "Reply only with Online."
                }
            ],

            max_completion_tokens=20,

            include_reasoning=False
        )

        print(
            "AI Brain:",
            test.choices[0].message.content
        )

    except Exception as e:

        print("\nGROQ CONNECTION ERROR:")
        print(e)

        return


    # --------------------------------------------------------
    # MICROPHONE
    # --------------------------------------------------------

    calibrate_microphone()


    # --------------------------------------------------------
    # STARTUP MESSAGE
    # --------------------------------------------------------

    speak(
        "Hello Soham. I am Jarvis. "
        "Your AI assistant is ready."
    )


    # --------------------------------------------------------
    # CONTINUOUS LOOP
    # --------------------------------------------------------

    while True:

        command = listen()

        if command:

            running = process_command(
                command
            )

            if not running:

                break


# ============================================================
# START JARVIS
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nJARVIS stopped by keyboard.")

    except Exception as e:

        print("\nPROGRAM ERROR:")
        print(e)