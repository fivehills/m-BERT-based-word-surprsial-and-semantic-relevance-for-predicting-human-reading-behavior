
#################################################
###use BERT-base to compute as an example  ######
###p(target word |left context), left context 
within one given sentence
#################################################


from transformers import BertTokenizer, BertForMaskedLM
import torch
import torch.nn.functional as F

# Initialize the tokenizer and the model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

# Define the left context and the target word
left_context = 'I like to eat'
target_word = 'apple'

# Tokenize the left context and the target word separately
left_context_tokens = tokenizer.tokenize(left_context)
target_word_tokens = tokenizer.tokenize(target_word)

# Concatenate the left context and the target word with the separator token
input_tokens = left_context_tokens + ['[SEP]'] + target_word_tokens

# Convert the input tokens to IDs
input_ids = tokenizer.convert_tokens_to_ids(input_tokens)

# Generate the attention mask and the segment IDs
attention_mask = [1] * len(input_ids)
segment_ids = [0] * len(left_context_tokens) + [1] * (len(target_word_tokens) + 1)

# Convert the input to PyTorch tensors
input_ids = torch.tensor([input_ids])
attention_mask = torch.tensor([attention_mask])
segment_ids = torch.tensor([segment_ids])

# Feed the input to the model and get the output
with torch.no_grad():
    outputs = model(input_ids, attention_mask=attention_mask, token_type_ids=segment_ids)
    logits = outputs.logits

# Find the index of the target word in the input tokens
target_word_index = input_tokens.index(target_word)

# Get the logits corresponding to the target word
target_logits = logits[0][target_word_index]

# Compute the probability using a softmax function
probabilities = F.softmax(target_logits, dim=-1)
probability = probabilities[tokenizer.convert_tokens_to_ids(target_word)].item()

print(f"The probability of '{target_word}' given '{left_context}' is {probability:.4f}")



##Prepare the input: Concatenate the left context and the target word with a special separator token (e.g., [SEP]) in between. For example, if you want to compute the probability of the word "apple" given the left context "I like to eat", the input to BERT would be "I like to eat [SEP] apple".

##Tokenize the input: Use BERT's tokenizer to convert the input into a sequence of tokens that BERT can understand.

##Generate input IDs, attention masks, and segment IDs: BERT requires three types of input: input IDs, attention masks, and segment IDs. Input IDs are token IDs generated by the tokenizer, attention masks indicate which tokens BERT should pay attention to, and segment IDs indicate which part of the input (left context or target word) each token belongs to.

##Feed the input to BERT: Pass the input IDs, attention masks, and segment IDs to BERT and get the output. BERT will output a sequence of hidden states, one for each token in the input.

##Extract the hidden state for the target word: Find the hidden state corresponding to the target word in the output of BERT.

##Compute the probability: The probability of the target word given the left context can be computed using a softmax function applied to the dot product between the hidden state of the target word and the final layer weights of BERT.



###############################################################################################
#########use multilingual BERT to compute p(word|left context) for different languages###
######### the left context is within one given sentence##################################
################################################################################################

from transformers import BertTokenizer, BertForMaskedLM
import torch
import torch.nn.functional as F

# Initialize the tokenizer and the model
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertForMaskedLM.from_pretrained('bert-base-multilingual-cased')

# Define the left context and the target word in a language of your choice
left_context = 'Je vais au'
target_word = 'cinéma'

# Tokenize the left context and the target word separately
left_context_tokens = tokenizer.tokenize(left_context)
target_word_tokens = tokenizer.tokenize(target_word)

# Concatenate the left context and the target word with the separator token
input_tokens = left_context_tokens + ['[SEP]'] + target_word_tokens

# Convert the input tokens to IDs
input_ids = tokenizer.convert_tokens_to_ids(input_tokens)

# Generate the attention mask and the segment IDs
attention_mask = [1] * len(input_ids)
segment_ids = [0] * len(left_context_tokens) + [1] * (len(target_word_tokens) + 1)

# Convert the input to PyTorch tensors
input_ids = torch.tensor([input_ids])
attention_mask = torch.tensor([attention_mask])
segment_ids = torch.tensor([segment_ids])

# Feed the input to the model and get the output
with torch.no_grad():
    outputs = model(input_ids, attention_mask=attention_mask, token_type_ids=segment_ids)
    logits = outputs.logits

# Get the logits corresponding to the target word
target_word_index = input_tokens.index(target_word) if target_word in input_tokens else -1
if target_word_index == -1:
    print(f"Unable to find target word '{target_word}' in input tokens.")
else:
    target_logits = logits[0][target_word_index]

    # Compute the probability using a softmax function
    probabilities = F.softmax(target_logits, dim=-1)
    probability = probabilities[tokenizer.convert_tokens_to_ids(target_word)].item()

    print(f"The probability of '{target_word}' given '{left_context}' is {probability:.4f}")

