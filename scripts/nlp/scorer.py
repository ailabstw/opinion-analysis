import torch

from transformers import BertTokenizer, BertForSequenceClassification


class SentimentScorer:

    def __init__(self, model_path):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(
            model_path, num_labels=1)
        self.cuda_flag = False

    def process(self, texts):
        input_ids, attention_masks, = self.make_inputs_from_batch(texts)
        input_ids = self.cudalize(input_ids)
        attention_masks = self.cudalize(attention_masks)

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids,
                                 attention_mask=attention_masks)
        scores = torch.sigmoid(outputs[0].squeeze(-1)).tolist()
        return scores

    def make_inputs_from_batch(self, texts):
        tokenized_output = self.tokenizer.batch_encode_plus(texts, pad_to_max_length=True,
                                                            return_attention_masks=True,
                                                            return_lengths=True,
                                                            max_length=min(512))
        input_ids = tokenized_output['input_ids']
        input_ids = torch.LongTensor(input_ids)
        attention_masks = tokenized_output['attention_mask']
        attention_masks = torch.LongTensor(attention_masks)
        return input_ids, attention_masks

    def to(self, device):
        if device == 'cuda':
            self.cuda_flag = True
        elif device == 'cpu':
            self.cuda_flag = False
        else:
            raise ValueError(f'Unknown device: {device}')
        self.model = self.cudalize(self.model)

    def cudalize(self, x):
        if self.cuda_flag is False:
            return x.cpu()
        return x.cuda()
