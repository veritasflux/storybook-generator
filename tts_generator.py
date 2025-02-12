# 🇪🇸 'e' => Spanish es
# 🇫🇷 'f' => French fr-fr
# 🇮🇳 'h' => Hindi hi
# 🇮🇹 'i' => Italian it
# 🇧🇷 'p' => Brazilian Portuguese pt-br

# 3️⃣ Initalize a pipeline
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import numpy as np
# 🇺🇸 'a' => American English, 🇬🇧 'b' => British English
# 🇯🇵 'j' => Japanese: pip install misaki[ja]
# 🇨🇳 'z' => Mandarin Chinese: pip install misaki[zh]
def generate_story_speech(text):
    pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice
    
    # This text is for demonstration purposes only, unseen during training
    text = '''
    As they journeyed deeper into the savannah, Paul and Leo encountered numerous obstacles, from treacherous ravines to steep hills. But with Leo's bravery and Paul's quick thinking, they overcame each challenge, drawing closer to finding the missing cubs. Paul marveled at Leo's incredible strength and agility, and Leo praised Paul's clever ideas and kindness. Their bond grew stronger with every step, and they worked together seamlessly, like a well-oiled machine. "We make a great team, Leo!" Paul exclaimed, and Leo responded with a mighty roar of approval.'''
    # text = '「もしおれがただ偶然、そしてこうしようというつもりでなくここに立っているのなら、ちょっとばかり絶望するところだな」と、そんなことが彼の頭に思い浮かんだ。'
    # text = '中國人民不信邪也不怕邪，不惹事也不怕事，任何外國不要指望我們會拿自己的核心利益做交易，不要指望我們會吞下損害我國主權、安全、發展利益的苦果！'
    # text = 'Los partidos políticos tradicionales compiten con los populismos y los movimientos asamblearios.'
    # text = 'Le dromadaire resplendissant déambulait tranquillement dans les méandres en mastiquant de petites feuilles vernissées.'
    # text = 'ट्रांसपोर्टरों की हड़ताल लगातार पांचवें दिन जारी, दिसंबर से इलेक्ट्रॉनिक टोल कलेक्शनल सिस्टम'
    # text = "Allora cominciava l'insonnia, o un dormiveglia peggiore dell'insonnia, che talvolta assumeva i caratteri dell'incubo."
    # text = 'Elabora relatórios de acompanhamento cronológico para as diferentes unidades do Departamento que propõem contratos.'
    text = " ".join(text.split())  # Removes newlines and trims spaces
    # 4️⃣ Generate, display, and save audio files in a loop.
    generator = pipeline(
        text, voice='af_heart', # <= change voice here
        speed=1, split_pattern=r'###'
    )
    audio_chunks = []
    
    for i, (gs, ps, audio) in enumerate(generator):
        print(i)  # Output index
        print(gs) # Graphemes (text)
        print(ps) # Phonemes
        audio_chunks.append(audio)  # Store audio chunk
    
    # Concatenate all audio chunks into one single array
    if audio_chunks:
        full_audio = np.concatenate(audio_chunks)
    

    
        # Save the final audio file
        sf.write('final_output.wav', full_audio, 24000)
    return display(Audio(data=full_audio, rate=24000, autoplay=True))
