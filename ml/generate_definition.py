import torch
import datetime
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, MarianMTModel, MarianTokenizer

# Класс для форматирования текста
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

# Функция подсчета времени генерации
def calcTime(time):
    return bcolors.OKGREEN + str((datetime.datetime.now() - time).total_seconds()) + bcolors.ENDC

# Загрузка токенизатора и модели напрямую из Hugging Face Hub
model_name_t5 = "t5-large"  # Замените на нужный идентификатор модели T5
model_name_gpt2 = "gpt2"    # Замените на нужный идентификатор модели GPT-2
model_name_translation = "Helsinki-NLP/opus-mt-en-ru"
device = "cuda" if torch.cuda.is_available() else "cpu"

t = datetime.datetime.now()
print('Загрузка модели Marian...')
tokenizer_translation = MarianTokenizer.from_pretrained(model_name_translation)
print('Модель Marian загружен! Время:' + calcTime(t))

t = datetime.datetime.now()
print('Загрузка токенизатора Marian...')
model_translation = MarianMTModel.from_pretrained(model_name_translation)
print('Токенизатор Marian загружен! Время:' + calcTime(t))


t = datetime.datetime.now()
print('Загрузка токенизатора GPT-2...')
tokenizer_gpt2 = GPT2Tokenizer.from_pretrained(model_name_gpt2)
print('Токенизатор GPT-2 загружен! Время:' + calcTime(t))

t = datetime.datetime.now()
print('Загрузка модели GPT-2...')
model_gpt2 = GPT2LMHeadModel.from_pretrained(model_name_gpt2)
model_gpt2.to(device)
print('Модель GPT-2 загружена! Время:' + calcTime(t))

# Функция генерации определения термина с использованием модели GPT-2
def generate_definition_gpt2(term, p={
        # Настройки модели
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
    
    # Генерация
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
    
    # Декодирование
    if len(outputs) > 0:
        lastTokensUsed = len(outputs[0])
    print(calcTime(t) + ' - время просчета, токенов в ответе -', lastTokensUsed, '\n')
    translated_text = translate_text(tokenizer_gpt2.decode(outputs[0][1 + p["tokens_offset"]:], skip_special_tokens=True),model_translation, tokenizer_translation)
    return translated_text

def translate_text(text, model, tokenizer):
    start_time = datetime.datetime.now()
    input_ids = tokenizer.encode(text, return_tensors='pt').to(device)
    
    # Перевод
    outputs = model.generate(input_ids, max_length=100)
    
    # Декодирование
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(calcTime(start_time) + ' - время перевода\n')
    return translation