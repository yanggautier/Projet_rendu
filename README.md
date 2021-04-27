# Projet_rendu
***
## Installation
For install packages

```
pip install -r requirements.txt
```

For launch test.py

```
python tests/test.py
```

For launch FastAPI for prediction

```
python main.py
```

After application starts, you can send a json POST message with:

* Postman on [Postman](https://www.postman.com/)
or 
* Insomnia on [Insomnia](https://insomnia.rest/products/insomnia)

on your endpoint [Link](https://127.0.0.1:8000/sentiment)

It will return a prediction message "Positif" or "Négatif"
