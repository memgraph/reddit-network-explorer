import emoji
import en_core_web_sm
import mgp
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


@mgp.read_proc
def procedure(context: mgp.ProcCtx,
              messages: str,
              ) -> mgp.Record(sentiment=int):
    try:
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')

        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')

        strings = emoji.get_emoji_regexp().sub(u'', messages)

        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
        tokenized_string = tokenizer.tokenize(strings)

        lower_string_tokenized = [word.lower() for word in tokenized_string]

        nlp = en_core_web_sm.load()

        all_stopwords = nlp.Defaults.stop_words

        text = lower_string_tokenized
        tokens_without_sw = [word for word in text if not word in all_stopwords]

        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = ([lemmatizer.lemmatize(w) for w in tokens_without_sw])

        cleaned_output = lemmatized_tokens

        sia = SIA()
        results = []

        for sentences in cleaned_output:
            pol_score = sia.polarity_scores(sentences)
            pol_score['words'] = sentences
            results.append(pol_score)

        pd.set_option('display.max_columns', None, 'max_colwidth', None)
        df = pd.DataFrame.from_records(results)

        df['label'] = 0
        df.loc[df['compound'] > 0.10, 'label'] = 1
        df.loc[df['compound'] < -0.10, 'label'] = -1
        df = df.loc[df['label'] != 0]

        counts = df['label'].value_counts()
        counts_index = counts.index

        sentiment = 0
        if counts.tolist()[0] > counts.tolist()[1]:
            sentiment = int(counts_index.tolist()[0])
        elif counts.tolist()[0] < counts.tolist()[1]:
            sentiment = int(counts_index.tolist()[1])

        return mgp.Record(sentiment=sentiment)
    except Exception as e:
        print(e)
        return
