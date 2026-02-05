"""
Authentication controller for login and registration endpoints.
"""
import logging
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.client import ClientModel
from schemas.auth_schema import LoginRequest, RegisterRequest, AuthResponse, RegisterResponse
from utils.auth_utils import hash_password, verify_password

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user with email and password.
    
    Args:
        request: Login credentials (email, password)
        db: Database session
        
    Returns:
        AuthResponse with user data if successful
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Buscar cliente por email
    client = db.query(ClientModel).filter(
        ClientModel.email == request.email
    ).first()
    
    if not client:
        logger.warning(f"Login fallido - email no encontrado: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Verificar contraseña
    if not client.password or not verify_password(request.password, client.password):
        logger.warning(f"Login fallido - contraseña incorrecta: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    logger.info(f"Login exitoso: {request.email}")
    
    return AuthResponse(
        id=client.id_key,
        name=client.name,
        lastname=client.lastname,
        email=client.email,
        telephone=client.telephone,
        is_admin=client.is_admin or False,
        message="Inicio de sesión exitoso"
    )


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        request: Registration data (name, lastname, email, password)
        db: Database session
        
    Returns:
        RegisterResponse with new user data
        
    Raises:
        HTTPException: 400 if email already exists
    """
    # Verificar si el email ya existe
    existing = db.query(ClientModel).filter(
        ClientModel.email == request.email
    ).first()
    
    if existing:
        logger.warning(f"Registro fallido - email ya existe: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email ya está registrado"
        )
    
    # Determinar si es admin (email contiene "admin")
    is_admin = "admin" in request.email.lower()
    
    # Crear nuevo cliente
    new_client = ClientModel(
        name=request.name,
        lastname=request.lastname,
        email=request.email,
        password=hash_password(request.password),
        telephone=request.telephone,
        is_admin=is_admin
    )
    
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    logger.info(f"Usuario registrado: {request.email} (admin={is_admin})")
    
    return RegisterResponse(
        id=new_client.id_key,
        name=new_client.name,
        lastname=new_client.lastname,
        email=new_client.email,
        is_admin=new_client.is_admin,
        message="Usuario registrado exitosamente"
    )

