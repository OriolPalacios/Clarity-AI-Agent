# Clarity-AI-Agent

## Demo Video

[![YouTube Demo](https://img.shields.io/badge/Youtube-Demo-red)](https://www.youtube.com/watch?v=Zjf2j64ZgrA)

## Overview

Clarity-AI-Agent is a project aimed at enhancing the development of decentralized applications (dApps) by fine-tuning AI models to assist developers in writing smart contracts using the Clarity language. The project focuses on data augmentation techniques to enrich a dataset containing questions, chain-of-thought (CoT) processes, and code responses, which are then utilized to fine-tune the deepseek r1 model using Low-Rank Adaptation (LoRA).

### Clarity AI Extension

[Clarity AI Agent Extension](https://github.com/joelvegas20/clarity-ia-agent-extension)

## Installation

[![Python 3.13.1](https://img.shields.io/badge/python-3.13.1-blue.svg)](https://www.python.org/downloads/release/python-3131/)
[![venv](https://img.shields.io/badge/venv-virtual_environment-green.svg)](https://docs.python.org/3/library/venv.html)

1. Make sure you have Python 3.13.1 installed.
2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Data Augmentation

We rely on gemini 2.0 flash, gemini 2.0 pro, and qwen qwq to paraphrase questions and chain-of-thought (CoT) segments using openrouter. We exclude code responses from this process to prevent hallucinations, ensuring the integrity of the generated content.

The following tools and libraries are used in this project:
- **Pandas**: For dataset manipulation and processing
- **OpenAI API**: For generating additional training data
- **PyTorch**: For model training and fine-tuning
- **Hugging Face Transformers**: For working with the deepseek r1 model
- **PEFT**: For efficient LoRA fine-tuning techniques



## Pretrained Model

The fine-tuned model is available on Hugging Face:
[![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-DeepSeek--R1--Clarity--AI--Agent-blue)](https://huggingface.co/OriolPalacios/DeepSeek-R1-Clarity-AI-Agent-2/tree/main)

You can access and download all model files from the repository above to use the fine-tuned DeepSeek-R1 model for Clarity smart contract development.

## Training Metrics

Training metrics and experiment tracking are available on Weights & Biases:
[![Weights & Biases](https://img.shields.io/badge/📊_Weights_&_Biases-Training_Report-yellow)](https://wandb.ai/oriol_palacios-universidad-nacional-de-san-antonio-abad-/Fine-tune-DeepSeek-R1-Distill-Llama-8B%20on%20Clarity%20Dataset%20for%20Clarity-AI-Agent?nw=nwuseroriol_palacios)

This report contains detailed information about the fine-tuning process, including loss curves, evaluation metrics, and hyperparameter configurations used during model training.

## Contributors

[![Joel Vegas](https://img.shields.io/badge/Joel-Vegas-orange)](https://github.com/joelvegas20)
[![Jonathan Nolasco](https://img.shields.io/badge/Jonathan-Nolasco-yellow)](https://github.com/jnolascob)
[![Oriol Palacios](https://img.shields.io/badge/Oriol-Palacios-red)](https://github.com/OriolPalacios)
