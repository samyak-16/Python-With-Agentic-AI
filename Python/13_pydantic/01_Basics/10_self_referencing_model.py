from typing import List, Optional
from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    content: str
    replies: Optional[List["Comment"]] = None


Comment.model_rebuild()  # rebuilds the class validation by converting the string "Comment" into actual class object , at this point the class is already completed building itslef so no any Comment not defined error


comment1 = Comment(
    id=1,
    content="Nice post!",
    replies=[
        Comment(
            id=2,
            content="Thanks!",
            replies=[Comment(id="a", content="Welcome!", replies=None)],
        )
    ],
)

print(comment1)
