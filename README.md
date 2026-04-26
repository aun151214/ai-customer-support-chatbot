# AI Customer Support Chatbot

A customer support chatbot prototype built with Python and Streamlit.

The app uses a small FAQ knowledge base to answer customer questions, retrieve the most relevant support entries, and avoid guessing when the FAQ does not contain enough information.

## Project Purpose

Many small businesses receive repeated customer questions about services, appointments, pricing, opening hours, cancellation policies, and contact details. This project demonstrates a practical FAQ-based chatbot that can be adapted into a simple customer support assistant for websites or internal business tools.

## Features

- Ask customer support questions in a chat interface
- Load a default business FAQ knowledge base
- Upload a custom FAQ CSV file
- Retrieve relevant FAQ entries using TF-IDF similarity
- Avoid unsupported answers when the match score is low
- Optional OpenAI API support for answer rewriting
- View retrieved FAQ entries for transparency
- Save customer lead requests locally in a CSV file
- Clean and simple Python project structure

## Demo Screenshots

### App Home

![App Home](assets/app_home.png)

### FAQ Answer Example

![FAQ Answer Demo](assets/faq_answer_demo.png)

### Unsupported Question Example

![Not Found Demo](assets/not_found_demo.png)

### Lead Request Form

![Lead Form Demo](assets/lead_form_demo.png)

## Tech Stack

- Python
- Streamlit
- Pandas
- scikit-learn
- OpenAI API optional
- Git and GitHub

## Folder Structure

```text
ai_customer_support_chatbot/
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   └── README.md
├── business_data/
│   └── faq.csv
├── src/
│   ├── faq_loader.py
│   ├── generator.py
│   ├── lead_capture.py
│   └── retriever.py
└── tests/
    └── test_retriever.py
```

## How It Works

1. The app loads a FAQ CSV file.
2. The user asks a customer support question.
3. The FAQ entries are converted into searchable text.
4. A TF-IDF retriever finds the most relevant FAQ entries.
5. If the best match score is high enough, the chatbot returns the relevant answer.
6. If the match score is too low, the chatbot says it cannot answer confidently.
7. If OpenAI API support is enabled, the retrieved answer can be rewritten in a more natural support style.
8. Users can also save a lead request using the contact form.

## FAQ CSV Format

The FAQ file must include at least these columns:

```text
question,answer
```

A category column is optional:

```text
category,question,answer
```

Example:

```csv
category,question,answer
Appointments,How can I book an appointment?,You can book by phone email or online form.
Payments,What payment methods do you accept?,We accept card cash and bank transfer.
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Optional OpenAI API Setup

The app works without an OpenAI API key by returning the best retrieved FAQ answer. To enable answer rewriting, set an OpenAI API key as an environment variable.

On Windows PowerShell:

```bash
$env:OPENAI_API_KEY="your_api_key_here"
```

Then run:

```bash
streamlit run app.py
```

Do not save API keys directly inside the code or upload them to GitHub.

## Example Questions

For the default demo FAQ, users can ask:

```text
What services do you provide?
How can I book an appointment?
What are your opening hours?
Do you provide emergency dental care?
What payment methods do you accept?
Who is the CEO of the clinic?
```

The final question is not answered because the FAQ does not contain CEO information.

## Business Use Case

This type of app can be adapted for:

- Clinic and healthcare FAQ support
- Local business website chatbots
- Customer service assistants
- Appointment and pricing FAQs
- Lead collection forms
- Internal support knowledge bases

## Limitations

- This is a portfolio prototype, not a production-ready support system.
- TF-IDF retrieval is simple and does not capture meaning as deeply as embedding-based retrieval.
- The chatbot can only answer based on the FAQ knowledge base.
- Lead data is saved locally and is not connected to a CRM.
- A production version would need authentication, privacy controls, deployment, logging, and better monitoring.

## Future Improvements

- Add embedding-based semantic search
- Add ChromaDB or FAISS vector storage
- Add website widget integration
- Add CRM or email notification support
- Add chat history export
- Add admin panel for editing FAQ entries
- Add deployment on Streamlit Cloud

## Author

Aun Ali  
Applied AI, Machine Learning, and Computer Vision Developer  
GitHub: https://github.com/aun151214
