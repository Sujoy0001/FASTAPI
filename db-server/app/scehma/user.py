from pydentic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: int = Field(..., description="The unique identifier for the user")
    name: str = Field(..., description="The name of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    is_active: bool = Field(default=True, description="Indicates if the user is active")
    
class UserCreate(BaseModel):
    name: str = Field(..., description="The name of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., description="The password for the user account")
    
class UserUpdate(BaseModel):
    
    name: str = Field(None, description="The name of the user")
    email: EmailStr = Field(None, description="The email address of the user")
    password: str = Field(None, description="The password for the user account")
    is_active: bool = Field(None, description="Indicates if the user is active")
    
class UserInDB(User):
    hashed_password: str = Field(..., description="The hashed password for the user account")
    
class UserOut(BaseModel):
    id: int = Field(..., description="The unique identifier for the user")
    name: str = Field(..., description="The name of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    is_active: bool = Field(..., description="Indicates if the user is active")