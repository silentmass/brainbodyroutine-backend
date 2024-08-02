import os
from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException
from groq import Groq
import re

from backend.api.src.routes.croq.schemas import (
    CroqSearchQueryBase,
    CroqSearchQueryResponse,
)

config = {
    **dotenv_values(".env.development"),  # load shared development variables
    # **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

router_croq = APIRouter(prefix="/api/croq", tags=["Croq"])


@router_croq.post("/search", response_model=CroqSearchQueryResponse)
async def search_suggestions(searchQuery: CroqSearchQueryBase):
    if searchQuery.searchQuery == "":
        raise HTTPException(status_code=400, detail="Query is empty")

    client = Groq(
        api_key=f"{config.get('GROQ_API_KEY')}",
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "".join(
                    [
                        "Questions should be maximum of 50 characters.",
                        "Simplify questions.",
                        "No fancy words.",
                        "Keep questions neutral.",
                        "Suggest four most asked questions related to: ",
                        f"{searchQuery.searchQuery}",
                    ]
                ),
            }
        ],
        model="llama3-8b-8192",
    )

    content = chat_completion.choices[0].message.content.split("\n")
    questions = [
        e.replace(re.search(r"^\d{1,}. ", e)[0], "")
        for (idx, e) in enumerate(content)
        if idx > 0 and e != ""
    ]

    print(questions)

    return {"searchQueryResult": questions}
