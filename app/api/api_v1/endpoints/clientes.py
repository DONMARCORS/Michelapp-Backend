# WARNING: This is not authentication, 
# this is for admin/vendor functionalities like 
# searching clients, or displaying clients in a table.


from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import random as rd
import string

from app import crud
from app.api import deps
from app import schemas
from app.schemas.user import (
    User,
    UserSearchResults,
    UserCreate
)

from sqlalchemy.orm import Session

router = APIRouter()

logger = logging.getLogger(__name__)

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )


@router.get("/", status_code=200, response_model=UserSearchResults)
def get_clientes(
    *,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Get all clients
    """

    results = crud.user.get_multi(db=db)
    if not results:
        return {"results": []}
    
    logger.debug(results[0].id)

    list_results = []
    for r in list(results):
        if r.privilege == 3:
            list_results.append(r)

    return {"results": list_results}


# Caso de uso: Crear un cliente
@router.post("/", status_code=201, response_model=schemas.User, response_description="Client created")
def create_cliente(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate = Body(
        ...,
        example={
            "first_name": "Israel",
            "last_name": "Hernandez",
            "email": "hdisra@gmail.com",
            "birthday": "2023-05-15",
            "privilege": 3,
            "password": ""
        }
    ),

) -> User:
    """
    Create a client
    """

    logger.info("Creating user")
    client = crud.user.get_by_email(db, email=user_in.email)
    if client:
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_in.privilege != 3:
        raise HTTPException(status_code=400, detail="Cannot create user with privilege other than client")
    
    # Creando password y envio a correo del cliente (GMAIL)
    email_subject = "Contraseña generada por Michelapp"
    dest_email_address = user_in.email
    sender_email_address = "hdisra@gmail.com" # Crear correo para el sistema
    email_smtp = "smtp.gmail.com"
    email_password = "hdwjasdc" # Contrasena del correo del sistema

    msg = MIMEMultipart()

    # Email headers
    msg['Subject'] = email_subject
    msg['From'] = sender_email_address
    msg['To'] = dest_email_address

    # Generando contrasena
    pwd = ""
    for c in range(0, 5):
        pwd += rd.choice(string.ascii_letters)

    print(pwd)
    '''
    message = "Hola! Tu contraseña para entrar a Michelapp será: "+pwd

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg["From"], email_password)
    server.sendmail(msg['From'], msg["To"], msg.as_string())
    server.quit()
    '''
    # Asignando contrasena al cliente
    user_in.password = pwd

    client = crud.user.create(db, obj_in=user_in)

    if client is None:
        raise HTTPException(status_code=400, detail="Client not created")
    

    return client
    




