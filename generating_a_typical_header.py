from transformers import pipeline, GPT2Tokenizer

ved_pipeline = pipeline('text-generation', model='./title_ved_gen_small', tokenizer='sberbank-ai/rugpt3small_based_on_gpt2')

initial_seed = "В Рязани"
initial_seed_split = initial_seed.split()
    
t = GPT2Tokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")

text = ' '.join(initial_seed_split)
length = len(t(text)['input_ids'])

out = ved_pipeline(text, max_length=length + 40, min_length=length + 5, early_stopping=True, do_sample=True, temperature=1.2)[0]['generated_text']

# Модель создаёт 2-3 заголовка, разделяя их двойным пробелом. Берём только 2-ой, чтобы заголовок не зависил от initial_seed и всегда получался разным
out = out.split('  ')
print(text[1])
