# Introduction
This is a service that exposes spacy

# Info
https://www.codementor.io/sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq

# Setup
```
conda create -n SpacyService pip
pip install flask flask-jsonpify flask-sqlalchemy flask-restful spacy==2.1.0
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
```

# Using
http://localhost:5002/analyse/the%20cat%20sat%20on%20the%20mat