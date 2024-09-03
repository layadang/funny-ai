import pandas as pd
import random

random.seed(1103)

df = pd.read_csv('data/masked_tweets_with_bert.csv')
rand_index = random.randint(0, len(df))

prompt_text = f"What goes in the empty space?\n\n {df['masked_tweet'][rand_index]}\n\nYour answer: "

user_answer = input(prompt_text).lower().strip()

print(f"Answer is {df['masked_word'][rand_index]}")
print(f"AI answered {df['bert_response'][rand_index]}")
