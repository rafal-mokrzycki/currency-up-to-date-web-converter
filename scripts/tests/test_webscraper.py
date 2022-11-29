""" to run: python -m pytest -vv scripts\tests\test_webscraper.py -s
add --pdb to debug in command line
use VScode test tools reccomended (the beaker) """
import pytest
import repackage

repackage.up()
from scripts.webscraper import Converter

conv = Converter()


@pytest.fixture(name="dictionary")
def fixture_dictionary():
    """Creates and returns a currencies dictionary."""
    yield {"GBP": 1.5, "USD": 2.5, "PLN": 4}


@pytest.fixture(name="webscraped_dictionary")
def fixture_webscraped_dictionary():
    """Creates and returns a currencies dictionary from web."""
    yield conv.get_dict_with_currencies(conv.url)


def test_get_dict_with_currencies_pln(webscraped_dictionary):
    assert ("PLN" in webscraped_dictionary) is True


def test_get_dict_with_currencies_eur(webscraped_dictionary):
    assert ("EUR" in webscraped_dictionary) is False


def test_get_dict_with_currencies_xxx(webscraped_dictionary):
    assert ("XXX" in webscraped_dictionary) is False


def test_convert_currencies_no_eur(dictionary):
    assert conv.convert_currencies(dictionary, "PLN", "USD", 100) == 1000.0


def test_convert_currencies_eur_left(dictionary):
    assert conv.convert_currencies(dictionary, "EUR", "USD", 100) == 250.0


def test_convert_currencies_eur_right(dictionary):
    assert conv.convert_currencies(dictionary, "PLN", "EUR", 100) == 25.0


def test_convert_currencies_eur_both(dictionary):
    assert conv.convert_currencies(dictionary, "EUR", "EUR", 100) == 100.0


def test_convert_currencies_error(dictionary):
    with pytest.raises(Exception):
        conv.convert_currencies(dictionary, "XXX", "YYY", 100)


def test_format_number():
    assert conv.format_number(2.5, "PLN") == "2.50 PLN"
