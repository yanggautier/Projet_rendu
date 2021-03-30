from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
import os

tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine")

path = '/model/tf_model.h5'
if os.path.exists(path):  

    model = TFAutoModelForSequenceClassification.from_pretrained('./model/', local_files_only=True)

else: 
    
    model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")

    tokenizer.save_pretrained('./tokenizer/')
    model.save_pretrained('./model/')



nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)