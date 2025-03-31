# Required Reading

Required Reading generates made-up textbook titles using excerpts from a corpus of texts.

From 2016 to 2024 it ran as a bot on Twitter(@req_reading), and later on Mastodon(@botsin.space@requiredreading), posting these titles.

## Usage

Before Required Reading can generate titles, it must run its excerpting process on a corpus. A corpus can be prepared by placing any number of plaintext files in a directory at data/corpus, and then running in excerpting mode. This can be achieved by running reading.py with the flag --excerpt. This will create a new directory at data/excerpts, which it can then use to generate titles.

To generate titles with Required Reading in the command line, run reading.py with the flag --test. This will generate one title and print it to the console.

To generate more titles at once, use the flag '-c' followed by an integer value.

## Requirements

Due to dependencies, at present Required Reading can only be run with python 2.

The project contains two requirements files. The packages in "requirements_excerpting.txt" are needed to process corpus data. Those in "requirements.txt" are required for it to function as a bot on social media.

## Posting on social media

Required Reading uses Bot Buddy for posting to its social media accounts. Bot Buddy does not currently exist in any package manager, but you can find the [source on Github](https://github.com/inthescales/bot-buddy).
