# Load necessary libraries and dependencies
import torch
import transformers
import pandas as pd
import numpy as np
import os

# Load your private codebase
data_dir = "/path/to/your/private/codebase"
train_df = pd.read_csv(os.path.join(data_dir, "train.csv"))
test_df = pd.read_csv(os.path.join(data_dir, "test.csv"))

# Set up the language model
model_name = "microsoft/CodeGPT-small-java"
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
model = transformers.AutoModelWithLMHead.from_pretrained(model_name)

# Fine-tune the language model on your private code
train_dataset = transformers.TextDataset(
    tokenizer=tokenizer,
    file_path=os.path.join(data_dir, "train.csv"),
    block_size=128
)
train_loader = transformers.DataLoader(train_dataset, batch_size=8, shuffle=True)
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)
for epoch in range(3):
    for batch in train_loader:
        inputs, labels = batch
        inputs = inputs.to(model.device)
        labels = labels.to(model.device)
        outputs = model(inputs, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        model.zero_grad()

# Generate code suggestions from the fine-tuned language model
test_dataset = transformers.TextDataset(
    tokenizer=tokenizer,
    file_path=os.path.join(data_dir, "test.csv"),
    block_size=128
)
test_loader = transformers.DataLoader(test_dataset, batch_size=8)
predictions = []
for batch in test_loader:
    inputs, labels = batch
    inputs = inputs.to(model.device)
    generated = model.generate(inputs, max_length=128, do_sample=True, top_k=50, top_p=0.95, temperature=0.8)
    for g in generated:
        prediction = tokenizer.decode(g, skip_special_tokens=True)
        predictions.append(prediction)
