"""Organization routes."""

import http
from typing import Sequence

from fastapi import APIRouter, Depends
from fastapi.params import Depends as DependsParam
from starlette import status

from src.core.api.v1.presentation.exceptions.responses_error import (
    ResponseError,
)
from src.core.api.v1.presentation.responses.organization import (
    CollectionOrganizationResponse,
    OrganizationResponse,
)
from src.core.api.v1.routes.organization.endpoints import (
    org_by_activities_tree,
    org_by_activity,
    org_by_building,
    org_by_id,
    org_by_location,
    org_by_name,
)
from src.core.api.v1.routes.utils.dependencies.api_key import get_api_key

router = APIRouter(tags=["Organization"])

common_depends: Sequence[DependsParam] = [
    Depends(get_api_key),
]

router.add_api_route(
    endpoint=org_by_id,
    methods=[http.HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    path="/org/{id}",
    response_model=OrganizationResponse,
    responses=ResponseError.RESPONSES,
    dependencies=common_depends,
)

router.add_api_route(
    endpoint=org_by_name,
    methods=[http.HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    path="/org/name",
    response_model=OrganizationResponse,
    responses=ResponseError.RESPONSES,
    dependencies=common_depends,
)

router.add_api_route(
    endpoint=org_by_building,
    methods=[http.HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    path="/org/building/{id}",
    response_model=CollectionOrganizationResponse,
    responses=ResponseError.RESPONSES,
    dependencies=common_depends,
)

router.add_api_route(
    endpoint=org_by_location,
    methods=[http.HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    path="/org/location/{lat}/{lon}",
    response_model=CollectionOrganizationResponse,
    responses=ResponseError.RESPONSES,
    dependencies=common_depends,
)

router.add_api_route(
    endpoint=org_by_activities_tree,
    methods=[http.HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    path="/org/{activity}/tree",
    response_model=CollectionOrganizationResponse,
    responses=ResponseError.RESPONSES,
    dependencies=common_depends,
)

router.add_api_route(
    endpoint=org_by_activity,
    methods=[http.HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    path="/org/{activity}",
    response_model=CollectionOrganizationResponse,
    responses=ResponseError.RESPONSES,
    dependencies=common_depends,
)
