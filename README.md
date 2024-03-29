# Natural language processing course 2022/23: `Multillingual paraphrasing of sentences`

Team members:
 * `Jannik Weiß`, `70088643`, `jw30016@student.uni-lj.si`
 * `Nikolay Vasilev`, `63190338`, `nv7834@student.uni-lj.si`
 * `Jan Jenicek`, `70090030`, `jj86854@student.uni-lj.si`
 
Group public acronym/name: `TEAM 3435`
 > This value will be used for publishing marks/scores. It will be known only to you and not you colleagues.

# Objective

Being an international team, it makes sense for us use this situation to delve into multilingual language models. It is known that in other cross-lingual tasks multilingual models can outperform monolingual ones. Given that paraphrasing is not by default a cross-lingual task, but is closely related to translation, we aim to find out, whether a multilingually trained model performs in this task against a monolingual model as a baseline.

# How to run our code

First, please read the below sections to understand what we did. 
The folder `dataset-evaluation` contains the human evaluation framework and scripts for running the human evaluation as command line dialogues. In the paper we only include results from the scripts of the form `human_eval_tatoeba-xxxx_pc-xxxx.py`. These can be run with your name as a command line argument.
The folder `notebooks` contains all the notebooks used for dataset creation, training and evaluation. These can be run in a google standard colab environment with a GPU runtime.

# Data

The repository doesn't collect any new dataset. Instead, we have decided to leverage the already existing ones.
We use the [ParaCrawl](https://opus.nlpl.eu/ParaCrawl.php) dataset which consists of lots of sentences in different languages. We use maching translation models from [huggingface](https://huggingface.co/) to create paraphrase data from this translation dataset. While other multilingual parallel datasets include sentence pairs within a language (i.e. paraphrases), they include only few if any of these paraphrase sentence pairs in medium resource languages like Slovene. With our approach we create similarly sized paraphrase datasets for different languages including medium resource languages by leveraging translation data, which is more widely available than paraphrase data.

Our generated data can be accessed on huggingface:
- [ParaCrawl-enen](https://huggingface.co/datasets/yawnick/para_crawl_enen)
- [ParaCrawl-dede](https://huggingface.co/datasets/yawnick/para_crawl_dede)
- [ParaCrawl-slsl](https://huggingface.co/datasets/yawnick/para_crawl_slsl)
- [ParaCrawl-cscs](https://huggingface.co/datasets/yawnick/para_crawl_cscs)
- [ParaCrawl-multi_all](https://huggingface.co/datasets/yawnick/para_crawl_multi_all)
- [ParaCrawl-multi_small](https://huggingface.co/datasets/yawnick/para_crawl_multi_small)

## Dataset Evaluation

We evaluate the quality of our monolingual datasets via human evaluation of a dataset sample and in direct comparison to other popular paraphrase datasets. We evaluate semantic similarity and lexical divergence and calculate a score base on their combination. The human evaluation results of the 4 generated monolingual datasets are shown in the following table:

| Language | Our dataset | Tatoeba |
| --- | --- | --- |
| en-en | 0.256 | 0.307 |
| de-de | 0.291 | 0.588 |
| sl-sl | 0.271 | 0.015 |
| cs-cs | 0.189 | 0.210 |

# Models

We train 6 different [mt5 models](https://huggingface.co/google/mt5-base), one for each of the datasets we have created. We refer to these models as mono- and multilingual models, even though they are originally multilingual mt5 models, because we train them on the generated mono- and multilingual datasets.

Our trained models can be accessed on huggingface:
- [MT5_small-enen](https://huggingface.co/yawnick/mt5-small-paracrawl-enen)
- [MT5_small-dede](https://huggingface.co/yawnick/mt5-small-paracrawl-dede)
- [MT5_small-slsl](https://huggingface.co/yawnick/mt5-small-paracrawl-slsl)
- [MT5_small-cscs](https://huggingface.co/yawnick/mt5-small-paracrawl-cscs)
- [MT5_small-multi_all](https://huggingface.co/yawnick/mt5-small-paracrawl-mutli-all)
- [MT5_small-multi_small](https://huggingface.co/yawnick/mt5-small-paracrawl-multi-small)

## Model Evaluation

We used the Parascore metric to evaluate all models. The Parascore evaluation results of the 4 monolingual trained models are shown in the following table:

| Language | Parascore score|
| -------- | -------------- |
| en-en    | 0.961          |
| de-de    | 0.925          |
| sl-sl    | 0.890          |
| cs-cs    | 0.922          |

The Parascore evaluation results of the 2 multilingual trained models are shown in the following table, which also shows the average scores for each of the 4 different language subparts of the test split of the multilingual dataset:

| Language       | Score multi-small | Score multi-all |
| -------------- | ----------------- | --------------- |
| whole test set | 0.925             | 0.925           |
| English part   | 0.938             | 0.939           |
| German part    | 0.926             | 0.925           |
| Slovene part   | 0.915             | 0.914           |
| Czech part     | 0.922             | 0.922           |
