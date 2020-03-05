# Data Conversion Tool for Image Position Prediction

This tool generates a dataset for Image Position Prediction task which is proposed in [our paper](#reference).

## Requirements
- `pip install -r requirements.txt`

    We tested our tool in the following packages.
```
    Python==3.7.0
    pip==20.0.1
    beautifulsoup4==4.8.2
    gensim==3.7.0
    numpy==1.14.2
    Pillow==7.0.0
    requests==2.22.0
```

- Download the latest Wikipedia<sup>[1](#footnote1)</sup> dump `enwiki-*-pages-articles.xml.bz2` from https://dumps.wikimedia.org/backup-index.html.

    This tool takes a Wikipedia dump as an input. You can run the tool on your own responsibility. By using our tool, you agree to [Wikimedia's Terms of Use](https://foundation.wikimedia.org/wiki/Terms_of_Use/en), [Reusers' rights and obligations](https://en.wikipedia.org/wiki/Wikipedia:Copyrights#Reusers.27_rights_and_obligations), [Reusing Wikipedia content page](https://en.wikipedia.org/wiki/Wikipedia:Reusing_Wikipedia_content), and [Reusing Wikimedia Commons content page](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia).

## Usage
Follow the instruction in [data_creation_procedure.txt](./data_creation_procedure.txt)

The final output of this tool is a collection of Wikipedia articles, which are separated by directories, i.e., one directory per one article. The structure in each directory is below:

```
${ARTICLE_NAME}/
  |-- doc.xml : an article text marked with section and image position information
  |-- doc.json : JSON format converted from doc.xml
  |-- *.jpeg : image files in JPEG format
  |-- info/ : additional information stored
        |-- *.license : license information of images
        |-- removed.json : modified parts from the original text
``` 

If you want to access the original articles, the link can be found in the `url` attribute of the `<doc>` tag in the `doc.xml` file. 

```<doc id="12" title="Anarchism" url="https://en.wikipedia.org/wiki?curid=12">```

Also, the original images can be accessed at `https://en.wikipedia.org/wiki/${IMAGE_FILE}`, where `${IMAGE_FILE}` is a value of the `name` attribute of the `<image>` tag in the `doc.xml` file. 

```<image id="0" name="File:Paolo Monti - Servizio fotografico (Napoli, 1969) - BEIC 6353768.jpg">```

## Reference
If you use this tool, please cite:
> Masayasu Muraoka, Ryosuke Kohita, and, Etsuko Ishii. "Image Position Prediction in Multimodal Documents." LREC. 2020.

## Notice
This repository and tool are licensed under [Apache 2.0](./LICENSE). 

(c) Copyright IBM Corporation 2020.

<a name="footnote1">1</a>: Wikimedia Wordmark is a trademark of the Wikimedia Foundation and is used with the permission of the Wikimedia Foundation. We are not endorsed by or affiliated with the Wikimedia Foundation.
