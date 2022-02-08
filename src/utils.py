import json
from typing import Dict
from src.main import db
from src.model import IntegrationEvent, IntegrationForm
from src.pydantic_models import Status


def redis_event_push(
    action: str,
    data: Dict,
    form_id,
    integration_id: int,
    db_session,
    row_id: int = None,
):

    ie = IntegrationEvent(
        form_id=form_id,
        action=action,
        data=data,
        row_id=row_id,
        integration_id=integration_id,
    )
    db_session.add(ie)
    db_session.flush()
    db.publish("action", json.dumps({"message": data, "data": data, "event_id": ie.id}))
    db_session.commit()


def trigger_event(
    data: Dict,
    form_id,
    db_session,
    row_id: int = None,
):
    integ = (
        db_session.query(IntegrationForm)
        .filter(
            IntegrationForm.form_id == form_id, IntegrationForm.status == Status.active
        )
        .all()
    )
    for integration in integ:
        redis_event_push(
            integration.action,
            data,
            form_id,
            integration.integration_id,
            db_session,
            row_id,
        )
