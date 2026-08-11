# Ez a fájl köti össze a rétegeket: HTTP végpontok (route-ok)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import models, schemas, crud
from app.seed import seed_ha_ures

