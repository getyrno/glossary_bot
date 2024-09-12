from transformers import AutoTokenizer, AutoModelForCausalLM
import json

# Загрузка токенизатора и модели Bloom
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")
model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-560m")

# Функция для генерации описания термина
def generate_description(term):
    prompt = f"Provide a concise explanation of the term '{term}' in the context of machine learning."
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=512, num_beams=5, early_stopping=True)

    
    # Декодирование текста
    description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Удаление повторяющегося промпта из результата
    description = description[len(prompt):].strip()
    description = ' '.join(description.split())  # Удаление лишних пробелов
    return description

# Функция для обновления глоссария
def update_glossary(term, description, glossary_file='glossary.json'):
    try:
        with open(glossary_file, 'r', encoding='utf-8') as f:
            glossary = json.load(f)
    except FileNotFoundError:
        glossary = {}

    glossary[term] = description

    with open(glossary_file, 'w', encoding='utf-8') as f:
        json.dump(glossary, f, ensure_ascii=False, indent=4)

# Функция для генерации и сохранения описания термина в указанный файл
def save_term_to_glossary(term, filename):
    description = generate_description(term)
    update_glossary(term, description, glossary_file=filename)
    print(f"Термин '{term}' был сохранён в файл '{filename}'.")
