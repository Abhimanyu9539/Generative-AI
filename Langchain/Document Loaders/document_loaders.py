# -*- coding: utf-8 -*-
"""Document Loaders.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V2_W57jTVqSgK7HEnlUA9VLOGiRJNgQr
"""

!pip install langchain==0.2.0
!pip install langchain-openai==0.1.7
!pip install langchain-community==0.2.0

# takes 2 - 5 mins to install on Colab
!pip install "unstructured[all-docs]==0.14.0"

# install OCR dependencies for unstructured
!sudo apt-get install tesseract-ocr
!sudo apt-get install poppler-utils

!pip install jq==1.7.0
!pip install pypdf==4.2.0
!pip install pymupdf==1.24.4

"""# Text Loader"""

!curl -o README.md https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md

from langchain_community.document_loaders import TextLoader

loader = TextLoader('README.md')
doc = loader.load()

doc[0].page_content[:1000]

type(doc[0])

print(doc[0].page_content[:10000])

"""# Markdown Loader"""

from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader("./README.md", mode='single')
docs = loader.load()

print(docs[0].page_content[:100])

type(docs[0])

from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader("./README.md", mode="elements")
docs = loader.load()

len(docs)

docs[:10]

from collections import Counter
Counter([doc.metadata['category'] for doc in docs])

"""Comparing Unstructured.io loaders vs LangChain wrapper API"""

from unstructured.partition.md import partition_md

docs = partition_md(filename="./README.md")

len(docs)

docs[:10]

docs[0].to_dict()

docs[1].to_dict()

from langchain_core.documents import Document

lc_docs = [Document(page_content=doc.text,
                    metadata=doc.metadata.to_dict())
              for doc in docs]
lc_docs[:10]

"""# CSV Loader"""

import pandas as pd

# Create a DataFrame with some dummy real estate data
data = {
    'Property_ID': [101, 102, 103, 104, 105],
    'Address': ['123 Elm St', '456 Oak St', '789 Pine St', '321 Maple St', '654 Cedar St'],
    'City': ['Springfield', 'Rivertown', 'Laketown', 'Hillside', 'Sunnyvale'],
    'State': ['CA', 'TX', 'FL', 'NY', 'CO'],
    'Zip_Code': [98765, 87654, 76543, 65432, 54321],
    'Bedrooms': [3, 2, 4, 3, 5],
    'Bathrooms': [2, 1, 3, 2, 4],
    'Listing_Price': [500000, 350000, 600000, 475000, 750000]
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('data.csv', index=False)

df

from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(file_path="./data.csv")
docs = loader.load()

docs

docs[0]

print(docs[0].page_content)

loader = CSVLoader(file_path="./data.csv",
                   csv_args={
                      "delimiter": ",",
                      "quotechar": '"',
                      "fieldnames": ["Property ID", "Address", "City", "State",
                                     "Zip Code", "Bedrooms", "Bathrooms", "Price"],
                   },
                  )
docs = loader.load()

docs

from langchain_community.document_loaders import UnstructuredCSVLoader

loader = UnstructuredCSVLoader("./data.csv")
docs = loader.load()

docs

len(docs)

docs[0]

"""# JSON Loader"""

import json

# Sample data dictionary similar to the one you provided but with modified contents
data = {
    'image': {'creation_timestamp': 1675549016, 'uri': 'image_of_the_meeting.jpg'},
    'is_still_participant': True,
    'joinable_mode': {'link': '', 'mode': 1},
    'magic_words': [],
    'messages': [
        {'content': 'See you soon!',
         'sender_name': 'User B',
         'timestamp_ms': 1675597571851},
        {'content': 'Thanks for the update! See you then.',
         'sender_name': 'User A',
         'timestamp_ms': 1675597435669},
        {'content': 'Actually, the green one is sold out.',
         'sender_name': 'User B',
         'timestamp_ms': 1675596277579},
        {'content': 'I was hoping to purchase the green one!',
         'sender_name': 'User A',
         'timestamp_ms': 1675595140251},
        {'content': 'I’m really interested in the green one, not the red!',
         'sender_name': 'User A',
         'timestamp_ms': 1675595109305},
        {'content': 'Here’s the $150 for it.',
         'sender_name': 'User B',
         'timestamp_ms': 1675595068468},
        {'photos': [{'creation_timestamp': 1675595059,
                     'uri': 'image_of_the_item.jpg'}],
         'sender_name': 'User B',
         'timestamp_ms': 1675595060730},
        {'content': 'It typically sells for at least $200 online',
         'sender_name': 'User B',
         'timestamp_ms': 1675595045152},
        {'content': 'How much are you asking?',
         'sender_name': 'User A',
         'timestamp_ms': 1675594799696},
        {'content': 'Good morning! $50 is far too low.',
         'sender_name': 'User B',
         'timestamp_ms': 1675577876645},
        {'content': 'Hello! I’m interested in the item you posted. I can offer $50. Let me know if that works for you. Thanks!',
         'sender_name': 'User A',
         'timestamp_ms': 1675549022673}
    ],
    'participants': [{'name': 'User A'}, {'name': 'User B'}],
    'thread_path': 'inbox/User A and User B chat',
    'title': 'User A and User B chat'
}

# Save the modified data to a JSON file
with open('chat_data.json', 'w') as file:
    json.dump(data, file, indent=4)

from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path='./chat_data.json',
    jq_schema='.',
    text_content=False)

data = loader.load()

data

len(data)

loader = JSONLoader(
    file_path='./chat_data.json',
    jq_schema='.messages[]',
    text_content=False)

data = loader.load()
data

loader = JSONLoader(
    file_path='./chat_data.json',
    jq_schema='.messages[].content',
    text_content=False)

data = loader.load()
data

"""# PDF Loader"""

!wget -O 'layoutparser_paper.pdf' 'http://arxiv.org/pdf/2103.15348.pdf'

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./layoutparser_paper.pdf")
pages = loader.load()

pages

len(pages)

pages[0]

print(pages[4].page_content)

from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader("./layoutparser_paper.pdf")
pages = loader.load()

len(pages)

pages[0].metadata

print(pages[0].page_content)

print(pages[4].page_content)

from langchain_community.document_loaders import UnstructuredPDFLoader

loader = UnstructuredPDFLoader('./layoutparser_paper.pdf')
data = loader.load()

len(data)

print(data[0].page_content[:1000])

# takes 3-4 mins on Colab
loader = UnstructuredPDFLoader('./layoutparser_paper.pdf',
                               strategy='hi_res',
                               extract_images_in_pdf=False,
                               infer_table_structure=True,
                               chunking_strategy="by_title",
                               max_characters=4000, # max size of chunks
                               new_after_n_chars=3800, # preferred size of chunks
                               combine_text_under_n_chars=2000, # smaller chunks < 2000 chars will be combined into a larger chunk
                               mode='elements')
data = loader.load()

len(data)

[doc.metadata['category'] for doc in data]

data[0]

data[5]

data[5].page_content

from IPython.display import HTML

HTML(data[5].metadata['text_as_html'])