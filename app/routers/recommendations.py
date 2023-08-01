from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path, HTTPException, status
from sqlmodel import Session, select

from ..auth import get_current_user
from ..database import get_session
from ..schemas import RecommendationCreate, RecommendationRead
from ..models import User, Recommendation, Tag
from ..crud import save_tags, get_recommendation_by_id


router = APIRouter(
    tags=['recommendations'],
)


@router.post('/recommend',
             response_model=RecommendationRead,
             status_code=status.HTTP_201_CREATED)
async def post_recommendation(data: Annotated[RecommendationCreate, Body()],
                              current_user: Annotated[User, Depends(get_current_user)],
                              session: Annotated[Session, Depends(get_session)]):
    tags = save_tags(session=session, tags=data.tags)
    recommendation = Recommendation(
        type_of_fiction=data.type_of_fiction,
        title=data.title,
        short_description=data.short_description,
        opinion=data.opinion,
        tags=tags,
        user_id=current_user.id
    )
    session.add(recommendation)
    session.commit()
    session.refresh(recommendation)
    return recommendation


@router.get('/recommendations/{recommendation_id}',
            response_model=RecommendationRead)
async def get_recommendation(recommendation_id: Annotated[int, Path()],
                             session: Annotated[Session, Depends(get_session)]):
    recommendation = get_recommendation_by_id(session=session,
                                              recommendation_id=recommendation_id)
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation with id {recommendation_id} was not found"
        )
    return recommendation


@router.delete('/recommendations/{recommendation_id}',
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_recommendation(recommendation_id: Annotated[int, Path()],
                                session: Annotated[Session, Depends(get_session)],
                                current_user: Annotated[User, Depends(get_current_user)]):
    recommendation = get_recommendation_by_id(session=session,
                                              recommendation_id=recommendation_id)
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation with id {recommendation_id} was not found"
        )
    if recommendation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You have not permission to delete this recommendation"
        )
    session.delete(recommendation)
    session.commit()
