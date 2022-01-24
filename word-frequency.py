import requests
import luigi
from bs4 import BeautifulSoup

class GetTopBooks(luigi.Task):
    def output(self):
        return luigi.LocalTarget('data/book_list.txt')

    def run(self):
        resp = requests.get("http://www.gutenberg.org/browse/scores/top")
        soup = BeautifulSoup(resp.content, "html.parser")

        pageHeader = soup.find_all("h2", string="Top 100 EBooks yesterday")[0]
        listTop = pageHeader.find_next_sibling("ol")

        with self.output().open("w") as f:
            for result in listTop.select("li>a"):
                if "/ebooks/" in result["href"]:
                    f.write("http://www.gutenberg.org{link}.txt.utf-8\n"
                        .format(
                            link=result["href"]
                        )
                    )