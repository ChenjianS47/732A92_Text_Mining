import pandas as pd
import string
import contextualSpellCheck

data = pd.read_excel('data_38k_us.xlsx')
from sklearn.model_selection import train_test_split

data_train,data_test = train_test_split(data, test_size=0.33, random_state=42)

train = data_train.groupby('Score').apply(lambda x: x.sample(frac=0.1,random_state=2201))
test = data_test.groupby('Score').apply(lambda x: x.sample(frac=0.1,random_state=2201))
train = train.reset_index(drop=True)
test = test.reset_index(drop=True)

import spacy
import re

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

print('test')

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("contextual spellchecker", config={"max_edit_dist": 5})

train_filt = pd.DataFrame(columns=['Time', 'Score', 'Content'])
test_filt = pd.DataFrame(columns=['Time', 'Score', 'Content'])

def spell_check_and_language_detect(data,data_filter):
    for i in range(len(data)):
        print(i)
        data.iloc[i,2]=remove_emoji(str(data.iloc[i,2]))
        doc = nlp(data.iloc[i,2])
        data.iloc[i,2] = doc._.outcome_spellCheck
        data_filter = data_filter.append(data.iloc[i,:])
        pass
    return data_filter

train_filt = spell_check_and_language_detect(train,train_filt)
test_filt = spell_check_and_language_detect(test,test_filt)


train_filt.to_excel('train_data.xlsx', index=False)
test_filt.to_excel('test_data.xlsx', index=False)