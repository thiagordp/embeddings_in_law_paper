# Impact of Text Specificity and Size on Word Embeddings Performance: an Empirical Evaluation in Brazilian Legal Domain

Source code for the paper published in BRACIS 2020.

## Project Structure

### Web Crawlers

In this subproject, we implemented crawlers to collect jurisprudence judgements from Brazilian courts platforms: 
  - STF
  - STJ
  - TJ-SC
  - Jusbrasil portal.
  
Regarding the first STF, STJ and TJ-SC we collected documents from all legal subjects available, however from Jusbrasil we collected only documents regarding *air transport services* and *consumer law* to fill own needs in this work.

### Embeddings Training

In this subproject, we implemented the embeddings training using [GloVe](https://nlp.stanford.edu/pubs/glove.pdf), [Word2Vec (CBOW and Skipgram)](https://arxiv.org/pdf/1301.3781.pdf) and [FastText (CBOW and Skipgram)](https://arxiv.org/pdf/1607.04606.pdf) algorithms.

As described in the paper, we had three corpora to train embeddings related to three contexts: *global*, *general* and *air transport* .
Global context embrances multigenre texts such as literature, news and blog posts. In the other hand, general texts are related to legal documents of all subjects. Finally, air transport context has jurisprudence documents about failures in air transport services.

For each corpora, we created smaller bases as described in the paper and then we used each of them to train a GloVe representation.
However, due to submition deadline, we could not use other algorithms to the paper.
Recently, we finished the training of all algorithms.

We make all trained embeddings in this [link](https://ufscbr-my.sharepoint.com/:f:/g/personal/thiago_rdp_ufsc_br/Et0dp2JGiAhBldl2w54vTtIBNTaU6EPcfFIHXps4B-uh8A?e=XGStTc).

The embeddings are organized in the link in three main folders, one for each algorithm.
Then, inside of these folders there are three folders regarding the contexts as described before.
Finally, each file is an embeddings, where the filename has a pattern to tell you how it was trained, for instance:

- **glove_1000_100.txt**: A GloVe embedding trained with a corpus of 1000 tokens with output vector of size 100.
- **fast_text_cbow_200000_100.txt**: A Fast Text CBOW embedding trained with a corpus of 200.000 tokens with output vector of size 100.


### Text Classification

In this subproject, we implemented Text Classification using Convolutional Neural Networks using an [available architecture](https://arxiv.org/abs/1408.5882).
We used a set of judgements related to failures in air transport services from JEC/UFSC.

For each embedding we created, we applied the CNN (train and test) 200 times. 
Then, we took the accuracy and Macro F1 Score for each repetition and averaged them to get the final metrics for each embedding.


## Notes

- We did not make our datasets for embeddings training and text classication available due to the personal data in the documents.

