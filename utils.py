import pyttsx3
import speech_recognition as sr
import re # Added missing import for re

def speak(text):
    """
    Converts text to speech.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """
    Listens to user's voice input and converts it to text.
    """
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("🎙️ Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        try:
            query = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {query}")
            return query
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"❌ Could not request results from Google Speech Recognition: {e}")
            return ""
    except Exception as e:
        print(f"❌ Error with microphone: {e}")
        return ""

def filter_by_budget(products, budget):
    """
    Filters the list of products to only include those under the given budget.
    Handles price as either int or string.
    """
    filtered = []
    try:
        budget = int(budget)  # Convert budget to int
    except (ValueError, TypeError):
        return filtered  # If conversion fails, return empty list

    for product in products:
        try:
            # Check if price is already an integer, if not, convert from string
            if isinstance(product["price"], int):
                price = product["price"]
            else:
                # Clean price string and convert to int
                price = int("".join(filter(str.isdigit, str(product["price"]))))
            
            if price <= budget:
                filtered.append(product)
        except (KeyError, ValueError, TypeError): # Catch errors if 'price' key is missing or conversion fails
            continue
    return filtered

def shorten_title(title, max_words=8):
    """
    Shortens a product title to a maximum number of words.
    """
    words = title.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return title