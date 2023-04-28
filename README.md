# Natural language processing course 2022/23: `Paraphrasing sentences`

Team members:
 * `Jannik Weiß`, `70088643`, `jw30016@student.uni-lj.si`
 * `Nikolay Vasilev`, `63190338`, `nv7834@student.uni-lj.si`
 * `Jan Jenicek`, `70090030`, `jj86854@student.uni-lj.si`
 
Group public acronym/name: `TEAM 3435`
 > This value will be used for publishing marks/scores. It will be known only to you and not you colleagues.

# Objective

Being an international Teamit makes sense for us use this situation to delve into multilingual language models. It is known that in other cross-lingual tasks multilingual models can outperform monolingual ones. Given that paraphrasing is not by default a cross-lingual task, but is closely related to translation, we aim to find out a multilingually trained model performs in this task against a monolingual model as a baseline.

# Data

The repository doesn't collect any new dataset. Instead, we have decided to leverage the already existing ones.
We use the [ParaCrawl](https://opus.nlpl.eu/ParaCrawl.php) dataset which consists of lots of sentences in different languages. We use maching translation models from [huggingface](https://huggingface.co/) to create paraphrase data from this translation dataset. While other multilingual parallel datasets include sentence pairs within a language (i.e. paraphrases), they include only few if any of these paraphrase sentence pairs in medium resource languages like Slovene. With our approach we create similarly sized paraphrase datasets for different languages including medium resource languages by leveraging translation data, which is more widely available than paraphrase data.

Our generated data can be accessed on huggingface:
- [ParaCrawl-enen](https://huggingface.co/datasets/yawnick/para_crawl_enen)
- [ParaCrawl-dede](https://huggingface.co/datasets/yawnick/para_crawl_dede)
- ParaCrawl-slsl
- ParaCrawl-cscs

### Dataset Evaluation

We evaluate the quality of our datasets via human evaluation of a dataset sample and in direct comparison to other popular paraphrase datasets. We evaluate semantic similarity and lexical divergence and calculate a score base on their combination.

| Language | Our dataset | Tatoeba |
| --- | --- | --- |
| en-en | 0.256 | 0.307 |