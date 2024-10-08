from fastapi import APIRouter, Depends, HTTPException, Response, Request
from starlette.responses import JSONResponse
from src.users import *
from src.models import Company
from fastapi import APIRouter, Depends, HTTPException
from src.users import fastapi_users
from src.users import *
from sqlalchemy.exc import SQLAlchemyError
from src.models import User, Employee
from starlette import status
from src.users import current_active_user ,current_superuser
from src.schemas import CompanyCreate, CompanyRead, CompanyUpdate
from src.db import AsyncSession, get_async_session
from sqlalchemy import select, update
from starlette import status
from fastapi_cache.decorator import cache as cache_decorator
from fastapi_redis_cache import cache_one_minute
from src.custom_responses import CustomizedORJSONResponse, ROUTER_API_RESPONSES_OPEN_API


current_user = fastapi_users.current_user(active=True)

company_router = APIRouter(prefix="/company",
    responses=ROUTER_API_RESPONSES_OPEN_API
)




@company_router.post("/add",response_class=CustomizedORJSONResponse)
async def create_company(
    company: CompanyCreate,
    user: User = Depends(current_active_user), # T E M P O R A R Y implementation are current_userlater it should do superuser
    # user: User = Depends(current_active_user)     
    session: AsyncSession = Depends(get_async_session),
    ):
    """
    ### Async method that creates Company item:\n
    Company - are created by registred ***user***, user who creates company is superuser and admin for particular company  .\n
    Args:\n
        user - Depends(current_active_user).\n
        session - (AsyncSession) Depends(get_async_session).\n
        company - CompanyCreate schema\n
    #### *Only director my change Company data.
    ##### Please read schema for understanding JSON schema
    """
    try:
        if company: # temporary check
            new_company = Company(
                name = company.name,
                director = user.id,
                phone = company.phone,
                email = company.email,
                address = company.address,
                location = company.location,
                info = company.info,
                type = company.type,
                name_legal = company.name_legal,
                INN = company.INN,
                KPP = company.KPP,
                OGRN = company.OGRN,
                OKPO = company.OKPO,                                        # NO SOLVED PUT DATA
                BIK = company.BIK,
                bank_name = company.bank_name,
                bank_address= company.bank_address,
                corr_account = company.corr_account,   
            )
            session.add(new_company)
            await session.commit()
        return new_company
    except SQLAlchemyError as e:
        return e    




@company_router.put("/update/{company_id}")
async def update_company(
    company_id: int,
    company: CompanyUpdate,
    user: User = Depends(current_active_user), 
    # user: User = Depends(current_superuser)
    session: AsyncSession = Depends(get_async_session),
    ):
    """
   ### Async method that updates/patches Company item :\n
    Company - are created by registred ***user***, user who creates company is superuser and admin for particular company  .\n
    Args:\n
        user - Depends(current_superuser).\n
        session - (AsyncSession) Depends(get_async_session).\n
        company - CompanyCreate schema\n
    #### *Only director my change Compay data.  
    ##### Please read schema for understanding JSON schema
    """
    try:
        if user:


            statement = update(
            Company).where(
                Company.id == company_id).values(
                    name = company.name,
                    director = user.id,
                    phone = company.phone,
                    email = company.email,
                    address = company.address,
                    location = company.location,
                    info = company.info,
                    type = company.type,
                    name_legal = company.name_legal,
                    INN = company.INN,
                    KPP = company.KPP,
                    OGRN = company.OGRN,
                    OKPO = company.OKPO,                                                                                # Temporary how
                    BIK = company.BIK,
                    bank_name = company.bank_name,
                    bank_address= company.bank_address,
                    corr_account = company.corr_account,
                )
            await session.execute(statement)
            await session.commit()
            return CustomizedORJSONResponse(content={"detail":"created"},status_code=status.HTTP_201_CREATED,background=None)
    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        raise CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e._message)},background=None)
    # return Response(status_code=201)



# DELETE COMPANY

@company_router.delete("/delete/{company_id}")
async def delete_company(
    company_id: int,
    user: User = Depends(current_active_user), # T E M P O R A R Y - only superuser may update Employee
    # user: User = Depends(current_superuser)
    session: AsyncSession = Depends(get_async_session),
    ):
    """
   ### Async method that deletes Company item :\n
    Company - are created by registred ***user***, user who creates company is superuser and admin for particular company  .\n
    Args:\n
        user - Depends(current_superuser).\n
        session - (AsyncSession) Depends(get_async_session).\n
        company - Company ORM\n
    #### *Only director my change Compay data.  
    ##### Please read schema for understanding JSON schema
    """
    try:
        if user and company_id:
            del_company = await session.get(Company, company_id)
            if del_company:
                await session.delete(del_company)
                await session.commit()
            elif not del_company:
                return CustomizedORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"detail":"not found"},background=None) # Logger binding with background param
            return CustomizedORJSONResponse(status_code=status.HTTP_201_CREATED,content={"detail":"created"})            
    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        raise CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e._message)})
    


@company_router.get("/get/{company_id}") #,response_model=CompanyRead)
async def get_company_id(
    company_id: int,
    user: User = Depends(current_active_user), # T E M P O R A R Y - only superuser may update Employee
    # user: User = Depends(current_superuser)
    session: AsyncSession = Depends(get_async_session),
    ):
    """
   ### Async method that gets Company item by id :\n
    Company - are created by registred ***user***, user who creates company is superuser and admin for particular company  .\n
    Args:\n
        user - Depends(current_superuser).\n
        session - (AsyncSession) Depends(get_async_session).\n
        company - Company ORM\n
    #### *Only director my change Compay data.  
    ##### Please read schema for understanding JSON schema
    """
    try:
        if user and company_id:
            company = await session.get(Company, company_id)
            if company:
                return CustomizedORJSONResponse(status_code=status.HTTP_200_OK,content={"detail":company},background=None)
    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        raise CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e._message)},background=None)


# Response.background = logger




