import json
import argparse


class InvertedIndex:
    def __init__(self, word_to_docs_mapping=None):
        self._word_to_docs = word_to_docs_mapping

    def set_mapping(self, new_dict):
        for key, value in new_dict.items():
            new_dict[key] = set(value)
        self._word_to_docs = new_dict

    def query(self, words):
        common_ids = set(self._word_to_docs[words[0]])
        for word in words:
            try:
                common_ids.intersection_update(self._word_to_docs[word])
            except KeyError:
                common_ids = set()
        return common_ids

    def dump(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self._word_to_docs, f, default=lambda x: tuple(x))

    @classmethod
    def load(cls, filepath):
        obj = cls()
        with open(filepath) as f:
            obj.set_mapping(json.load(f))
        return obj


def load_document(filepath):
    with open(filepath, encoding="utf8") as f:
        articles = dict()

        for line in f:
            article_id, content = line.split('\t', 1)
            articles[int(article_id)] = content.strip()

    return articles


def build_inverted_index(articles):
    words = dict()

    for article_id, content in articles.items():
        words_set = set(content.split())
        for word in words_set:
            words.setdefault(word, set()).update({article_id})

    return InvertedIndex(words)


def build(args):
    articles = load_document(args.dataset)
    inverted_index = build_inverted_index(articles)
    inverted_index.dump(args.index)


def query(args):
    inverted_indices = InvertedIndex.load(args.index)
    with open(args.query_file) as f:
        for line in f:
            queries = line.split()
            articles_ids = [*inverted_indices.query(queries)]
            print(*sorted(articles_ids), sep=',')


def build_parser():
    parser = argparse.ArgumentParser(description='InvertedIndex parser')
    subparsers = parser.add_subparsers()

    parser_build = subparsers.add_parser('build')
    parser_build.add_argument('--dataset', metavar='dataset', type=str)
    parser_build.add_argument('--index', metavar='index', type=str)
    parser_build.set_defaults(func=build)

    parser_query = subparsers.add_parser('query')
    parser_query.add_argument('--index', metavar='index', type=str)
    parser_query.add_argument('--query_file', metavar='index')
    parser_query.set_defaults(func=query)

    args = parser.parse_args()
    args.func(args)


build_parser()
