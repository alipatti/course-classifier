from __future__ import annotations
from dataclasses import dataclass
import pathlib
from typing import Iterable

import json
from bs4 import BeautifulSoup
import requests
import nltk

CATALOG_URL = "https://apps.carleton.edu/campus/registrar/catalog/current/departments/"


@dataclass
class Course:
    dept: str
    number: str
    description: str

    @classmethod
    def from_course_div(cls, div: BeautifulSoup) -> Course:
        dept, number = div.select_one(".courseNumber").text.split()  # type: ignore

        description = div.select_one(".courseDescription").text  # type: ignore

        # remove prereqs
        description, *_ = description.rsplit("Prerequisite:", maxsplit=1)

        description = preprocess(description)

        return Course(dept.lower(), number, description)

    @classmethod
    def from_json(cls, string: str) -> Course:
        return Course(**json.loads(string))

    def to_json(self) -> str:
        return json.dumps(self.__dict__)


def create_catalog(directory, catalog="courses.jsonl"):
    directory = pathlib.Path(directory)

    with open(catalog, "wt", encoding="utf8") as f:
        for dept in _get_all_depts():
            print(f"Scraping {dept[:-1].upper()}...")

            for course in _scrape_dept(CATALOG_URL + dept):
                f.write(course.to_json() + "\n")


def _get_all_depts() -> tuple[str, ...]:
    with requests.get(CATALOG_URL) as req:
        soup = BeautifulSoup(req.text, features="html.parser")

    return tuple(a.attrs["href"] for a in soup.select(".childrenList a[href]"))


def _scrape_dept(url: str) -> Iterable[Course]:
    with requests.get(url) as req:
        soup = BeautifulSoup(req.text, features="html.parser")

    return (Course.from_course_div(div) for div in soup.select(".courseContainer"))


# --- PREPROCESSING with Tokenization---

nltk.download("stopwords")
nltk.download("punkt")
STOP_WORDS = set(nltk.corpus.stopwords.words("english"))


def preprocess(text: str):
    "Makes text lowercase and removes stopwords and punctuation."
    text = text.lower()
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word.isalpha() and word not in STOP_WORDS]

    return " ".join(words)


if __name__ == "__main__":
    create_catalog("courses/")
