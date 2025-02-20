
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import random
import math
import numpy as np

Image.MAX_IMAGE_PIXELS = 1000000000

max_token  = {
    'docVQA': 100,
    'textVQA': 100,
    "docVQATest": 100
}

class MiniCPM_V:

    def __init__(self, model_path, ckpt, device=None)->None:
        self.model_path = model_path
        self.ckpt = ckpt
        self.model = AutoModel.from_pretrained(self.model_path, trust_remote_code=True).eval()
        if self.ckpt is not None:
            self.ckpt = ckpt
            self.state_dict = torch.load(self.ckpt, map_location=torch.device('cpu'))
            self.model.load_state_dict(self.state_dict)
            
        self.model = self.model.to(dtype=torch.float16)
        self.model.to(device)
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        torch.cuda.empty_cache()

    def generate(self, images, questions, datasetname):
        image = Image.open(images[0]).convert('RGB')
        max_new_tokens = max_token[datasetname]

        prompt = "Answer the question directly with single word." + '\n' + questions[0]
        
        msgs = [{'role': 'user', 'content': prompt}]
        default_kwargs = dict(
            max_new_tokens=max_new_tokens,
            sampling=False,
            num_beams=3
        )
        res = self.model.chat(
            image=image,
            msgs=msgs,
            context=None,
            tokenizer=self.tokenizer,
            **default_kwargs
        )
        
        return [res]
    
    def generate_with_interleaved(self, images, questions, datasetname):
        max_new_tokens = max_token[datasetname]
        
        prompt = "Answer the question directly with single word."
        
        default_kwargs = dict(
            max_new_tokens=max_new_tokens,
            sampling=False,
            num_beams=3
        )
        
        content = []
        message = [
            {'type': 'text', 'value': prompt},
            {'type': 'image', 'value': images[0]},
            {'type': 'text', 'value': questions[0]}
        ]
        for x in message:
            if x['type'] == 'text':
                content.append(x['value'])
            elif x['type'] == 'image':
                image = Image.open(x['value']).convert('RGB')
                content.append(image)
        msgs = [{'role': 'user', 'content': content}]

        res = self.model.chat(
            image=None,
            msgs=msgs,
            context=None,
            tokenizer=self.tokenizer,
            **default_kwargs
        )

        if isinstance(res, tuple) and len(res) > 0:
            res = res[0]
        print(f"Q: {content}, \nA: {res}")
        return [res]


class MiniCPM_V_2_6:

    def __init__(self, model_path, ckpt, device=None)->None:
        random.seed(0)
        np.random.seed(0)
        torch.manual_seed(0)
        torch.cuda.manual_seed_all(0)
        
        self.model_path = model_path
        self.ckpt = ckpt
        self.model = AutoModel.from_pretrained(self.model_path, trust_remote_code=True).eval()
        if self.ckpt is not None:
            self.ckpt = ckpt
            self.state_dict = torch.load(self.ckpt, map_location=torch.device('cpu'))
            self.model.load_state_dict(self.state_dict)

        self.model = self.model.to(dtype=torch.bfloat16)
        self.model.to(device)
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        torch.cuda.empty_cache()

    def generate(self, images, questions, datasetname):
        image = Image.open(images[0]).convert('RGB')
        img_width, img_height = image.width, image.height
        if (img_width * img_height) < (1344 * 1344):
            ratio = math.sqrt((1344 * 1344) / (img_width * img_height))
            max_img_width = int(img_width * ratio)
            new_img_width = random.randint(img_width, max_img_width)
            new_img_height = int(new_img_width / img_width * img_height)
            image = image.resize((new_img_width, new_img_height))
        
        max_new_tokens = max_token[datasetname]
            
        prompt = "Answer the question directly with single word." + '\n' + questions[0]
        
        msgs = [{'role': 'user', 'content': prompt}]
        default_kwargs = dict(
            max_new_tokens=max_new_tokens,
            sampling=False,
            num_beams=3
        )
        res = self.model.chat(
            image=image,
            msgs=msgs,
            context=None,
            tokenizer=self.tokenizer,
            **default_kwargs
        )
        
        return [res]
    
    def generate_with_interleaved(self, images, questions, datasetname):
        max_new_tokens = max_token[datasetname]
        
        prompt = "Answer the question directly with single word."
        
        default_kwargs = dict(
            max_new_tokens=max_new_tokens,
            sampling=False,
            num_beams=3
        )
        
        content = []
        message = [
            {'type': 'text', 'value': prompt},
            {'type': 'image', 'value': images[0]},
            {'type': 'text', 'value': questions[0]}
        ]
        for x in message:
            if x['type'] == 'text':
                content.append(x['value'])
            elif x['type'] == 'image':
                image = Image.open(x['value']).convert('RGB')
                img_width, img_height = image.width, image.height
                if (img_width * img_height) >= (1344 * 1344):
                    content.append(image)
                else:
                    ratio = math.sqrt((1344 * 1344) / (img_width * img_height))
                    max_img_width = int(img_width * ratio)
                    new_img_width = random.randint(img_width, max_img_width)
                    new_img_height = int(new_img_width / img_width * img_height)
                    resized_image = image.resize((new_img_width, new_img_height))
                    content.append(resized_image)
        msgs = [{'role': 'user', 'content': content}]

        res = self.model.chat(
            image=None,
            msgs=msgs,
            context=None,
            tokenizer=self.tokenizer,
            **default_kwargs
        )

        if isinstance(res, tuple) and len(res) > 0:
            res = res[0]

        return [res]


