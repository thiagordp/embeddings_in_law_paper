"""

"""
import nltk
import spacy

from pre_processing.extract_texts_pdf import digital_pdf_file

from nltk.tokenize import sent_tokenize

# nltk.download('punkt')


sentence_denied = [
    "o documento pode ser acessado pelo endere",
    "documento assinado digitalmente conforme mp"
]


def main():
    nlp = spacy.load('pt_core_news_sm')

    text = digital_pdf_file("document.pdf")

    tokens = nlp(text)

    nltk.data.load('tokenizers/punkt/portuguese.pickle')
    tokens = sent_tokenize(text)
    for token in tokens:
        found = False
        for denied in sentence_denied:
            if token.find(denied) != -1:
                found = True
                break

        if not found:
            print(token)


if __name__ == "__main__":
    main()
