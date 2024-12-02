import warnings
from fuzzywuzzy import fuzz
import re

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

import whisper
model = whisper.load_model("base")

specialWords = True

AUDIO = "story.mp3"
transcript = model.transcribe(
    word_timestamps=True,
    audio=AUDIO
)

with open('inputText.txt', 'r') as file:
    lines = file.readlines()
content = ''.join(lines)
content = content.replace('-', ' ')
words = content.split()

def clean_word_for_comparison(word):
    word = re.sub(r'[^\w\s]', '', word)
    return word.strip().lower()

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = round(seconds % 60, 3)
    return f"{hours:02}:{minutes:02}:{seconds:05.3f}".replace('.', ',')

def find_best_match(current_word, context_words):
    cleaned_current_word = clean_word_for_comparison(current_word)
    
    best_match = current_word
    best_index = 0
    highest_similarity = 0
    
    for i, candidate in enumerate(context_words):
        cleaned_candidate = clean_word_for_comparison(candidate)
        
        similarity = fuzz.ratio(cleaned_current_word, cleaned_candidate)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = candidate
            best_index = i
    return best_match, best_index

srt_counter = 1  # For numbering subtitles
list_index = 0   

with open('subtitles.srt', 'w') as srt_file:
    for segment in transcript['segments']:
        for word in segment['words']:
            start_time = format_time(word['start'])
            end_time = format_time(word['end'])
            word_text = word['word']  

            cleaned_word_text = clean_word_for_comparison(word_text)
            if specialWords and list_index < len(words):
                original_text = words[list_index]
                cleaned_original_text = clean_word_for_comparison(original_text)

    
                threshold = 20 if len(word_text) < 4 else 30

                if cleaned_word_text != cleaned_original_text:
                    similarity = fuzz.ratio(cleaned_word_text, cleaned_original_text)
                    if similarity < threshold:  
                        
                        context_window = [clean_word_for_comparison(w) for w in words[max(0, list_index - 3):min(len(words)-1, list_index + 3)]]
                        best_match, relative_index = find_best_match(cleaned_word_text, context_window)
                       
                        list_index = max(0, list_index - 3) + relative_index
                        word_text = words[max(0, list_index - 3) + relative_index]  
                    else:
                        word_text = original_text 

                list_index += 1

            srt_file.write(f"{srt_counter}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{word_text}\n\n")

            srt_counter += 1
