from datasets import load_dataset
from transformers import T5Tokenizer, AutoTokenizer, MT5ForConditionalGeneration, DataCollatorForSeq2Seq, Seq2SeqTrainer, Seq2SeqTrainingArguments
from parascore import ParaScorer
import numpy as np

raw_datasets = load_dataset('glue', 'mrpc')

raw_datasets_train = raw_datasets['train']
raw_datasets_val = raw_datasets['validation']
raw_datasets_test = raw_datasets['test']

ds_train = raw_datasets_train.filter(lambda x: x['label']==1)
ds_val = raw_datasets_val.filter(lambda x: x['label']==1)
ds_test = raw_datasets_test.filter(lambda x: x['label']==1)

checkpoint = 'google/mt5-small'
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

max_length = 128

# the prefix has to (dynamically) be adjusted depending on the language or when training multilingually (I think).
prefix = 'paraphrase: '

def preprocess_function(examples):
    inputs = [prefix+s1 for s1 in examples['sentence1']]
    targets = examples['sentence2']
    # most likely there will be nothing to truncate, but we still add it
    model_inputs = tokenizer(inputs, text_target=targets, max_length=max_length, truncation=True)
    return model_inputs

tokenized_ds_train = ds_train.map(
    preprocess_function,
    batched=True,
    remove_columns=ds_train.column_names
)
tokenized_ds_val = ds_val.map(
    preprocess_function,
    batched=True,
    remove_columns=ds_val.column_names
)
tokenized_ds_test = ds_test.map(
    preprocess_function,
    batched=True,
    remove_columns=ds_test.column_names
)

model = MT5ForConditionalGeneration.from_pretrained(checkpoint)

data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

scorer = ParaScorer(lang='en', model_type='bert-base-uncased')

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    # In case the model returns more than the prediction logits
    if isinstance(preds, tuple):
        preds = preds[0]

    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100s in the labels as we can't decode them
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [label.strip() for label in decoded_labels]
    print(decoded_preds[:5])
    print(decoded_labels[:5])
    
    parascore = scorer.free_score(decoded_preds, decoded_labels)
    return {'parascore': float(parascore[-1].mean())}

args = Seq2SeqTrainingArguments(
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy='steps',
    logging_steps=50,
    output_dir='.',
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=3,
    predict_with_generate=True,
)

trainer = Seq2SeqTrainer(
    model,
    args,
    train_dataset=tokenized_ds_train,
    eval_dataset=tokenized_ds_val,
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()