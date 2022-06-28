# Kindle Dictionaries for Toki Pona

Using community data from lipu Linku by kala Asi, construct dictionaries for Toki Pona words 
compatible with kindle devices for quick word lookup. Great for new learners of the language.

## Releases

To quickly get dictionaries compatibile with your kindle device, you can download 
pre-compiled .mobi files in your preferred language from the 
[Releases](https://github.com/IanC27/lipu_nimi_pi_toki_pona/releases) page.

To load the dictionary onto your kindle, use [this guide](https://blog.the-ebook-reader.com/2015/07/14/kindle-dictionary-guide-how-to-add-change-and-create-custom-kindle-dictionaries/)

## Compiling your own dictionary

If you want a dictionary with the most up-to-date data from Linku, or want to do some customizing to your dictionary, then follow these steps to compile using the python scripts.

### Dependencies

You will need to have Python 3.10.5 or later installed: [download](https://www.python.org/downloads/)

Additionally, you will need a couple of python modules:

- Jinja2

`pip install Jinja2`

- Requests

`pip install requests`

Lastly you will need a tool to generate mobi files. The best way is to use [kindlegen](https://archive.org/details/kindlegen_202011). Download the executable and place it in the current directory or add it to path. The script will use it to generate your mobi for you.

Alternatively, you can use Amazon's current tool, [Kindle Previewer](https://www.amazon.com/Kindle-Previewer/b?ie=UTF8&node=21381691011). **However, it does not currently support exporting in a number of scripts, including Devanagari and Arabic.**

### How to Compile

To create your dictionary, run the python script `dict_file_gen.py` on the command line with the following arguments:

    usage: dict_file_gen.py [-h] [-a] [lang ...]

    create a Toki Pona dictionary mobi for use in kindles

    positional arguments:
      lang        the short id for the output language of the dictionary, as listed in the linku data

    options:
      -h, --help  show this help message and exit
      -a, --all   compile dictionaries for all languages available

For example,

    python dict_file_gen.py es

will generate a Toki Pona-Spanish dictionary.


If you specify no language, it will use English by default. 

To view all the languages available, their ids, % completeness, and more, `lang_table_gen.py` will create a document `supported_languages.html` which contains a table of that information.

Once you have run the main script, you should find new files in `dict_files/{language}/`.
If the script directory contains `kindlegen.exe`, you should see `tok-{ID}.mobi` is built and ready to load. If not, continue to the next section.

### Building a Mobi with Kindle Previewer

If using Kindle Previewer, select `File>Open Book` and then open the `.opf` file you generated earlier. It should only take a few seconds before you see a preview of your book. To create the mobi, click `File>Export` and then be sure to choose `Books(.mobi)` as the file type. Click ok through any warnings and you'll have your book.
    

## Resources Used
I used a patchwork of various tutorials to make the dictionary and the scripts to assemble them:
- [html templates for needed files, and guide on how to compile to mobi](https://jakemccrary.com/blog/2020/11/11/creating-a-custom-kindle-dictionary/)

- [using Jinja to fill templates with content](https://code-maven.com/minimal-example-generating-html-with-python-jinja)

- [txt method](https://1manfactory.com/create-your-own-kindle-dictionary-for-every-language-for-free/)
