from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import date

from backend.services.energy_service import EnergyService
from backend.repositories.energy_repository import EnergyRepository
from backend.models.schemas import DailyEnergy, Metrics, Health

router = APIRouter()


def get_service():
    repo = EnergyRepository()
    return EnergyService(repo)


@router.get("/health", response_model=Health)
def health():
    return {"status": "ok"}


@router.get("/energy/daily", response_model=list[DailyEnergy])
def daily(
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    service: EnergyService = Depends(get_service)
):
    if start and end and start > end:
        raise HTTPException(status_code=400, detail="start must be <= end")
    return service.get_daily_energy(start, end)


@router.get("/energy/metrics", response_model=Metrics)
def metrics(service: EnergyService = Depends(get_service)):
    data = service.get_metrics()
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    return data


@router.get("/energy/anomalies", response_model=list[DailyEnergy])
def anomaöies(
    methond: str = Query(default="threshold"),
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
):
    if start and end and start > end:
        raise HTTPException(status_code=400, detail="start must be <= end")
    return service.detect_anomalies(methond, start, end)
