from icrawler.builtin import BingImageCrawler

crawler = BingImageCrawler(downloader_threads=4, storage={"root_dir": "cats_3"})
crawler.crawl(keyword="猫 写真", max_num=2000)