# Natural language processing course 2022/23: `Paraphrasing sentences`

Team members:
 * `Jannik Weiß`, `70088643`, `jw30016@student.uni-lj.si`
 * `Nikolay Vasilev`, `63190338`, `nv7834@student.uni-lj.si`
 * `Jan Jenicek`, `70090030`, `jj86854@student.uni-lj.si`
 
Group public acronym/name: `TEAM 3435`
 > This value will be used for publishing marks/scores. It will be known only to you and not you colleagues.

 # Data

 The repository doesn't collect any new dataset. Instead, we have decided to laverage the already existing ones.

 ## PPDB

 The paraphrase.org dataset (**PPDB**) dataset can be downloaded  [here](http://paraphrase.org/#/download). 

 Utilities for working with the dataset are implemented in [datautils](https://github.com/UL-FRI-NLP-Course-2022-23/nlp-course-team-3435/blob/master/src/datautils.py).

Example of using the data parser: 

```
import datautils

PATH = "<YOUR_LOCAL_PATH>"

with open(PATH, "r") as file_ppdb:
    for data in datautils.parse_data_ppdb(file_ppdb):
        # work with the data here
        pass

```
