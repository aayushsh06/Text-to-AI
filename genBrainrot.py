from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GROQ_KEY')
client = Groq(api_key=api_key)

with open('inputText.txt', 'r') as file:
    lines = file.readlines()
story = ''.join(lines)

brainrot_words_with_definitions = {
    "Gyatt": "An exclamation of admiration, often for someone's appearance.",
    "Rizz": "The ability to attract or charm someone romantically.",
    "Only in Ohio": "Refers to something bizarre or absurd, implying it could only happen in Ohio.",
    "Duke Dennis": "Refers to a popular content creator known for gaming and humorous content.",
    "Baby Gronk": "A young football player or someone seen as a prodigy.",
    "Sussy imposter": "A suspicious or untrustworthy person, derived from 'Among Us.'",
    "Sigma": "A lone wolf or independent person, often with a strong or confident personality.",
    "Alpha": "The leader of a group or someone seen as dominant and assertive.",
    "Huzz": "Young women",
    "Skibidi": "A quirky or humorous dance or movement.",
    "Freddy Fazbear": "The animatronic bear from 'Five Nights at Freddy's,' used to imply creepiness or nostalgia.",
    "Winter Arc": "A difficult or challenging phase in someone's life.",
    "Kai Cenat": "A famous Twitch streamer and internet personality.",
    "Fanum tax": "A playful term for an unexpected expense or cost.",
    "Edging": "A term from gaming or sports, referring to narrowly avoiding failure.",
    "Hitting the griddy": "A celebratory dance move.",
    "Goofy ahh": "Something comically absurd or silly.",
    "Gooning": "Engaging in rowdy or playful behavior.",
    "Aiden Ross": "A Twitch streamer known for his collaborations and humor.",
    "Light skin stare": "A humorous reference to a specific flirtatious or intense facial expression.",
    "Drippy Cheese": "Refers to something stylish or 'drippy,' often in fashion.",
    "Knee Surgery": "A term now used for an exciting upcomin event",
    "Mogging": "Dominating or outperforming someone.",
    "Quandale Dingle": "A surreal meme character.",
    "Glizzy": "Slang for a hotdog, often used humorously.",
    "Ratioed": "When a reply gets more engagement than the original post, implying the original was unpopular.",
    "Mewing": "A technique for improving jawline appearance.",
    "Fortnite battle pass": "Refers to a purchasable in-game item in 'Fortnite,' often used humorously.",
    "Based": "Staying true to oneself, often in the face of criticism.",
    "Cringe": "Something awkward, embarrassing, or second-hand embarrassing.",
    "Ice Spice": "Refers to a popular music artist.",
    "NPC energy": "Behaving like a non-player character, lacking individuality or spontaneity.",
    "Just a chill guy": "Someone relaxed, easygoing, or low-key.",
    "Lunchly": "Acting carelessly or clumsily.",
    "Baby Oil": "Used to imply smoothness or sleekness, literally or metaphorically.",
}

brainrot_words = list(brainrot_words_with_definitions.keys())

# Building the completion request
completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": (
                f"Take the following story and rewrite it to include the provided slang words as naturally and contextually as possible. "
                f"The story should remain coherent, and the words must be inserted based on their slang meanings. Here are the exact words to include with their definitions:\n"
                + "\n".join([f"{word}: {definition}" for word, definition in brainrot_words_with_definitions.items()])
                + f"\nEnsure that each word appears as much as possible, and you cannot modify the words (no dashes, spaces, or alterations). "
                f"The tone should stay true to the original story and only use humor derived from the correct integration of the slang words. "
                f"Do not add extra slang, casual language, or jokes that are not in the provided list. Limit the output to 200 words."
                f"\n\nOriginal story:\n{story}\n\n"
                f"ONLY OUTPUT THE REWRITTEN STORY IN A SINGLE BLOCK OF TEXT WITHOUT EXTRA EXPLANATIONS OR CONTEXT. ***DO NOT SAY HERE IS YOUR REWRITTEN STORY at the start of your result JUST OUTPUT THE STORY***"
            )
        },
    ],
    temperature=1,
    max_tokens=800,
    top_p=1,
    stream=True,
    stop=None,
)

script = []
for chunk in completion:
    content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content else ""
    if content:
        script.append(content)

rewritten_story = ''.join(script)

with open("inputText.txt", "w") as file:
    file.write(rewritten_story)
