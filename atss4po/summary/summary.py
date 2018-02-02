from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import pickle
import time
import os
from flask import current_app
from atss4po.database import db
from ..user.models import Article
class AutoSummary(object):
    def __init__(self, language):
        self.language = language
        self.stemmer = Stemmer(self.language)
        self.summarizer = Summarizer(self.stemmer)
        self.summarizer.stop_words = get_stop_words(self.language)


    def save_article(self, parser):
        date = time.strftime('%Y%m%d',time.localtime(time.time()))
        dir_path = os.path.join(current_app.config['DATA_PATH'], date)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        filename = time.strftime('%H-%M-%S',time.localtime(time.time())) + '.pkl'
        filepath = os.path.join(dir_path, filename)
        article = Article(filepath)
        with open(filepath, mode='wb') as f:
            pickle.dump(parser.document, f)
            db.session.add(article)
            db.session.commit()

    def read_article(self, filename):
        article = ''
        with open(filename, mode='rb') as f:
            document = pickle.load(f)
            for paragraph in document.paragraphs:
                if(len(paragraph.headings)):
                    for heading in paragraph.headings:
                        article = article + str(heading)
                if(len(paragraph.sentences)):
                    for sentence in paragraph.sentences:
                        article = article + str(sentence)
                article = article + '\n'
        return article

    def summary_from_url(self, url, count):
        list = []
        try:
            parser = HtmlParser.from_url(url, Tokenizer(self.language))
            self.save_article(parser)
            for sentence in self.summarizer(parser.document, count):
                list.append(str(sentence))
        except:
            list = []
        return list

    def summary_from_text(self, text, count):
        list = []
        try:
            parser = PlaintextParser.from_string(text, Tokenizer(self.language))
            self.save_article(parser)
            for sentence in self.summarizer(parser.document, count):
                list.append(str(sentence))
        except:
            list = []
        return list


autosum = AutoSummary('chinese')

if __name__ == '__main__':
    filename = '/Users/zhangke/project/atss4po/atss4po/data/20180202/18-00-42.pkl'
    article = autosum.read_article(filename)
    print(article)