class MiniCPM_o_2_6:

    def __init__(self, model_path, ckpt, device=None)->None:
        random.seed(0)
        np.random.seed(0)
        torch.manual_seed(0)
        torch.cuda.manual_seed_all(0)
        
        self.model_path = model_path
        self.ckpt = ckpt
        self.model = AutoModel.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            attn_implementation='sdpa',
            torch_dtype=torch.bfloat16,
            init_vision=True,
            init_audio=False,
            init_tts=False
        )
        if self.ckpt is not None:
            self.ckpt = ckpt
            self.state_dict = torch.load(self.ckpt, map_location=torch.device('cpu'))
            self.model.load_state_dict(self.state_dict)

        self.model = self.model.eval().to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        torch.cuda.empty_cache()

    def generate(self, images, questions, datasetname):
        image = Image.open(images[0]).convert('RGB')
        img_width, img_height = image.width, image.height
        if (img_width * img_height) < (1344 * 1344):
            ratio = math.sqrt((1344 * 1344) / (img_width * img_height))
            max_img_width = int(img_width * ratio)
            new_img_width = random.randint(img_width, max_img_width)
            new_img_height = int(new_img_width / img_width * img_height)
            image = image.resize((new_img_width, new_img_height))     

        max_new_tokens = max_token[datasetname]

        prompt = "Answer the question directly with single word." + '\n' + questions[0]
        
        msgs = [{'role': 'user', 'content': prompt}]
        default_kwargs = dict(
            max_new_tokens=max_new_tokens,
            sampling=False,
            num_beams=3,
            max_inp_length=8192,
            use_image_id=True,
            max_slice_nums=None
        )
        res = self.model.chat(
            image=image,
            msgs=msgs,
            context=None,
            tokenizer=self.tokenizer,
            **default_kwargs
        )
        
        return [res]
    
    def generate_with_interleaved(self, images, questions, datasetname):
        max_new_tokens = max_token[datasetname]
        
        prompt = "Answer the question directly with single word."
        
        default_kwargs = dict(
            max_new_tokens=max_new_tokens,
            sampling=False,
            num_beams=3,
            max_inp_length=8192,
            use_image_id=True,
            max_slice_nums=None
        )
        
        content = []
        message = [
            {'type': 'text', 'value': prompt},
            {'type': 'image', 'value': images[0]},
            {'type': 'text', 'value': questions[0]}
        ]
        for x in message:
            if x['type'] == 'text':
                content.append(x['value'])
            elif x['type'] == 'image':
                image = Image.open(x['value']).convert('RGB')
                img_width, img_height = image.width, image.height
                if (img_width * img_height) >= (1344 * 1344):
                    content.append(image)
                else:
                    ratio = math.sqrt((1344 * 1344) / (img_width * img_height))
                    max_img_width = int(img_width * ratio)
                    new_img_width = random.randint(img_width, max_img_width)
                    new_img_height = int(new_img_width / img_width * img_height)
                    resized_image = image.resize((new_img_width, new_img_height))
                    content.append(resized_image)
        msgs = [{'role': 'user', 'content': content}]

        res = self.model.chat(
            image=None,
            msgs=msgs,
            context=None,
            tokenizer=self.tokenizer,
            **default_kwargs
        )

        if isinstance(res, tuple) and len(res) > 0:
            res = res[0]
        print(f"Q: {content}, \nA: {res}")
        return [res]