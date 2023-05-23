# WARNING: This is not authentication, 
# this is for admin/vendor functionalities like 
# searching clients, or displaying clients in a table.


from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
import logging
import yagmail
import random as rd
import string
from app.core.security import verify_password

from app import crud
from app.api import deps
from app import schemas
from app.schemas.user import (
    User,
    UserSearchResults,
    UserUpdate
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
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Get all clients
    """

    if current_user.privilege != 1:
        raise authorization_exception


    results = crud.user.get_multi(db=db)
    if not results:
        return {"results": []}
    
    logger.debug(results[0].id)

    list_results = []
    for r in list(results):
        if r.privilege == 3:
            list_results.append(r)

    return {"results": list_results}


# Caso de uso: Crear una cuenta para el cliente
@router.post("/", status_code=201, response_model=schemas.User, response_description="Client created")
def create_cliente(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate = Body(
        ...,
        example={
            "first_name": "Israel",
            "last_name": "Hernandez",
            "email": "hdisra318@ciencias.unam.mx",
            "birthday": "2023-05-15",
            "address": "CDMX",
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
    sender_email_address = "michelappingsoft@gmail.com" # Correo para el sistema
    email_password = "Ihebd837" # Contrasena del correo del sistema
    password_aplicacion = 'eycooxfyrydhszmc' # Contrasena para el envio de correos GMAIL

    # Generando contrasena
    pwd = ""
    for c in range(0, 5):
        pwd += rd.choice(string.ascii_letters)

    yag = yagmail.SMTP(user=sender_email_address, password=password_aplicacion)

    dest_email = [user_in.email]
    titulo = '<h1>Hola! Aqui te enviamos la contraseña con la que puedes ingresar a Michelapp!</h1>'
    cuerpo = '<p>Contraseña: '+pwd+'</p>'

    yag.send(dest_email, email_subject, [titulo, cuerpo])

    # Asignando contrasena al cliente
    user_in.password = pwd

    client = crud.user.create(db, obj_in=user_in)

    if client is None:
        raise HTTPException(status_code=400, detail="Client not created")
    

    return client
    

# Caso de uso: Borrar la cuenta del cliente
@router.delete("/{client_id}/{client_pwd}", status_code=200, response_model=schemas.User, response_description="Client deleted")
def delete_client(
    *,
    client_id: int,
    client_pwd: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Delete a client. Only clients can
    """

    if current_user.privilege != 3:
        raise authorization_exception
    
    # Si el id no coincide
    if current_user.id != client_id:
        raise authorization_exception
    
    client = crud.user.get(db, id=client_id)
    
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Confirmando eliminacion con la contrasena
    if not verify_password(client_pwd, client.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    crud.user.remove(db=db, id=client_id)

    # success message
    return {"message": "Client deleted"}


# Caso de uso: Actualizar la cuenta del cliente (Contrasena)
@router.put("/password/{client_id}/{client_old_pwd}", status_code=200, response_model=schemas.User, response_description="Client's password updated")
def update_client_pwd(
    *,
    client_id: int,
    client_old_pwd: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_in: UserUpdate = Body(
        ...,
        example={
            "password": "example123"
        }
    ),
) -> dict:
    
    """
    Updates client's password
    """

    if current_user.privilege != 3:
        raise authorization_exception
    
    # Si el id no coincide
    if current_user.id != client_id:
        raise authorization_exception
    
    client = crud.user.get(db, id=client_id)

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    if not verify_password(client_old_pwd, client.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    client = crud.user.update(db, db_obj=client, obj_in=user_in)

    return client


# Caso de uso: Actualizar la cuenta del cliente (Correo o direccion)
@router.put("/email/{client_id}", status_code=200, response_model=schemas.User, response_description="Client updated")
def update_client_email_address(
    *,
    client_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_in: UserUpdate = Body(
        ...,
        example={
            "email": "",
            "address": ""
        }
    ),
) -> dict:
    
    """
    Updates client's email or client's address
    """

    if current_user.privilege != 3:
        raise authorization_exception
    
    # Si el id no coincide
    if current_user.id != client_id:
        raise authorization_exception
    
    # Checando que no se quiera actualizar otro campo
    if user_in.first_name != None or user_in.last_name != None or user_in.birthday != None or user_in.password != None or user_in.privilege != None:
        raise HTTPException(status_code=400, detail="Update not possible")

    
    client = crud.user.get(db, id=client_id)

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    client = crud.user.update(db, db_obj=client, obj_in=user_in)

    return client

