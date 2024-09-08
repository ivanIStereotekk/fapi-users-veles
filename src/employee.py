
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.responses import JSONResponse
from src.users import *
from sqlalchemy.exc import SQLAlchemyError
from src.models import User, Employee
from starlette import status
from src.users import current_active_user,current_superuser
from src.db import AsyncSession, get_async_session
from src.schemas import EmployeeRead, EmployeeUpdate,EmployeeCreate
from sqlalchemy import select, update
from starlette import status
from src.custom_responses import *


employee_router = APIRouter(
    prefix="/employee",
    responses=ROUTER_API_RESPONSES_OPEN_API,
)

@employee_router.post("/add",response_class=CustomizedORJSONResponse)
async def create_employee(
    employee: EmployeeCreate,
    user: User = Depends(current_active_user), # T E M P O R A R Y implementation are current_userlater it should do superuser
    # user: User = Depends(current_superuser)     
    session: AsyncSession = Depends(get_async_session),
    ):
    """
    ### Async method that creates Employee item:\n
    Employee are linked with User by ForeinKey parameter so it extends
    basic User Model and gives additional fields to User during it's work on a position.\n
    Args:\n
        user - Depends(current_superuser).\n
        * only superuser may create employee
        session - (AsyncSession) Depends(get_async_session).\n
        employee - Employee schema\n  
    ##### Please read schema for understanding JSON schema
    """
    try:
        if isinstance(employee.position,str): # temporary checker
            new_employee = Employee(
            user_id=employee.user_id,
            position=employee.position,
            obligations=employee.obligations,
            company_id=employee.company_id,
            )
            session.add(new_employee)
            await session.commit()
            return {"detail": "created"}
    except SQLAlchemyError as e:
        return CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

        



@employee_router.put("/update/{user_id}",response_class=CustomizedORJSONResponse)
async def update_employee(
    user_id: int,
    employee: EmployeeUpdate,
    user: User = Depends(current_active_user), # T E M P O R A R Y - only superuser may update Employee
    # user: User = Depends(current_superuser)
    session: AsyncSession = Depends(get_async_session),
    ):
    """
   ### Async method that updates/patches Employee item :\n
    Employee are linked with User by ForeinKey parameter so extends
    basic User Model and gives additional fields to User.\n
    Args:\n
        user_id: int of linked User that you want to update.\n
        session - (AsyncSession) Depends(get_async_session).\n
        employee - EmployeeUpdate schema\n
    #### *Only superuser my change and create Employee    
    ##### Please read schema for understanding JSON schema
    """
    try:
        if user:
            statement = update(
            Employee).where(
                Employee.user_id == user_id).values(
                    user_id=employee.user_id,
                    position=employee.position,
                    obligations=employee.obligations,
                    company_id=employee.company_id,
                )
            await session.execute(statement)
            await session.commit()
            return CustomizedORJSONResponse(content={"detail":"updated"},status_code=status.HTTP_201_CREATED)
    except SQLAlchemyError as e:  
        # <<< logging here
        return CustomizedORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"detail":str(e)})                          # <<<< later will do e  to logger
    #     raise HTTPException(status_code=404,detail=status.HTTP_404_NOT_FOUND)
    # return CreatedJSONResponse





@employee_router.get("/get/{user_id}",response_model=EmployeeRead,response_class=CustomizedORJSONResponse)
async def get_employee_id(
    user_id: int,
    user: User = Depends(current_active_user),
    # user: User = Depends(current_superuser)
    session: AsyncSession = Depends(get_async_session)
    ):
    """
   ### Async method that retrieves Employee by user_id int param :\n
    Employee are linked with User by ForeinKey parameter so extends
    basic User Model and gives additional fields to User.\n
    Args:\n
        user_id: int of linked User that you want to retrieve.\n
        session - (AsyncSession) Depends(get_async_session).\n
        employee - EmployeeUpdate schema\n
    ##### Please read schema for understanding JSON schema
    """
    if user_id:
        try:
            statement = select(Employee).where(Employee.user_id == user_id)
            result = await session.execute(statement=statement)
            retrieved = result.scalar_one_or_none() # retrieved employee item
            if retrieved is not None:
                return retrieved # Here is pure scalar object that parses response_model=EmployeeRead
            else:
                return CustomizedORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"detail":"item not found"})
            
        except SQLAlchemyError as e:                                            # <<<< later will do e  to logger
            raise CustomizedORJSONResponse(status_code=404,detail=status.HTTP_404_NOT_FOUND)


##### HERE





@employee_router.delete(
        "/delete/{employee_id}",
        summary="Summary Of Employee",
        response_class=CustomizedORJSONResponse,
        )
async def delete_employee(
    employee_id: int,
    user: User = Depends(current_active_user), # T E M P O R A R Y - only superuser may update Employee
    # user: User = Depends(current_superuser)
    session: AsyncSession = Depends(get_async_session),
    ):
    """
   ### Async method that deletes Employee item :\n
    Employee - are created by registred ***user***.\n
    Args:\n
        user - Depends(current_superuser).\n
        session - (AsyncSession) Depends(get_async_session).\n
        employee_id - Employee ORM\n 
    ##### Please read schema for understanding JSON schema
    """
    try:
        if user and employee_id:
            del_employee = await session.get(Employee, employee_id)
            if del_employee and del_employee.id == employee_id:
                await session.delete(del_employee)
                await session.commit()
                return CustomizedORJSONResponse(status_code=status.HTTP_202_ACCEPTED,content={"detail":"deleted"})
            else:
                return CustomizedORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"detail":"not found"})

    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        return CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e)})



from fastapi.responses import RedirectResponse, Response
@employee_router.get('/redirect')
async def redirect(response: Response):
    response.init_headers
    return RedirectResponse("http://127.0.0.1:8000/docs",headers={"WWW-Authenticate": "Bearer"})