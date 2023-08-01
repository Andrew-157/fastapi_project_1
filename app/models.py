from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .schemas import UserBase, RecommendationBase, TagBase


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    recommendations: list["Recommendation"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "delete"})


class RecommendationTagLink(SQLModel, table=True):
    recommendation_id: int | None = Field(
        default=None, foreign_key="recommendation.id", primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )


class Recommendation(RecommendationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    published: datetime = Field(nullable=True, default=datetime.utcnow())
    updated: datetime | None = Field(default=None)
    user_id: int = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="recommendations")
    tags: list["Tag"] = Relationship(back_populates="recommendations",
                                     link_model=RecommendationTagLink)


class Tag(TagBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    recommendations: list[Recommendation] = Relationship(back_populates="tags",
                                                         link_model=RecommendationTagLink)
