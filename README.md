# OpenTTD & LLM

Use an LLM to drive an OpenTTD AI. ([More on my personal blog](https://jplattel.nl/post/llm-plays-openttd/)) 

## Getting started

1.  Install dependencies with `uv sync`
2.  Symlink the OpenTTDLLM to <openttd_data_folder>/ai/OpenTTDLLM
3.  Startup OpenTTD and the LLM interface: `uv run main.py`
4.  Start the AI through the in-game console with `start_ai OpenTTDLLM`

As a proof of concept it'll get the maps dimensions, bank balance and loan amount... It ain't building something (yet!) 

## Architecture

1 shot with OpenAI:

![A circulair architecture](https://files.jplattel.nl/2026/01/PWlJvx.png)

## Example screenhot

![Example screenshot of the log](https://files.jplattel.nl/2026/01/peObxN.png)