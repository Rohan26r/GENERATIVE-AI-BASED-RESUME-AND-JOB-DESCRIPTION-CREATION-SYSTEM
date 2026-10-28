"""
Firebase service — initializes Admin SDK for Firestore only (free tier).
Storage is handled locally on disk — no Firebase Storage costs.
"""

import os
import logging
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore

logger = logging.getLogger("services.firebase")

_app: firebase_admin.App | None = None


def _init_app() -> firebase_admin.App:
    global _app
    if _app:
        return _app

    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

    if cred_path:
        cred = credentials.Certificate(cred_path)
    else:
        # Application Default Credentials (Cloud Run / GCP)
        cred = credentials.ApplicationDefault()

    _app = firebase_admin.initialize_app(cred)
    logger.info("Firebase Admin SDK initialized (Firestore only).")
    return _app


@lru_cache(maxsize=1)
def get_firestore():
    _init_app()
    return firestore.client()
