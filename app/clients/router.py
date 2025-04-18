"""
Router module for client-related endpoints.
Handles all HTTP requests for client operations including create, read, update, and delete.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from app.auth.router import get_current_user, get_admin_user
from app.models import User, UserRole
from app.clients.service.logic import interpret_and_calculate, MODEL
from app.clients.schema import PredictionInput

from app.database import get_db
from app.clients.service.client_service import ClientService
from app.clients.schema import (
    ClientResponse,
    ClientUpdate,
    ClientListResponse,
    ServiceResponse,
    ServiceUpdate
)

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/predictions")
async def predict(data: PredictionInput):
    return interpret_and_calculate(data.model_dump())


@router.get("/", response_model=ClientListResponse)
async def get_clients(
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=50, ge=1, le=150, description="Maximum number of records to return"),
        _: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return ClientService.get_clients(db, skip, limit)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
        client_id: int,
        _: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Get a specific client by ID"""
    return ClientService.get_client(db, client_id)


@router.get("/search/by-criteria", response_model=List[ClientResponse])
async def get_clients_by_criteria(
    employment_status: Optional[bool] = None,
    education_level: Optional[int] = Query(None, ge=1, le=14),
    age_min: Optional[int] = Query(None, ge=18),
    gender: Optional[int] = Query(None, ge=1, le=2),
    work_experience: Optional[int] = Query(None, ge=0),
    canada_workex: Optional[int] = Query(None, ge=0),
    dep_num: Optional[int] = Query(None, ge=0),
    canada_born: Optional[bool] = None,
    citizen_status: Optional[bool] = None,
    fluent_english: Optional[bool] = None,
    reading_english_scale: Optional[int] = Query(None, ge=0, le=10),
    speaking_english_scale: Optional[int] = Query(None, ge=0, le=10),
    writing_english_scale: Optional[int] = Query(None, ge=0, le=10),
    numeracy_scale: Optional[int] = Query(None, ge=0, le=10),
    computer_scale: Optional[int] = Query(None, ge=0, le=10),
    transportation_bool: Optional[bool] = None,
    caregiver_bool: Optional[bool] = None,
    housing: Optional[int] = Query(None, ge=1, le=10),
    income_source: Optional[int] = Query(None, ge=1, le=11),
    felony_bool: Optional[bool] = None,
    attending_school: Optional[bool] = None,
    substance_use: Optional[bool] = None,
    time_unemployed: Optional[int] = Query(None, ge=0),
    need_mental_health_support_bool: Optional[bool] = None,
    _: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Search clients by any combination of criteria"""
    return ClientService.get_clients_by_criteria(
        db,
        employment_status=employment_status,
        education_level=education_level,
        age_min=age_min,
        gender=gender,
        work_experience=work_experience,
        canada_workex=canada_workex,
        dep_num=dep_num,
        canada_born=canada_born,
        citizen_status=citizen_status,
        fluent_english=fluent_english,
        reading_english_scale=reading_english_scale,
        speaking_english_scale=speaking_english_scale,
        writing_english_scale=writing_english_scale,
        numeracy_scale=numeracy_scale,
        computer_scale=computer_scale,
        transportation_bool=transportation_bool,
        caregiver_bool=caregiver_bool,
        housing=housing,
        income_source=income_source,
        felony_bool=felony_bool,
        attending_school=attending_school,
        substance_use=substance_use,
        time_unemployed=time_unemployed,
        need_mental_health_support_bool=need_mental_health_support_bool
    )


@router.get("/search/by-services", response_model=List[ClientResponse])
async def get_clients_by_services(
        employment_assistance: Optional[bool] = None,
        life_stabilization: Optional[bool] = None,
        retention_services: Optional[bool] = None,
        specialized_services: Optional[bool] = None,
        employment_related_financial_supports: Optional[bool] = None,
        employer_financial_supports: Optional[bool] = None,
        enhanced_referrals: Optional[bool] = None,
        _: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Get clients filtered by multiple service statuses"""
    return ClientService.get_clients_by_services(
        db,
        employment_assistance=employment_assistance,
        life_stabilization=life_stabilization,
        retention_services=retention_services,
        specialized_services=specialized_services,
        employment_related_financial_supports=employment_related_financial_supports,
        employer_financial_supports=employer_financial_supports,
        enhanced_referrals=enhanced_referrals
    )


@router.get("/{client_id}/services", response_model=List[ServiceResponse])
async def get_client_services(
        client_id: int,
        _: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Get all services and their status for a specific client, including case worker info"""
    return ClientService.get_client_services(db, client_id)


@router.get("/search/success-rate", response_model=List[ClientResponse])
async def get_clients_by_success_rate(
        min_rate: int = Query(70, ge=0, le=100, description="Minimum success rate percentage"),
        _: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Get clients with success rate above specified threshold"""
    return ClientService.get_clients_by_success_rate(db, min_rate)


@router.get("/case-worker/{case_worker_id}", response_model=List[ClientResponse])
async def get_clients_by_case_worker(
        case_worker_id: int,
        _: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return ClientService.get_clients_by_case_worker(db, case_worker_id)


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
        client_id: int,
        client_data: ClientUpdate,
        _: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Update a client's information"""
    return ClientService.update_client(db, client_id, client_data)


@router.put("/{client_id}/services/{user_id}", response_model=ServiceResponse)
async def update_client_services(
        client_id: int,
        user_id: int,
        service_update: ServiceUpdate,
        _: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return ClientService.update_client_services(db, client_id, user_id, service_update)


@router.post("/{client_id}/case-assignment", response_model=ServiceResponse)
async def create_case_assignment(
        client_id: int,
        case_worker_id: int = Query(..., description="Case worker ID to assign"),
        _: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Create a new case assignment for a client with a case worker"""
    return ClientService.create_case_assignment(db, client_id, case_worker_id)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
        client_id: int,
        _: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Delete a client"""
    ClientService.delete_client(db, client_id)
    return None


@router.get("/models/current", response_model=Dict[str, str])
async def get_current_model():
    """Get the name and type of the currently active model."""
    from app.clients.service import logic
    model_type = type(logic.MODEL).__name__
    model_type_to_name = {
        "RandomForestRegressor": "random_forest",
        "LinearRegression": "linear_regression",
        "GradientBoostingRegressor": "gradient_boost"
    }
    model_name = model_type_to_name.get(model_type, model_type.lower())
    return {
        "name": model_name,
        "type": model_type
    }


@router.get("/models/available", response_model=List[Dict[str, str]])
async def get_available_models():
    """Get list of available models with their types."""
    available_models = [
        {
            "name": "random_forest",
            "type": "RandomForestRegressor"
        },
        {
            "name": "linear_regression",
            "type": "LinearRegression"
        },
        {
            "name": "gradient_boost",
            "type": "GradientBoostingRegressor"
        }
    ]
    return available_models

@router.put("/models/current/{model_name}", response_model=Dict[str, str])
async def set_current_model(model_name: str):
    """Set the current model to use."""
    import logging
    logger = logging.getLogger("uvicorn")

    # Get available models
    logger.info(f"Attempting to switch to model: {model_name}")
    available_models = await get_available_models()
    model_names = [model["name"] for model in available_models]
    logger.info(f"Available models: {model_names}")

    # Validate model name
    if model_name not in model_names:
        logger.error(f"Model '{model_name}' not found in available models")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Model '{model_name}' not found. Available models: {model_names}"
        )

    try:
        # Check current model type
        from app.clients.service import logic
        current_model_type = type(logic.MODEL).__name__
        logger.info(f"Current model type: {current_model_type}")

        # Get the expected model type for the requested model
        model_type = next((model["type"] for model in available_models if model["name"] == model_name), None)
        if not model_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model type not found for model '{model_name}'"
            )

        # If the current model is already the requested type, return early
        if current_model_type == model_type:
            return {
                "name": model_name,
                "type": current_model_type
            }

        # Build model path
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'service', f'{model_name}.pkl')
        logger.info(f"Looking for model at: {model_path}")

        # Check if file exists
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at: {model_path}")
            # Try to list files in directory
            service_dir = os.path.join(current_dir, 'service')
            if os.path.exists(service_dir):
                files = os.listdir(service_dir)
                logger.info(f"Files in service directory: {files}")

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model file '{model_name}.pkl' not found"
            )

        # Load model
        import pickle
        logger.info(f"Loading model from: {model_path}")
        with open(model_path, "rb") as model_file:
            new_model = pickle.load(model_file)

        logger.info(f"Loaded model type: {type(new_model).__name__}")

        # Update the MODEL variable
        logic.MODEL = new_model
        logger.info("Model successfully updated")

        return {
            "name": model_name,
            "type": type(new_model).__name__
        }
    except Exception as e:
        import traceback
        logger.error(f"Error setting model: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error setting model: {str(e)}"
        ) from e
