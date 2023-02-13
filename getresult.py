import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import numpy as np
import pymorphy2

model = gensim.models.KeyedVectors.load_word2vec_format('model1.bin', binary=True)


class analys:

    def __init__(self, text1, text2, model):
        self.text1 = text1
        self.text2 = text2
        self.flag = True

    def clear_text(self, text: str):
        symbols_to_delete = ['.', ',', '\'', '!', '(', ')', '?', '"']

        for s in symbols_to_delete:
            text = text.replace(s, '')

        symbols_to_replace = {'ё': 'е'}
        for k, v in symbols_to_replace.items():
            text = text.replace(k, v)

        return text

    def replace_antonyms(self, text):
        keywords = ['НЕ', 'не', 'Не']
        text = text.split()
        for i in range(len(text) - 1):
            if text[i] in set(keywords):
                try:
                    text_to_replace = text[i + 1]
                    for sense in wn.get_senses(text_to_replace):
                        res = sense.synset.antonyms[0].title.split()[0]
                        res = self.clear_text(self, res)
                        res = res.lower()
                        text[i + 1] = res
                        text[i] = ''


                except Exception as e:
                    pass

        text = [a for a in text if a]
        return ' '.join(text)


    def determine_vector(self, text: str):
        clean_text = self.clear_text(text)
        text_to_antonyms = self.replace_antonyms(clean_text)
        clean_text = self.clear_text(text_to_antonyms)
        text_list = clean_text.split(' ')  # список со словами
        text_len = len(text_list)

        morph = pymorphy2.MorphAnalyzer(lang='ru')

        bad = []
        good = []

        good_count = 0
        first_start = True

        for word in text_list:
            word_analyzed = morph.parse(word)[0]
            POS = word_analyzed.tag.POS
            normal_form = word_analyzed.normal_form.replace('ё', 'е')

            pymorph_POS_to_w2v = {'ADVB': 'ADV', 'ADJF': 'ADJ', 'NPRO': 'PROPN',
                                  'PRCL': 'NOUN'}
            for k, v in pymorph_POS_to_w2v.items():
                try:
                    POS = POS.replace(k, v)
                except Exception:
                    pass

            try:
                vec = model.get_vector(normal_form + '_' + str(POS))
                good.append(normal_form + '_' + str(POS))
            except:
                bad.append(normal_form + '_' + str(POS))
                continue

            if first_start:
                text_vec = vec
                first_start = False
                good_count += 1
                continue

            text_vec = np.add(text_vec, vec)
            good_count += 1
        try:

            res = text_vec / good_count
            return res, self.flag
        except Exception:
            self.flag = False
        return -1, self.flag


def cosine_similarity(vec1, vec2):
    res = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return res


def result(text1, text2):
    a = analys(text1, text2, model)
    first_text_vec, flag1 = a.determine_vector(text1)
    second_text_vec, flag2 = a.determine_vector(text2)
    if flag1 and flag2:

        return float(round(cosine_similarity(first_text_vec, second_text_vec) * 100, 2))
    else:
        return -1


