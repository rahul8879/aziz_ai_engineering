# aziz_ai_engineering

Hands-on AI engineering practice repo — LangChain basics, prompt engineering, and NLP/RAG.

## Repo structure

| Folder | What's inside |
| --- | --- |
| `00_langchain_learning/` | LangChain basics, Pydantic structured output |
| `01_prompt_engineering/` | Prompting patterns, memory, tool calling, pipelines (`.py` + notebooks) |
| `02_NLP_RAG/` | NLP and RAG experiments |
| `learning.md` | Running notes |

## 1. Get the code

First time:

```bash
git clone https://github.com/rahul8879/aziz_ai_engineering.git
cd aziz_ai_engineering
```

To pull the latest code later:

```bash
git pull origin main
```

If you have local changes and want to keep them while pulling:

```bash
git stash          # park your changes
git pull origin main
git stash pop      # bring them back
```

## 2. Create the virtual environment

Requires Python 3.11+ (developed on 3.13).

```bash
python3 -m venv ai-env
```

## 3. Activate the virtual environment

macOS / Linux:

```bash
source ai-env/bin/activate
```

Windows (PowerShell):

```powershell
ai-env\Scripts\Activate.ps1
```

Windows (cmd):

```cmd
ai-env\Scripts\activate.bat
```

To leave the environment: `deactivate`

## 4. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

To run the notebooks as well:

```bash
pip install jupyter ipykernel
```

## 5. Set up your API key

Create a `.env` file in the project root (it is git-ignored, never commit it):

```bash
OPENAI_API_KEY=sk-your-key-here
```

The code loads it with `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()
```

- Create an OpenAI API key: https://platform.openai.com/home
- List of models available in OpenAI: https://developers.openai.com/api/docs/models

## 6. Run something

Python scripts:

```bash
python 01_prompt_engineering/v0_naive.py
```

Notebooks:

```bash
jupyter notebook
```

Then open any `.ipynb` and select the `ai-env` kernel.

## Adding a new package

```bash
pip install <package>
pip freeze | grep -i <package> >> requirements.txt   # or add the name manually
```

## Push your changes

```bash
git add .
git commit -m "your message"
git push origin main
```