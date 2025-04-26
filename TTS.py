import asyncio
import edge_tts
import re

with open('inputText.txt', 'r') as file:
    lines = file.readlines()
content = ''.join(lines)
TEXT = content

def expand_contractions(text):
    contractions_dict = {
        "lowkey": "low key",
        "outta": "out of",
        "gotta": "got to",
        "gonna": "going to",
        "wanna": "want to",
        "lemme": "let me",
        "kinda": "kind of",
        "sorta": "sort of",
        "ain't": "is not",
        "can't": "cannot",
        "won't": "will not",
        "n't": " not",
        "'re": " are",
        "'d": " would",
        "'ll": " will",
        "'ve": " have",
        "'m": " am",
        "y'all": "you all",
        "o'clock": "of the clock",
        "ma'am": "madam",
        "c'mon": "come on",
        "how'd": "how did",
        "how'll": "how will",
        "how's": "how is",
        "it's": "it is",
        "let's": "let us",
        "what're": "what are",
        "what'll": "what will",
        "what's": "what is",
        "where'd": "where did",
        "where'll": "where will",
        "where's": "where is",
        "who'd": "who did",
        "who'll": "who will",
        "who's": "who is",
        "you'd": "you would",
        "you'll": "you will",
        "you've": "you have",
        "tryna": "trying to",
        "finna": "fixing to",
        "lotsa": "lots of"
    }

    contractions_pattern = re.compile('({})'.format('|'.join(map(re.escape, contractions_dict.keys()))), 
                                       flags=re.IGNORECASE)
    
    def expand_match(contraction):
        match = contraction.group(0)
        return contractions_dict.get(match.lower(), match)
    
    expanded_text = contractions_pattern.sub(expand_match, text)
    return expanded_text

def combine_words_with_dash(text):
    """Remove dashes and combine adjacent words."""
    return text.replace("-", "")

TEXT = expand_contractions(TEXT)
TEXT = combine_words_with_dash(TEXT) 
TEXT = re.sub(r'["]', '', TEXT) 

with open("inputText.txt", 'w') as file:
    file.write(TEXT)

with open('model.txt', 'r') as file:
    lines = file.readlines()
voice = ''.join(lines)

voices = ["en-US-GuyNeural", "en-US-JennyNeural", "en-US-EricNeural", 
          "en-NZ-MollyNeural", "en-US-ChristopherNeural", "en-US-AriaNeural"]
names = ["Matthew", "Jenny", "Eric", "Molly", "Christopher", "Aria"]
map = {}

for i in range(0, len(voices)):
    map[names[i]] = voices[i]

VOICE = map[voice]

OUTPUT_FILE = "story.mp3"

async def amain() -> None:
    """Main function"""
    RATE = "+10%"
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE)
    await communicate.save(OUTPUT_FILE)

if __name__ == "__main__":
    asyncio.run(amain())
