import torch
import datetime
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, MarianMTModel, MarianTokenizer
from deep_translator import GoogleTranslator
translator = GoogleTranslator()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def calcTime(time):
    return bcolors.OKGREEN + str((datetime.datetime.now() - time).total_seconds()) + bcolors.ENDC

model_name_t5 = "t5-large"
model_name_gpt2 = "gpt2"
device = "cuda" if torch.cuda.is_available() else "cpu"

t = datetime.datetime.now()
print('Загрузка токенизатора GPT-2...')
tokenizer_gpt2 = GPT2Tokenizer.from_pretrained(model_name_gpt2)
print('Токенизатор GPT-2 загружен! Время:' + calcTime(t))

t = datetime.datetime.now()
print('Загрузка модели GPT-2...')
model_gpt2 = GPT2LMHeadModel.from_pretrained(model_name_gpt2)
model_gpt2.to(device)
print('Модель GPT-2 загружена! Время:' + calcTime(t))

def generate_definition_gpt2(term, p={
        "do_sample": True,
        "top_p": 0.9,
        "temperature": 0.15,
        "repetition_penalty": 2.0,
        "min_length": 5,
        "max_length": 200,
        "tokens_offset": 0
        }):
    t = datetime.datetime.now()
    inp = f'Generate a definition for: {term}'
    input_ids = tokenizer_gpt2.encode(inp, return_tensors='pt').to(device)
    
    outputs = model_gpt2.generate(
        input_ids,
        do_sample=p["do_sample"],
        top_p=p["top_p"],
        temperature=p["temperature"],
        repetition_penalty=p["repetition_penalty"],
        min_length=p["min_length"],
        max_length=p["max_length"],
        early_stopping=True
    )
    
    if len(outputs) > 0:
        lastTokensUsed = len(outputs[0])
    print(calcTime(t) + ' - время просчета, токенов в ответе -', lastTokensUsed, '\n')
    translated_text = translate_text(tokenizer_gpt2.decode(outputs[0][1 + p["tokens_offset"]:], skip_special_tokens=True))
    return translated_text

def translate_text(text):
    start_time = datetime.datetime.now()
    translation = translate(text, 'ru', 'en')
    print(calcTime(start_time) + ' - время перевода\n')
    return translation


def translate(text: str, target_language: str, source_language: str = 'en') -> str:
    try:
        translator = GoogleTranslator(source=source_language, target=target_language)
        return translator.translate(text)
    except Exception as e:
        return text
