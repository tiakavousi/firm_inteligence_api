from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import knowledge
from anthropic import APIStatusError,APITimeoutError,RateLimitError
import llm


# Relevance floor
# below this we treat the retrived context as not relevance
RELEVANCE_FLOOR = 0.35

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

class Question(BaseModel):
    question:str = Field(min_length=3)
    top_k:int = Field(default=3, gt=0, lt=8)

@router.post("/index")
def rebuild_index():
    """
    embed the corpus, costs tokens so it is a deliberate POST rather than embeded in the application
    """
    tokens = knowledge.build_index()
    return {"indexed": len(knowledge.INDEX), "embeddings_tokens": tokens}

@router.post("/search")
def search_query(query: Question):
    try:
        return knowledge.search(query.question, query.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/ask")
def ask(q:Question):
    "Retieve, then answer using only what was retrieved ... or refuse"
    # 1. Retrieve
    # same call as /knowledge/search
    # 2. Filter, and decide whether to make a call to the model at all
    # (compare against the RELEVANCE_FLOOR)
    # 3. Build context and generate the answer
    # 4. Return the successful answer