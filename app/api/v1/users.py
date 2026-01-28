from fastapi import APIRouter, Depends, status, Response 
from sqlalchemy.orm import Session
from datetime import datetime, timedelta 

from app.db.session import get_db
from app.models import User, OTP
from app.schemas import UserSchema 
from utils.code import generate_code

user_router = APIRouter()

@user_router.get('/check-user/{check_user}')
async def check_user(chat_id: str, db:Session = Depends(get_db)):
	user = db.query(User).filter(User.chat_id == chat_id).first()

	if user is not None:
		return User
	
	data = {
		"status": False, 
		"message": "User not found."
	}

	return Response(content=data, status_code=status.HTTP_404_NOT_FOUND)


@user_router.post('/register')
async def register_user(user: UserSchema, db:Session = Depends(get_db)):

	user_db = User(
		first_name = user.first_name, 
		last_name =  user.last_name, 
		username =  user.username, 
		chat_id =  user.chat_id, 
 		phone_number  =  user.phone_number, 
		)
	
	db.add(user_db) 
	db.commit()
	db.refresh(user_db)
	
	while db.query(OTP).filter(OTP.code == code).first():
		code = generate_code() 


	otp = OTP(
		user_id = user_db.id, 
		code  = code, 
		expire_at  = datetime.utcnow() + timedelta(minutes=2), 
		is_active = True
	)

	data = {
		"status": False, 
		"message": "User not found."
	}

	return Response(content=data, status_code=status.HTTP_404_NOT_FOUND)