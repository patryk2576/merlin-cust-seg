# merlin-cust-seg

A customer segmentation project that clusters customer data and provides a Streamlit chatbot interface for querying insights.

## Pre-requisites
- Please ensure you have installed uv (https://docs.astral.sh/uv/)
- Once uv has been installed, please install the required dependencies by running: `uv sync` within the project directory
- Please ensure you have added a `.env` file containing your API key: `OPENAI_API_KEY=your-key-here`

## Running the Streamlit chatbot
- To run the Streamlit chatbot, run the following: `uv run streamlit run main.py`
- This should launch your web browser automatically; if not, navigate to the localhost URL shown in the terminal.
- The chatbot allows you to query the customer segmentation results interactively.

## Project structure
| File | Description |
|------|-------------|
| `main.py` | Streamlit chatbot application |
| `eda.ipynb` | Jupyter notebook for exploratory data analysis, clustering, and outputting the final processed data |

## eda.ipynb notebook
- Reads raw customer data, performs exploratory data analysis, applies clustering algorithms, and outputs the final segmented dataset used by the chatbot.