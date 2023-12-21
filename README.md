Python app that extracts images from HAR file and generates PDF file from them

### HOW TO RUN IT?

- install java 'brew install openjdk@11'
- create symlink to installation 'brew link openjdk@11'
- download latest release of 'browsermob-proxy' (https://github.com/lightbody/browsermob-proxy/releases/tag/browsermob-proxy-2.1.4)
- unpack package inside proxy folder that should be located inside 'har_image_extractor'. 
- pipenv install
- place HAR file inside har_files folder
- pipenv run python3 main.py or pipenv run python3 create-har.py
