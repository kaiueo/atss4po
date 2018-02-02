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
from atss4po.user.models import Article
from numpy.linalg.linalg import LinAlgError
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
        except(LinAlgError):
            list.append(text)
        except:
            list = []
        return list

    def summary_from_weibos(self, weibos, count):
        text = ''
        for weibo in weibos:
            text = text + weibo + '\n'
        return self.summary_from_text(text, count)

autosum = AutoSummary('chinese')

if __name__ == '__main__':
    weibos = ['【#超级蓝血月全食# 据说在世的地球人都没见过！】今晚，超级蓝月伴血月即将组团亮相。“蓝月亮”指一个公历月中的第二个满月，血月本常伴随月食出现，但#超级蓝血月全食#极为罕见，是152年一遇的奇观。#央视新闻微直播#在北京、长春、青岛、阿勒泰、兴隆五地开启↓来互动赢奖品！ O央视新闻的微博直播 ​​​​',
              '#超级蓝血月全食# 【看来好照片还是要上专业设备~】美图继续刷起来~~最后一张是本组图片的拍摄者程月星、林鹏，感谢他们~~~ ​​​​',
              '【今晚必备！用手机也能拍出超级蓝血月全食！拍照攻略收好[耶]】今晚，超级月亮+蓝月+月全食将上演。拍摄月亮，不一定要有专业单反相机，家中的普通相机和手机也可以！实用拍月亮攻略，助你称霸朋友圈！戳视频学习↓↓L人民日报的秒拍视频（生活提示） 必收，转！ ​​​​',
              '#超级蓝血月全食# 你们的月亮看到没？[doge] ​​​​',
              '九九归一，食全10美。#超级蓝血月全食# ​​​​',
              '#超级蓝血月全食#朋友圈里各位大师都在晒月亮，本大师手残不好意思晒作品，就盗图几张啦，看这位大师水平咋样 ​​​​',
              '#超级蓝血月全食#现在的月亮是你们看向我的脸 ​​​[doge] ​​​​',
              '#超级蓝血月全食#哈哈哈，凑热闹[兔子] 2渭南·蒲城县城关镇 ​​​',
              '#超级蓝血月全食#  啊啊啊啊看到月亮了！家人健康！考试通过！@Rex-赖沛丰 爱我爱到无法自拔！ 2驻马店 ​​​​',
              '我们“用望远镜看创新 ”，也用望远镜看月亮奇观。你们今晚拍什么有意思的照片了吗？#超级蓝血月全食# ​​​ ​​​​',
              '拍的不好，只是纪念一下今晚极为罕见的#超级蓝血月全食#152年一遇的奇观。（第一张无P，第二张用手机P了一下） ​​​​']
    weibos = [' #南极之恋0202# “无论环境是好是坏，无论是富贵是贫贱，我都会爱着你，直到死亡将我们分开......”请接收这份来自南极的“求婚”[心]青春里的男孩@HERO趙又廷  女孩@杨子姗 ，在多年后终以吴富春、荆如意的名义在地球的极南端再次相遇相爱[男孩儿][女孩儿]2月2日赵又廷南极求婚，待你而来！',
              ' #南极之恋0202# 不负好时光，《南极绝恋》正式更名#南极之恋# 发布“深情相拥”版海报定档2月2日，2018南极之旅为爱重启！总有一个人爱你如生命，爱让我们生死相依[心][心]@HERO趙又廷 @杨子姗 @关锦鹏 @吴有音 ​​​​',
              '#南极之恋0202# 踏行南极，为爱而生！当世界的颜色仅剩下冰冷的蓝白，是爱带给彼此温暖。相忘于江湖，不如相濡以沫，为爱剪去杂乱胡须，为爱戴上空气婚戒，总有一个人爱你如生命[心]@HERO趙又廷 @杨子姗 @关锦鹏 @吴有音 ​​​​',
              '#南极之恋# 我死了，她怎么办，我回来了。——《南极之恋》 ​​​​',
              '#南极之恋# 有人以为南极是出世的，我却以为南极是入世的，所有的红尘法则，在这里不是被缩小了，而是被放大了。']
    print(autosum.summary_from_weibos(weibos, 3))

