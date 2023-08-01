from sqlmodel import Session, select
from .models import User, Tag, Recommendation, RecommendationTagLink


def get_user_with_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()


def get_user_with_email(session: Session, email: str):
    return session.exec(select(User).where(User.email == email)).first()


def save_tags(session: Session, tags: list):
    tags_objects = []
    for tag in tags:
        tag: str = tag.strip().replace(' ', '-')
        existing_tag = session.exec(select(Tag).where(Tag.name == tag)).first()
        if existing_tag:
            tags_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag)
            # session.add(new_tag)
            # session.commit()
            # session.refresh(new_tag)
            tags_objects.append(new_tag)

    return tags_objects


def get_recommendation_by_id(session: Session, recommendation_id: int):
    return session.exec(select(Recommendation).join(RecommendationTagLink).join(Tag).
                        where(Recommendation.id == recommendation_id)).first()
