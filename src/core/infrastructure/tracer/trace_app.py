"""Tracer setup."""

import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.sdk.trace.sampling import (
    ALWAYS_OFF,
    ALWAYS_ON,
    ParentBased,
    Sampler,
    TraceIdRatioBased,
)

from src.core.configs.env import settings

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


def setup_jaeger(
    app: FastAPI,
    service_name: str = settings.trace.SERVICE_NAME_API,
    environment: str = settings.trace.MODE,
    agent_host_name: str = settings.trace.AGENT_HOSTNAME,
    agent_port: int = settings.trace.AGENT_PORT,
    service_namespace: str = settings.trace.SERVICE_NAMESPACE_APP,
    tags: Optional[Dict[str, Any]] = settings.trace.tags,
    sampling_rate: float = settings.trace.sampling_rate,
    max_queue_size: int = settings.trace.MAX_QUEUE_SIZE,
    max_export_batch_size: int = settings.trace.MAX_EXPORT_BATCH_SIZE,
    schedule_delay_millis: int = settings.trace.SCHEDULE_DELAY_MILLIS,
    debug_mode: bool = settings.trace.debug_mode,
) -> trace.Tracer:
    """Configure Jaeger tracing.

    :param app: FastAPI application.
    :param service_name: Name of Jaeger tracing service.
    :param environment: Name of Jaeger tracing environment.
    :param agent_host_name: Name of Jaeger tracing agent hostname.
    :param agent_port: Name of Jaeger tracing agent port.
    :param service_namespace: Name of Jaeger tracing service namespace.
    :param tags: Dictionary of tags.
    :param sampling_rate: Sampling rate.
    :param max_queue_size: Max queue size.
    :param max_export_batch_size: Max export batch size.
    :param schedule_delay_millis: Schedule delay milliseconds.
    :param debug_mode: Debug mode.
    :return: Jaeger tracing service
    :rtype: trace.Tracer
    """
    resource_params = {
        "service.name": service_name,
        "service.namespace": service_namespace,
        "environment": environment,
    }

    if tags:
        resource_params.update(tags)

    resource = Resource.create(resource_params)

    sampler: Sampler

    if sampling_rate == 1.0:
        sampler = ALWAYS_ON
    elif sampling_rate == 0.0:
        sampler = ALWAYS_OFF
    else:

        probability_sampler = TraceIdRatioBased(sampling_rate)
        sampler = ParentBased(root=probability_sampler)

    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    jaeger_exporter = JaegerExporter(
        agent_host_name=agent_host_name,
        agent_port=agent_port,
        udp_split_oversized_batches=True,
    )

    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            jaeger_exporter,
            max_queue_size=max_queue_size,
            max_export_batch_size=max_export_batch_size,
            schedule_delay_millis=schedule_delay_millis,
        )
    )

    if debug_mode:
        tracer_provider.add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter())
        )

    trace.set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(
        app,
        excluded_urls="health,metrics",
        tracer_provider=tracer_provider,
    )

    tracer = trace.get_tracer(__name__)

    LOGGER.info(
        f"Jaeger tracing setup for service {service_name} "
        f"in environment {environment} with sampling rate {sampling_rate}"
    )

    return tracer
