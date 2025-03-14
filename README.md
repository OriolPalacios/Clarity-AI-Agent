# Clarity-AI-Agent-Mockup-repo

## Purpose

This repository is designed to perform data augmentation on a dataset comprised of:
- Questions
- Chain of Thought (CoT)
- Responses (code)

The augmented dataset will be used to apply Low-Rank Adaptation (LoRA) fine-tuning on the deepseek r1 model. The ultimate goal is to build an AI agent that assists developers in building decentralized applications (dapps) using Clarity for smart contracts.

## Tools

The following tools and libraries are used in this project:
- **Pandas**: For dataset manipulation and processing
- **OpenAI API**: For generating additional training data
- **PyTorch**: For model training and fine-tuning
- **Hugging Face Transformers**: For working with the deepseek r1 model
- **PEFT**: For efficient LoRA fine-tuning techniques

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


## Contributors

[![Joel Vegas](https://img.shields.io/badge/Joel-Vegas-orange)](https://github.com/joelvegas20)
[![Jonathan Nolasco](https://img.shields.io/badge/Jonathan-Nolasco-yellow)](https://github.com/jnolascob)
[![Oriol Palacios](https://img.shields.io/badge/Oriol-Palacios-red)](https://github.com/OriolPalacios)
