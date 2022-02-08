import logging
from fastapi import Depends, FastAPI


from sqlalchemy.orm import Session

from src.model import (
    FormData,
    FormDefinition,
    Forms,
    Integration,
    IntegrationEvent,
    IntegrationForm,
    get_db,
)
from src.pydantic_models import (
    FormDataNew,
    FormDefinitionNew,
    FormNew,
    IntegrationNew,
    PublishedStatus,
    Status,
)
import redis


app = FastAPI()

log = logging.getLogger(__name__)
REDIS_DATABASE_URL = "0.0.0.0"

db = redis.StrictRedis(host=REDIS_DATABASE_URL)


@app.get("/test")
async def test():
    return {
        "result": "success",
        "message": "It works!",
    }


@app.post("/add_form")
async def add_form(form: FormNew, db: Session = Depends(get_db)):
    formNew = Forms(name=form.name, published=form.published)

    db.add(formNew)
    db.commit()
    return {
        "result": "success",
        "message": "Form Created!",
    }


@app.post("/publish_form")
async def publish_form(form_id: int, db: Session = Depends(get_db)):
    form = (
        db.query(Forms)
        .filter(Forms.id == form_id, Forms.status == Status.active)
        .one_or_none()
    )
    if not form:
        return {"result": "error", "message": "Form not found!", "data": {}}
    form.published = PublishedStatus.published
    db.commit()
    return {"result": "success", "message": "Form published!", "data": form}


@app.post("/unpublish_form")
async def unpublish_form(form_id: int, db: Session = Depends(get_db)):
    form = (
        db.query(Forms)
        .filter(Forms.id == form_id, Forms.status == Status.active)
        .one_or_none()
    )
    if not form:
        return {"result": "error", "message": "Form not found!", "data": {}}
    form.published = PublishedStatus.unpublished
    db.commit()
    return {"result": "success", "message": "Form unpublished!", "data": form}


@app.get("/get_form")
async def get_form(form_id: int, db: Session = Depends(get_db)):
    form = (
        db.query(Forms)
        .filter(Forms.id == form_id, Forms.status == Status.active)
        .one_or_none()
    )
    if not form:
        return {"result": "error", "message": "Form not found!", "data": {}}

    return {"result": "success", "message": "Form found!", "data": form}


@app.post("/add_question")
async def add_question(
    form_id: int, formData: FormDefinitionNew, db: Session = Depends(get_db)
):
    form = (
        db.query(Forms)
        .filter(Forms.id == form_id, Forms.status == Status.active)
        .one_or_none()
    )
    if not form:
        return {"result": "error", "message": "form not found!", "data": {}}
    formDefinition = FormDefinition(
        question=formData.question,
        type=formData.type,
        published=formData.published,
        form_id=form.id,
    )
    return {
        "result": "success",
        "message": "question added!",
    }


@app.post("/fill_form")
async def fill_form(
    form_id: int, question: int, formData: FormDataNew, db: Session = Depends(get_db)
):
    form = (
        db.query(Forms)
        .filter(
            Forms.id == form_id,
            Forms.status == Status.active,
            Forms.published == PublishedStatus.published,
        )
        .one_or_none()
    )
    if not form:
        return {
            "result": "error",
            "message": "form not found or not published!",
            "data": {},
        }
    ques = (
        db.query(FormDefinition)
        .filter(
            FormDefinition.id == form_id,
            FormDefinition.status == Status.active,
            FormDefinition.published == PublishedStatus.published,
        )
        .one_or_none()
    )
    if not ques:
        return {"result": "error", "message": "question not found!", "data": {}}
    formdata = FormData(
        form_definition_id=question,
        form_id=form.id,
        data=formData.data,
    )
    from src.utils import trigger_event

    trigger_event(data=formData.dict(), form_id=form.id, db_session=db)
    return {
        "result": "success",
        "message": "question filled!",
    }


@app.post("/add_integration")
async def add_integration(integration: IntegrationNew, db: Session = Depends(get_db)):
    integrationNew = Integration(name=integration.name, action=integration.action)

    db.add(integrationNew)
    db.commit()
    return {
        "result": "success",
        "message": "Integration Created!",
    }


@app.post("/apply_integration")
async def apply_integration(
    integration: int, form_id: int, db: Session = Depends(get_db)
):
    form = (
        db.query(Forms)
        .filter(Forms.id == form_id, Forms.status == Status.active)
        .one_or_none()
    )
    if not form:
        return {"result": "error", "message": "form not found!", "data": {}}
    integ = (
        db.query(Integration)
        .filter(Integration.id == integration, Integration.status == Status.active)
        .one_or_none()
    )
    if not integ:
        return {"result": "error", "message": "form not found!", "data": {}}
    integrationNew = IntegrationForm(integration_id=integ.id, form_id=form.id)
    db.add(integrationNew)
    db.commit()
    return {
        "result": "success",
        "message": "Integration Created!",
    }


@app.post("/callback")
async def callback(ie: int, status: str, db: Session = Depends(get_db)):
    event = (
        db.query(IntegrationEvent)
        .filter(IntegrationEvent.id == ie, IntegrationEvent.action_status == "pending")
        .one_or_none()
    )
    if not event:
        return {
            "result": "error",
            "message": "event not found or status changed!",
            "data": {},
        }
    event.published = status
    db.commit()
    return {"result": "success", "message": "event updated!", "data": {}}
