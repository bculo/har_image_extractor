import json
import os.path

from browsermobproxy import Server
from selenium import webdriver

PAGE_URL = "http://www.google.co.uk"
HAR_FOLDER = "har_files"
HAR_NAME = "file"
BROWSERMOB_PATH = "./proxy/browsermob-proxy-2.1.4/bin/browsermob-proxy"
options = {'port': 8090}

server = Server(BROWSERMOB_PATH, options={'port': 8090})
server.start()

proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))

driver = webdriver.Chrome(options=chrome_options)

proxy.new_har(HAR_NAME)
driver.get(PAGE_URL)

destination = os.path.join(HAR_FOLDER, f"{HAR_NAME}.har")
with open(destination, "w") as writer:
    writer.write(json.dumps(proxy.har))

server.stop()
driver.quit()
