import os
from llama_index import GPTSimpleVectorIndex

from llama_index import (
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
    PromptHelper,
    LLMPredictor,
    ServiceContext,
)

from langchain.chat_models import ChatOpenAI

from openbb_terminal.core.session.current_user import get_current_user
from openbb_terminal.decorators import check_api_key
from openbb_terminal.rich_config import console
from openbb_terminal.core.config.paths import (
    MISCELLANEOUS_DIRECTORY,
)

INDEX_DIRECTORY = MISCELLANEOUS_DIRECTORY / "gpt_index/"
MODEL_NAME = "gpt-3.5-turbo"

current_user = get_current_user()
os.environ["OPENAI_API_KEY"] = current_user.credentials.API_OPENAI_KEY


def generate_index():
    # import from print console and say generating index, this might take a while
    console.print("Generating index, this might take a while...")

    # read in documents
    documents = SimpleDirectoryReader(INDEX_DIRECTORY / "data/").load_data()

    # define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name=MODEL_NAME))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    index = GPTSimpleVectorIndex.from_documents(
        documents=documents, service_context=service_context
    )

    return index


@check_api_key(["API_OPENAI_KEY"])
def query_LLM(query_text):
    # check if index exists
    if os.path.exists(INDEX_DIRECTORY / "index.json"):
        index = GPTSimpleVectorIndex.load_from_disk(INDEX_DIRECTORY / "index.json")
    else:
        index = generate_index()

        # save to disk
        index.save_to_disk(INDEX_DIRECTORY / "index.json")

    response = index.query(
        f"""From argparse help text above, provide the command for {query_text}.
        Provide the exact command to get that information, and nothing else.
        If and only if there is no information in the argparse help text above, say I don't know.
        """
    )

    return response.response
