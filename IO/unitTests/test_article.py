import pytest

from IO.models.article import *
from jsonschema import validate
import requests, json


class TestArticle:
    article: Article

    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.article = Article()

    def test_add_paragraph_gives_article_with_paragraph_on_paragraph(self):
        paragraph = Paragraph()
        self.article.add_paragraph(paragraph)
        assert self.article.paragraphs.__len__() == 1

    def test_add_paragraph_gives_article_without_paragraph_on_string(self):
        self.article.add_paragraph("string")
        assert self.article.paragraphs.__len__() < 1

    def test_to_json_gives_valid_json_on_call(self):
        output = self.article.to_json()
        try:
            json.loads(output)
            assert True
        except ValueError:
            pytest.fail("Generated string is not valid JSON")

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
