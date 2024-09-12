# ml/generate_definition.py
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained('t5-base')
model = T5ForConditionalGeneration.from_pretrained('t5-base')

def generate_definition(term):
    """
    Генерирует определение для заданного термина с использованием T5.
    """
    input_text = f"Define the term: {term}"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    
    output_ids = model.generate(input_ids, max_length=100, num_beams=5, early_stopping=True)
    definition = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return definition
