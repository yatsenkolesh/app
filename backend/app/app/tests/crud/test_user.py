from sqlalchemy.orm import Session  # type: ignore
import pytest  # type: ignore
from app import crud
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    assert user["email"] == email  # type: ignore
    assert "hashed_password" in user  # type: ignore


@pytest.mark.asyncio
async def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    authenticated_user = await crud.user.authenticate(
        db, email=email, password=password
    )
    assert authenticated_user
    assert user["email"] == authenticated_user["email"]  # type: ignore


@pytest.mark.asyncio
async def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = "wrong password"
    user = await crud.user.authenticate(db, email=email, password=password)
    assert user is None


@pytest.mark.asyncio
async def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    is_active = crud.user.is_active(user)
    assert is_active is True


@pytest.mark.asyncio
async def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, disabled=True)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    is_active = crud.user.is_active(user)
    assert is_active


@pytest.mark.asyncio
async def test_check_if_user_is_superuser(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


@pytest.mark.asyncio
async def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


@pytest.mark.asyncio
async def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    user_2 = await crud.user.get(db, id=user["_id"])  # type: ignore
    assert user_2
    assert user["email"] == user_2["email"]
    # assert jsonable_encoder(user) == jsonable_encoder(user_2)


@pytest.mark.asyncio
async def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = await crud.user.create(db, obj_in=user_in)  # type: ignore
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    await crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = await crud.user.get(db, id=user["_id"])  # type: ignore
    assert user_2
    assert user["email"] == user_2["email"]
    # assert verify_password(new_password, user_2["hashed_password"])


# @pytest.mark.asyncio
# async def notest_get_multi(db: Session) -> None:
#     users = await crud.user.get_multi(db=db)  # type: ignore
#     assert len(users) > 0
