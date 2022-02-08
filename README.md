# Daisy

## How to run server

I have the images tagged to my local registry so run a local registry as shown below. In case you don't want to run your own registry do change the image name to a non registry tag.

`docker run -d -p 5000:5000 --name registry registry:2`

## To run the server

```
docker-compose build
docker-compose push
docker-compose up
```

## First Time setup

After first `docker-compose up` create database atlan and run `alembic upgrade head`

Docs at localhost:8000/docs

## Design Specification

The project is designed as a central api service used to create forms, add questions and add the appropriate responses. There are is no auth, users or organization considerations.
There are separate services that talk to the central api service through a pusub mechanism. The pubsub mechanism used here is redis pubsub. The individual script can be made into
microservice that can be plugged in through the integrations table which needs the pubsub channel and the data that needs to be passed through.
The pubsub works through a series of well placed triggers at specific action points that might lead to integrations. The trigger_event method figures out all the available integrations
available for the form and then calls them. This trigger_method should essentially be called asynchronously through queue workers such as celery or redis-queues.
All the triggers are logged in the IntegrationEvents table. The status column tracks the status of the event triggered and whether the microservice has completed the action.
The microservice essentially gives a call back on successful completion or marks it as completed.
Benchmarking of the same can be performed through locust , monitoring and alerts through sentry/new relic. A huge chuck of system failures can be mitigated through a well done orchestration engine or the cloud provider tooling.
There would be API level limitations from third party services such as rate limiting etc which can be mitigated through buying out a higher thruput from the vendor or doing batch dumps to the service.
