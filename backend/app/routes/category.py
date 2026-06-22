from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.category_schema import CategoryCreate
from app.models.category import Category

router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)

@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Category).filter(
        Category.category_name == category.category_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = Category(
        category_name=category.category_name,
        description=category.description
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {
        "message": "Category created",
        "category_id": new_category.category_id
    }

@router.get("/")
def get_categories(
    db: Session = Depends(get_db)
):
    return db.query(Category).all()