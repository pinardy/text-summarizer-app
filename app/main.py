import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest

def summarize_text(raw_text):
    nlp = spacy.load('en_core_web_sm')
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)

    # Build word frequency
    # word.text is tokenization in spacy
    word_frequencies = {}  
    for word in docx:  
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    # Sentence tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Calculate sentence score & ranking
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Find N Largest
    summary_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summary_sentences ]
    summary = ' '.join(final_sentences)

    print(f"Original Document (Length: {len(raw_text)})\n")
    print(raw_text)
    print(f"\n\nSummarized Document (Length: {len(summary)})\n")
    print(summary)

    return summary
