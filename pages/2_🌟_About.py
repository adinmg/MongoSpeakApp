import streamlit as st
from ui import logo

st.set_page_config(
    page_title="MongoSpeakApp",
    page_icon="🎓",
)

st.markdown(
"""
#### About Me 🚀
I'm a physicist with a passion for machine learning, deep learning, data, and creating interactive web applications with Streamlit.

#### What You'll Find Here 📚
- CRUD Application with MongoDB 📊
- Text-to-audio conversion 🔊
- Text generated by a Large Language Model 📝

#### My Projects 🌟
Here are some of the projects I've worked on:
- [Paper Replicating in Vision Transformers focused on sound classification in PyTorch (GitHub)](https://github.com/adinmg/Vit-classifier-pytorch) 📂
- [Streamlit app capable of classifying up to 120 different dog breeds in TensorFlow (Huggingface)](https://huggingface.co/spaces/josueadin/dog_breed_classifier) | [GitHub](https://github.com/jamg/dog_breed_classifier) 🐶
- [PyTorch Utils: a repository with a series of helper functions (GitHub)](https://github.com/adinmg/PyTorch_utils) 🧰
- [Generative_AI_Flask: a repository containing connections to Generative AI with ChatGPT and Bria (Image Generation) with Flask (GitHub)](https://github.com/adinmg/generative_ai_flask) 🤖

#### Tools and Packages 🛠️
I used various tools and packages to build this app, including:

- **MongoDB**: For storing and retrieving data 📂
- **PyMongo**: Python library for MongoDB 🐍
- **Streamlit**: An interactive web app framework for Python 🌐
- **gTTS**: Library for converting text to speech 🔊
- **Tempfile**: Creating temporary files 📁
- **LangChain**: Custom-built language processing framework that added powerful linguistic capabilities to my app 📖

#### Contact Me 📧
Feel free to reach out to me at: [josue.adin@gmail.com](mailto:josue.adin@gmail.com)

""")

logo()