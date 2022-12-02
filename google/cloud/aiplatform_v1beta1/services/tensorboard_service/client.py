# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import os
import re
from typing import Dict, Mapping, Optional, Iterable, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation as gac_operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.aiplatform_v1beta1.services.tensorboard_service import pagers
from google.cloud.aiplatform_v1beta1.types import encryption_spec
from google.cloud.aiplatform_v1beta1.types import operation as gca_operation
from google.cloud.aiplatform_v1beta1.types import tensorboard
from google.cloud.aiplatform_v1beta1.types import tensorboard as gca_tensorboard
from google.cloud.aiplatform_v1beta1.types import tensorboard_data
from google.cloud.aiplatform_v1beta1.types import tensorboard_experiment
from google.cloud.aiplatform_v1beta1.types import (
    tensorboard_experiment as gca_tensorboard_experiment,
)
from google.cloud.aiplatform_v1beta1.types import tensorboard_run
from google.cloud.aiplatform_v1beta1.types import tensorboard_run as gca_tensorboard_run
from google.cloud.aiplatform_v1beta1.types import tensorboard_service
from google.cloud.aiplatform_v1beta1.types import tensorboard_time_series
from google.cloud.aiplatform_v1beta1.types import (
    tensorboard_time_series as gca_tensorboard_time_series,
)
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import TensorboardServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import TensorboardServiceGrpcTransport
from .transports.grpc_asyncio import TensorboardServiceGrpcAsyncIOTransport


class TensorboardServiceClientMeta(type):
    """Metaclass for the TensorboardService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[TensorboardServiceTransport]]
    _transport_registry["grpc"] = TensorboardServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = TensorboardServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: str = None,
    ) -> Type[TensorboardServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class TensorboardServiceClient(metaclass=TensorboardServiceClientMeta):
    """TensorboardService"""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "aiplatform.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TensorboardServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TensorboardServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> TensorboardServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            TensorboardServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def tensorboard_path(
        project: str,
        location: str,
        tensorboard: str,
    ) -> str:
        """Returns a fully-qualified tensorboard string."""
        return (
            "projects/{project}/locations/{location}/tensorboards/{tensorboard}".format(
                project=project,
                location=location,
                tensorboard=tensorboard,
            )
        )

    @staticmethod
    def parse_tensorboard_path(path: str) -> Dict[str, str]:
        """Parses a tensorboard path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/tensorboards/(?P<tensorboard>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def tensorboard_experiment_path(
        project: str,
        location: str,
        tensorboard: str,
        experiment: str,
    ) -> str:
        """Returns a fully-qualified tensorboard_experiment string."""
        return "projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}".format(
            project=project,
            location=location,
            tensorboard=tensorboard,
            experiment=experiment,
        )

    @staticmethod
    def parse_tensorboard_experiment_path(path: str) -> Dict[str, str]:
        """Parses a tensorboard_experiment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/tensorboards/(?P<tensorboard>.+?)/experiments/(?P<experiment>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def tensorboard_run_path(
        project: str,
        location: str,
        tensorboard: str,
        experiment: str,
        run: str,
    ) -> str:
        """Returns a fully-qualified tensorboard_run string."""
        return "projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}".format(
            project=project,
            location=location,
            tensorboard=tensorboard,
            experiment=experiment,
            run=run,
        )

    @staticmethod
    def parse_tensorboard_run_path(path: str) -> Dict[str, str]:
        """Parses a tensorboard_run path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/tensorboards/(?P<tensorboard>.+?)/experiments/(?P<experiment>.+?)/runs/(?P<run>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def tensorboard_time_series_path(
        project: str,
        location: str,
        tensorboard: str,
        experiment: str,
        run: str,
        time_series: str,
    ) -> str:
        """Returns a fully-qualified tensorboard_time_series string."""
        return "projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}/timeSeries/{time_series}".format(
            project=project,
            location=location,
            tensorboard=tensorboard,
            experiment=experiment,
            run=run,
            time_series=time_series,
        )

    @staticmethod
    def parse_tensorboard_time_series_path(path: str) -> Dict[str, str]:
        """Parses a tensorboard_time_series path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/tensorboards/(?P<tensorboard>.+?)/experiments/(?P<experiment>.+?)/runs/(?P<run>.+?)/timeSeries/(?P<time_series>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, TensorboardServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the tensorboard service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, TensorboardServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, TensorboardServiceTransport):
            # transport is a TensorboardServiceTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def create_tensorboard(
        self,
        request: Union[tensorboard_service.CreateTensorboardRequest, dict] = None,
        *,
        parent: str = None,
        tensorboard: gca_tensorboard.Tensorboard = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Creates a Tensorboard.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_create_tensorboard():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                tensorboard = aiplatform_v1beta1.Tensorboard()
                tensorboard.display_name = "display_name_value"

                request = aiplatform_v1beta1.CreateTensorboardRequest(
                    parent="parent_value",
                    tensorboard=tensorboard,
                )

                # Make the request
                operation = client.create_tensorboard(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.CreateTensorboardRequest, dict]):
                The request object. Request message for
                [TensorboardService.CreateTensorboard][google.cloud.aiplatform.v1beta1.TensorboardService.CreateTensorboard].
            parent (str):
                Required. The resource name of the Location to create
                the Tensorboard in. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tensorboard (google.cloud.aiplatform_v1beta1.types.Tensorboard):
                Required. The Tensorboard to create.
                This corresponds to the ``tensorboard`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.aiplatform_v1beta1.types.Tensorboard` Tensorboard is a physical database that stores users' training metrics.
                   A default Tensorboard is provided in each region of a
                   Google Cloud project. If needed users can also create
                   extra Tensorboards in their projects.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, tensorboard])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.CreateTensorboardRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.CreateTensorboardRequest):
            request = tensorboard_service.CreateTensorboardRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if tensorboard is not None:
                request.tensorboard = tensorboard

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_tensorboard]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            gca_tensorboard.Tensorboard,
            metadata_type=tensorboard_service.CreateTensorboardOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_tensorboard(
        self,
        request: Union[tensorboard_service.GetTensorboardRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard.Tensorboard:
        r"""Gets a Tensorboard.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_get_tensorboard():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.GetTensorboardRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_tensorboard(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.GetTensorboardRequest, dict]):
                The request object. Request message for
                [TensorboardService.GetTensorboard][google.cloud.aiplatform.v1beta1.TensorboardService.GetTensorboard].
            name (str):
                Required. The name of the Tensorboard resource. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.Tensorboard:
                Tensorboard is a physical database
                that stores users' training metrics. A
                default Tensorboard is provided in each
                region of a Google Cloud project. If
                needed users can also create extra
                Tensorboards in their projects.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.GetTensorboardRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.GetTensorboardRequest):
            request = tensorboard_service.GetTensorboardRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_tensorboard]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_tensorboard(
        self,
        request: Union[tensorboard_service.UpdateTensorboardRequest, dict] = None,
        *,
        tensorboard: gca_tensorboard.Tensorboard = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Updates a Tensorboard.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_update_tensorboard():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                tensorboard = aiplatform_v1beta1.Tensorboard()
                tensorboard.display_name = "display_name_value"

                request = aiplatform_v1beta1.UpdateTensorboardRequest(
                    tensorboard=tensorboard,
                )

                # Make the request
                operation = client.update_tensorboard(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.UpdateTensorboardRequest, dict]):
                The request object. Request message for
                [TensorboardService.UpdateTensorboard][google.cloud.aiplatform.v1beta1.TensorboardService.UpdateTensorboard].
            tensorboard (google.cloud.aiplatform_v1beta1.types.Tensorboard):
                Required. The Tensorboard's ``name`` field is used to
                identify the Tensorboard to be updated. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                This corresponds to the ``tensorboard`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the Tensorboard resource by the update.
                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask. If the user does not
                provide a mask then all fields will be overwritten if
                new values are specified.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.aiplatform_v1beta1.types.Tensorboard` Tensorboard is a physical database that stores users' training metrics.
                   A default Tensorboard is provided in each region of a
                   Google Cloud project. If needed users can also create
                   extra Tensorboards in their projects.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.UpdateTensorboardRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.UpdateTensorboardRequest):
            request = tensorboard_service.UpdateTensorboardRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard is not None:
                request.tensorboard = tensorboard
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_tensorboard]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard.name", request.tensorboard.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            gca_tensorboard.Tensorboard,
            metadata_type=tensorboard_service.UpdateTensorboardOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_tensorboards(
        self,
        request: Union[tensorboard_service.ListTensorboardsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTensorboardsPager:
        r"""Lists Tensorboards in a Location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_list_tensorboards():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.ListTensorboardsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_tensorboards(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.ListTensorboardsRequest, dict]):
                The request object. Request message for
                [TensorboardService.ListTensorboards][google.cloud.aiplatform.v1beta1.TensorboardService.ListTensorboards].
            parent (str):
                Required. The resource name of the Location to list
                Tensorboards. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.tensorboard_service.pagers.ListTensorboardsPager:
                Response message for
                [TensorboardService.ListTensorboards][google.cloud.aiplatform.v1beta1.TensorboardService.ListTensorboards].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.ListTensorboardsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.ListTensorboardsRequest):
            request = tensorboard_service.ListTensorboardsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_tensorboards]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTensorboardsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_tensorboard(
        self,
        request: Union[tensorboard_service.DeleteTensorboardRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Deletes a Tensorboard.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_delete_tensorboard():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.DeleteTensorboardRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_tensorboard(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.DeleteTensorboardRequest, dict]):
                The request object. Request message for
                [TensorboardService.DeleteTensorboard][google.cloud.aiplatform.v1beta1.TensorboardService.DeleteTensorboard].
            name (str):
                Required. The name of the Tensorboard to be deleted.
                Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.DeleteTensorboardRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.DeleteTensorboardRequest):
            request = tensorboard_service.DeleteTensorboardRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_tensorboard]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def create_tensorboard_experiment(
        self,
        request: Union[
            tensorboard_service.CreateTensorboardExperimentRequest, dict
        ] = None,
        *,
        parent: str = None,
        tensorboard_experiment: gca_tensorboard_experiment.TensorboardExperiment = None,
        tensorboard_experiment_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_tensorboard_experiment.TensorboardExperiment:
        r"""Creates a TensorboardExperiment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_create_tensorboard_experiment():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.CreateTensorboardExperimentRequest(
                    parent="parent_value",
                    tensorboard_experiment_id="tensorboard_experiment_id_value",
                )

                # Make the request
                response = client.create_tensorboard_experiment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.CreateTensorboardExperimentRequest, dict]):
                The request object. Request message for
                [TensorboardService.CreateTensorboardExperiment][google.cloud.aiplatform.v1beta1.TensorboardService.CreateTensorboardExperiment].
            parent (str):
                Required. The resource name of the Tensorboard to create
                the TensorboardExperiment in. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tensorboard_experiment (google.cloud.aiplatform_v1beta1.types.TensorboardExperiment):
                The TensorboardExperiment to create.
                This corresponds to the ``tensorboard_experiment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tensorboard_experiment_id (str):
                Required. The ID to use for the Tensorboard experiment,
                which will become the final component of the Tensorboard
                experiment's resource name.

                This value should be 1-128 characters, and valid
                characters are /[a-z][0-9]-/.

                This corresponds to the ``tensorboard_experiment_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardExperiment:
                A TensorboardExperiment is a group of
                TensorboardRuns, that are typically the
                results of a training job run, in a
                Tensorboard.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, tensorboard_experiment, tensorboard_experiment_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.CreateTensorboardExperimentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.CreateTensorboardExperimentRequest
        ):
            request = tensorboard_service.CreateTensorboardExperimentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if tensorboard_experiment is not None:
                request.tensorboard_experiment = tensorboard_experiment
            if tensorboard_experiment_id is not None:
                request.tensorboard_experiment_id = tensorboard_experiment_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_tensorboard_experiment
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_tensorboard_experiment(
        self,
        request: Union[
            tensorboard_service.GetTensorboardExperimentRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_experiment.TensorboardExperiment:
        r"""Gets a TensorboardExperiment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_get_tensorboard_experiment():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.GetTensorboardExperimentRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_tensorboard_experiment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.GetTensorboardExperimentRequest, dict]):
                The request object. Request message for
                [TensorboardService.GetTensorboardExperiment][google.cloud.aiplatform.v1beta1.TensorboardService.GetTensorboardExperiment].
            name (str):
                Required. The name of the TensorboardExperiment
                resource. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardExperiment:
                A TensorboardExperiment is a group of
                TensorboardRuns, that are typically the
                results of a training job run, in a
                Tensorboard.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.GetTensorboardExperimentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.GetTensorboardExperimentRequest):
            request = tensorboard_service.GetTensorboardExperimentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_tensorboard_experiment
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_tensorboard_experiment(
        self,
        request: Union[
            tensorboard_service.UpdateTensorboardExperimentRequest, dict
        ] = None,
        *,
        tensorboard_experiment: gca_tensorboard_experiment.TensorboardExperiment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_tensorboard_experiment.TensorboardExperiment:
        r"""Updates a TensorboardExperiment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_update_tensorboard_experiment():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.UpdateTensorboardExperimentRequest(
                )

                # Make the request
                response = client.update_tensorboard_experiment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.UpdateTensorboardExperimentRequest, dict]):
                The request object. Request message for
                [TensorboardService.UpdateTensorboardExperiment][google.cloud.aiplatform.v1beta1.TensorboardService.UpdateTensorboardExperiment].
            tensorboard_experiment (google.cloud.aiplatform_v1beta1.types.TensorboardExperiment):
                Required. The TensorboardExperiment's ``name`` field is
                used to identify the TensorboardExperiment to be
                updated. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}``

                This corresponds to the ``tensorboard_experiment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the TensorboardExperiment resource by the
                update. The fields specified in the update_mask are
                relative to the resource, not the full request. A field
                will be overwritten if it is in the mask. If the user
                does not provide a mask then all fields will be
                overwritten if new values are specified.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardExperiment:
                A TensorboardExperiment is a group of
                TensorboardRuns, that are typically the
                results of a training job run, in a
                Tensorboard.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard_experiment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.UpdateTensorboardExperimentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.UpdateTensorboardExperimentRequest
        ):
            request = tensorboard_service.UpdateTensorboardExperimentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard_experiment is not None:
                request.tensorboard_experiment = tensorboard_experiment
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_tensorboard_experiment
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard_experiment.name", request.tensorboard_experiment.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_tensorboard_experiments(
        self,
        request: Union[
            tensorboard_service.ListTensorboardExperimentsRequest, dict
        ] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTensorboardExperimentsPager:
        r"""Lists TensorboardExperiments in a Location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_list_tensorboard_experiments():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.ListTensorboardExperimentsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_tensorboard_experiments(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.ListTensorboardExperimentsRequest, dict]):
                The request object. Request message for
                [TensorboardService.ListTensorboardExperiments][google.cloud.aiplatform.v1beta1.TensorboardService.ListTensorboardExperiments].
            parent (str):
                Required. The resource name of the Tensorboard to list
                TensorboardExperiments. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.tensorboard_service.pagers.ListTensorboardExperimentsPager:
                Response message for
                [TensorboardService.ListTensorboardExperiments][google.cloud.aiplatform.v1beta1.TensorboardService.ListTensorboardExperiments].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.ListTensorboardExperimentsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.ListTensorboardExperimentsRequest
        ):
            request = tensorboard_service.ListTensorboardExperimentsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_tensorboard_experiments
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTensorboardExperimentsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_tensorboard_experiment(
        self,
        request: Union[
            tensorboard_service.DeleteTensorboardExperimentRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Deletes a TensorboardExperiment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_delete_tensorboard_experiment():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.DeleteTensorboardExperimentRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_tensorboard_experiment(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.DeleteTensorboardExperimentRequest, dict]):
                The request object. Request message for
                [TensorboardService.DeleteTensorboardExperiment][google.cloud.aiplatform.v1beta1.TensorboardService.DeleteTensorboardExperiment].
            name (str):
                Required. The name of the TensorboardExperiment to be
                deleted. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.DeleteTensorboardExperimentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.DeleteTensorboardExperimentRequest
        ):
            request = tensorboard_service.DeleteTensorboardExperimentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_tensorboard_experiment
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def create_tensorboard_run(
        self,
        request: Union[tensorboard_service.CreateTensorboardRunRequest, dict] = None,
        *,
        parent: str = None,
        tensorboard_run: gca_tensorboard_run.TensorboardRun = None,
        tensorboard_run_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_tensorboard_run.TensorboardRun:
        r"""Creates a TensorboardRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_create_tensorboard_run():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                tensorboard_run = aiplatform_v1beta1.TensorboardRun()
                tensorboard_run.display_name = "display_name_value"

                request = aiplatform_v1beta1.CreateTensorboardRunRequest(
                    parent="parent_value",
                    tensorboard_run=tensorboard_run,
                    tensorboard_run_id="tensorboard_run_id_value",
                )

                # Make the request
                response = client.create_tensorboard_run(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.CreateTensorboardRunRequest, dict]):
                The request object. Request message for
                [TensorboardService.CreateTensorboardRun][google.cloud.aiplatform.v1beta1.TensorboardService.CreateTensorboardRun].
            parent (str):
                Required. The resource name of the TensorboardExperiment
                to create the TensorboardRun in. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tensorboard_run (google.cloud.aiplatform_v1beta1.types.TensorboardRun):
                Required. The TensorboardRun to
                create.

                This corresponds to the ``tensorboard_run`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tensorboard_run_id (str):
                Required. The ID to use for the Tensorboard run, which
                will become the final component of the Tensorboard run's
                resource name.

                This value should be 1-128 characters, and valid
                characters are /[a-z][0-9]-/.

                This corresponds to the ``tensorboard_run_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardRun:
                TensorboardRun maps to a specific
                execution of a training job with a given
                set of hyperparameter values, model
                definition, dataset, etc

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, tensorboard_run, tensorboard_run_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.CreateTensorboardRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.CreateTensorboardRunRequest):
            request = tensorboard_service.CreateTensorboardRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if tensorboard_run is not None:
                request.tensorboard_run = tensorboard_run
            if tensorboard_run_id is not None:
                request.tensorboard_run_id = tensorboard_run_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_tensorboard_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def batch_create_tensorboard_runs(
        self,
        request: Union[
            tensorboard_service.BatchCreateTensorboardRunsRequest, dict
        ] = None,
        *,
        parent: str = None,
        requests: Sequence[tensorboard_service.CreateTensorboardRunRequest] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_service.BatchCreateTensorboardRunsResponse:
        r"""Batch create TensorboardRuns.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_batch_create_tensorboard_runs():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                requests = aiplatform_v1beta1.CreateTensorboardRunRequest()
                requests.parent = "parent_value"
                requests.tensorboard_run.display_name = "display_name_value"
                requests.tensorboard_run_id = "tensorboard_run_id_value"

                request = aiplatform_v1beta1.BatchCreateTensorboardRunsRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                response = client.batch_create_tensorboard_runs(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.BatchCreateTensorboardRunsRequest, dict]):
                The request object. Request message for
                [TensorboardService.BatchCreateTensorboardRuns][google.cloud.aiplatform.v1beta1.TensorboardService.BatchCreateTensorboardRuns].
            parent (str):
                Required. The resource name of the TensorboardExperiment
                to create the TensorboardRuns in. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}``
                The parent field in the CreateTensorboardRunRequest
                messages must match this field.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            requests (Sequence[google.cloud.aiplatform_v1beta1.types.CreateTensorboardRunRequest]):
                Required. The request message
                specifying the TensorboardRuns to
                create. A maximum of 1000
                TensorboardRuns can be created in a
                batch.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.BatchCreateTensorboardRunsResponse:
                Response message for
                [TensorboardService.BatchCreateTensorboardRuns][google.cloud.aiplatform.v1beta1.TensorboardService.BatchCreateTensorboardRuns].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, requests])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.BatchCreateTensorboardRunsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.BatchCreateTensorboardRunsRequest
        ):
            request = tensorboard_service.BatchCreateTensorboardRunsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if requests is not None:
                request.requests = requests

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_create_tensorboard_runs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_tensorboard_run(
        self,
        request: Union[tensorboard_service.GetTensorboardRunRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_run.TensorboardRun:
        r"""Gets a TensorboardRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_get_tensorboard_run():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.GetTensorboardRunRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_tensorboard_run(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.GetTensorboardRunRequest, dict]):
                The request object. Request message for
                [TensorboardService.GetTensorboardRun][google.cloud.aiplatform.v1beta1.TensorboardService.GetTensorboardRun].
            name (str):
                Required. The name of the TensorboardRun resource.
                Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardRun:
                TensorboardRun maps to a specific
                execution of a training job with a given
                set of hyperparameter values, model
                definition, dataset, etc

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.GetTensorboardRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.GetTensorboardRunRequest):
            request = tensorboard_service.GetTensorboardRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_tensorboard_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_tensorboard_run(
        self,
        request: Union[tensorboard_service.UpdateTensorboardRunRequest, dict] = None,
        *,
        tensorboard_run: gca_tensorboard_run.TensorboardRun = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_tensorboard_run.TensorboardRun:
        r"""Updates a TensorboardRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_update_tensorboard_run():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                tensorboard_run = aiplatform_v1beta1.TensorboardRun()
                tensorboard_run.display_name = "display_name_value"

                request = aiplatform_v1beta1.UpdateTensorboardRunRequest(
                    tensorboard_run=tensorboard_run,
                )

                # Make the request
                response = client.update_tensorboard_run(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.UpdateTensorboardRunRequest, dict]):
                The request object. Request message for
                [TensorboardService.UpdateTensorboardRun][google.cloud.aiplatform.v1beta1.TensorboardService.UpdateTensorboardRun].
            tensorboard_run (google.cloud.aiplatform_v1beta1.types.TensorboardRun):
                Required. The TensorboardRun's ``name`` field is used to
                identify the TensorboardRun to be updated. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}``

                This corresponds to the ``tensorboard_run`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the TensorboardRun resource by the
                update. The fields specified in the update_mask are
                relative to the resource, not the full request. A field
                will be overwritten if it is in the mask. If the user
                does not provide a mask then all fields will be
                overwritten if new values are specified.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardRun:
                TensorboardRun maps to a specific
                execution of a training job with a given
                set of hyperparameter values, model
                definition, dataset, etc

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard_run, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.UpdateTensorboardRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.UpdateTensorboardRunRequest):
            request = tensorboard_service.UpdateTensorboardRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard_run is not None:
                request.tensorboard_run = tensorboard_run
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_tensorboard_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard_run.name", request.tensorboard_run.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_tensorboard_runs(
        self,
        request: Union[tensorboard_service.ListTensorboardRunsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTensorboardRunsPager:
        r"""Lists TensorboardRuns in a Location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_list_tensorboard_runs():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.ListTensorboardRunsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_tensorboard_runs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.ListTensorboardRunsRequest, dict]):
                The request object. Request message for
                [TensorboardService.ListTensorboardRuns][google.cloud.aiplatform.v1beta1.TensorboardService.ListTensorboardRuns].
            parent (str):
                Required. The resource name of the TensorboardExperiment
                to list TensorboardRuns. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.tensorboard_service.pagers.ListTensorboardRunsPager:
                Response message for
                [TensorboardService.ListTensorboardRuns][google.cloud.aiplatform.v1beta1.TensorboardService.ListTensorboardRuns].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.ListTensorboardRunsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.ListTensorboardRunsRequest):
            request = tensorboard_service.ListTensorboardRunsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_tensorboard_runs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTensorboardRunsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_tensorboard_run(
        self,
        request: Union[tensorboard_service.DeleteTensorboardRunRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Deletes a TensorboardRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_delete_tensorboard_run():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.DeleteTensorboardRunRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_tensorboard_run(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.DeleteTensorboardRunRequest, dict]):
                The request object. Request message for
                [TensorboardService.DeleteTensorboardRun][google.cloud.aiplatform.v1beta1.TensorboardService.DeleteTensorboardRun].
            name (str):
                Required. The name of the TensorboardRun to be deleted.
                Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.DeleteTensorboardRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.DeleteTensorboardRunRequest):
            request = tensorboard_service.DeleteTensorboardRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_tensorboard_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def batch_create_tensorboard_time_series(
        self,
        request: Union[
            tensorboard_service.BatchCreateTensorboardTimeSeriesRequest, dict
        ] = None,
        *,
        parent: str = None,
        requests: Sequence[
            tensorboard_service.CreateTensorboardTimeSeriesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_service.BatchCreateTensorboardTimeSeriesResponse:
        r"""Batch create TensorboardTimeSeries that belong to a
        TensorboardExperiment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_batch_create_tensorboard_time_series():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                requests = aiplatform_v1beta1.CreateTensorboardTimeSeriesRequest()
                requests.parent = "parent_value"
                requests.tensorboard_time_series.display_name = "display_name_value"
                requests.tensorboard_time_series.value_type = "BLOB_SEQUENCE"

                request = aiplatform_v1beta1.BatchCreateTensorboardTimeSeriesRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                response = client.batch_create_tensorboard_time_series(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.BatchCreateTensorboardTimeSeriesRequest, dict]):
                The request object. Request message for
                [TensorboardService.BatchCreateTensorboardTimeSeries][google.cloud.aiplatform.v1beta1.TensorboardService.BatchCreateTensorboardTimeSeries].
            parent (str):
                Required. The resource name of the TensorboardExperiment
                to create the TensorboardTimeSeries in. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}``
                The TensorboardRuns referenced by the parent fields in
                the CreateTensorboardTimeSeriesRequest messages must be
                sub resources of this TensorboardExperiment.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            requests (Sequence[google.cloud.aiplatform_v1beta1.types.CreateTensorboardTimeSeriesRequest]):
                Required. The request message
                specifying the TensorboardTimeSeries to
                create. A maximum of 1000
                TensorboardTimeSeries can be created in
                a batch.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.BatchCreateTensorboardTimeSeriesResponse:
                Response message for
                [TensorboardService.BatchCreateTensorboardTimeSeries][google.cloud.aiplatform.v1beta1.TensorboardService.BatchCreateTensorboardTimeSeries].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, requests])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.BatchCreateTensorboardTimeSeriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.BatchCreateTensorboardTimeSeriesRequest
        ):
            request = tensorboard_service.BatchCreateTensorboardTimeSeriesRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if requests is not None:
                request.requests = requests

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_create_tensorboard_time_series
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_tensorboard_time_series(
        self,
        request: Union[
            tensorboard_service.CreateTensorboardTimeSeriesRequest, dict
        ] = None,
        *,
        parent: str = None,
        tensorboard_time_series: gca_tensorboard_time_series.TensorboardTimeSeries = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_tensorboard_time_series.TensorboardTimeSeries:
        r"""Creates a TensorboardTimeSeries.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_create_tensorboard_time_series():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                tensorboard_time_series = aiplatform_v1beta1.TensorboardTimeSeries()
                tensorboard_time_series.display_name = "display_name_value"
                tensorboard_time_series.value_type = "BLOB_SEQUENCE"

                request = aiplatform_v1beta1.CreateTensorboardTimeSeriesRequest(
                    parent="parent_value",
                    tensorboard_time_series=tensorboard_time_series,
                )

                # Make the request
                response = client.create_tensorboard_time_series(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.CreateTensorboardTimeSeriesRequest, dict]):
                The request object. Request message for
                [TensorboardService.CreateTensorboardTimeSeries][google.cloud.aiplatform.v1beta1.TensorboardService.CreateTensorboardTimeSeries].
            parent (str):
                Required. The resource name of the TensorboardRun to
                create the TensorboardTimeSeries in. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tensorboard_time_series (google.cloud.aiplatform_v1beta1.types.TensorboardTimeSeries):
                Required. The TensorboardTimeSeries
                to create.

                This corresponds to the ``tensorboard_time_series`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardTimeSeries:
                TensorboardTimeSeries maps to times
                series produced in training runs

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, tensorboard_time_series])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.CreateTensorboardTimeSeriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.CreateTensorboardTimeSeriesRequest
        ):
            request = tensorboard_service.CreateTensorboardTimeSeriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if tensorboard_time_series is not None:
                request.tensorboard_time_series = tensorboard_time_series

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_tensorboard_time_series
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_tensorboard_time_series(
        self,
        request: Union[
            tensorboard_service.GetTensorboardTimeSeriesRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_time_series.TensorboardTimeSeries:
        r"""Gets a TensorboardTimeSeries.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_get_tensorboard_time_series():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.GetTensorboardTimeSeriesRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_tensorboard_time_series(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.GetTensorboardTimeSeriesRequest, dict]):
                The request object. Request message for
                [TensorboardService.GetTensorboardTimeSeries][google.cloud.aiplatform.v1beta1.TensorboardService.GetTensorboardTimeSeries].
            name (str):
                Required. The name of the TensorboardTimeSeries
                resource. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}/timeSeries/{time_series}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardTimeSeries:
                TensorboardTimeSeries maps to times
                series produced in training runs

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.GetTensorboardTimeSeriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.GetTensorboardTimeSeriesRequest):
            request = tensorboard_service.GetTensorboardTimeSeriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_tensorboard_time_series
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_tensorboard_time_series(
        self,
        request: Union[
            tensorboard_service.UpdateTensorboardTimeSeriesRequest, dict
        ] = None,
        *,
        tensorboard_time_series: gca_tensorboard_time_series.TensorboardTimeSeries = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gca_tensorboard_time_series.TensorboardTimeSeries:
        r"""Updates a TensorboardTimeSeries.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_update_tensorboard_time_series():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                tensorboard_time_series = aiplatform_v1beta1.TensorboardTimeSeries()
                tensorboard_time_series.display_name = "display_name_value"
                tensorboard_time_series.value_type = "BLOB_SEQUENCE"

                request = aiplatform_v1beta1.UpdateTensorboardTimeSeriesRequest(
                    tensorboard_time_series=tensorboard_time_series,
                )

                # Make the request
                response = client.update_tensorboard_time_series(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.UpdateTensorboardTimeSeriesRequest, dict]):
                The request object. Request message for
                [TensorboardService.UpdateTensorboardTimeSeries][google.cloud.aiplatform.v1beta1.TensorboardService.UpdateTensorboardTimeSeries].
            tensorboard_time_series (google.cloud.aiplatform_v1beta1.types.TensorboardTimeSeries):
                Required. The TensorboardTimeSeries' ``name`` field is
                used to identify the TensorboardTimeSeries to be
                updated. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}/timeSeries/{time_series}``

                This corresponds to the ``tensorboard_time_series`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the TensorboardTimeSeries resource by the
                update. The fields specified in the update_mask are
                relative to the resource, not the full request. A field
                will be overwritten if it is in the mask. If the user
                does not provide a mask then all fields will be
                overwritten if new values are specified.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.TensorboardTimeSeries:
                TensorboardTimeSeries maps to times
                series produced in training runs

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard_time_series, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.UpdateTensorboardTimeSeriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.UpdateTensorboardTimeSeriesRequest
        ):
            request = tensorboard_service.UpdateTensorboardTimeSeriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard_time_series is not None:
                request.tensorboard_time_series = tensorboard_time_series
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_tensorboard_time_series
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "tensorboard_time_series.name",
                        request.tensorboard_time_series.name,
                    ),
                )
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_tensorboard_time_series(
        self,
        request: Union[
            tensorboard_service.ListTensorboardTimeSeriesRequest, dict
        ] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTensorboardTimeSeriesPager:
        r"""Lists TensorboardTimeSeries in a Location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_list_tensorboard_time_series():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.ListTensorboardTimeSeriesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_tensorboard_time_series(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.ListTensorboardTimeSeriesRequest, dict]):
                The request object. Request message for
                [TensorboardService.ListTensorboardTimeSeries][google.cloud.aiplatform.v1beta1.TensorboardService.ListTensorboardTimeSeries].
            parent (str):
                Required. The resource name of the TensorboardRun to
                list TensorboardTimeSeries. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.tensorboard_service.pagers.ListTensorboardTimeSeriesPager:
                Response message for
                [TensorboardService.ListTensorboardTimeSeries][google.cloud.aiplatform.v1beta1.TensorboardService.ListTensorboardTimeSeries].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.ListTensorboardTimeSeriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.ListTensorboardTimeSeriesRequest
        ):
            request = tensorboard_service.ListTensorboardTimeSeriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_tensorboard_time_series
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTensorboardTimeSeriesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_tensorboard_time_series(
        self,
        request: Union[
            tensorboard_service.DeleteTensorboardTimeSeriesRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gac_operation.Operation:
        r"""Deletes a TensorboardTimeSeries.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_delete_tensorboard_time_series():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.DeleteTensorboardTimeSeriesRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_tensorboard_time_series(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.DeleteTensorboardTimeSeriesRequest, dict]):
                The request object. Request message for
                [TensorboardService.DeleteTensorboardTimeSeries][google.cloud.aiplatform.v1beta1.TensorboardService.DeleteTensorboardTimeSeries].
            name (str):
                Required. The name of the TensorboardTimeSeries to be
                deleted. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}/timeSeries/{time_series}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.DeleteTensorboardTimeSeriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.DeleteTensorboardTimeSeriesRequest
        ):
            request = tensorboard_service.DeleteTensorboardTimeSeriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_tensorboard_time_series
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = gac_operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gca_operation.DeleteOperationMetadata,
        )

        # Done; return the response.
        return response

    def batch_read_tensorboard_time_series_data(
        self,
        request: Union[
            tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest, dict
        ] = None,
        *,
        tensorboard: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse:
        r"""Reads multiple TensorboardTimeSeries' data. The data
        point number limit is 1000 for scalars, 100 for tensors
        and blob references. If the number of data points stored
        is less than the limit, all data will be returned.
        Otherwise, that limit number of data points will be
        randomly selected from this time series and returned.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_batch_read_tensorboard_time_series_data():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.BatchReadTensorboardTimeSeriesDataRequest(
                    tensorboard="tensorboard_value",
                    time_series=['time_series_value1', 'time_series_value2'],
                )

                # Make the request
                response = client.batch_read_tensorboard_time_series_data(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.BatchReadTensorboardTimeSeriesDataRequest, dict]):
                The request object. Request message for
                [TensorboardService.BatchReadTensorboardTimeSeriesData][google.cloud.aiplatform.v1beta1.TensorboardService.BatchReadTensorboardTimeSeriesData].
            tensorboard (str):
                Required. The resource name of the Tensorboard
                containing TensorboardTimeSeries to read data from.
                Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}``.
                The TensorboardTimeSeries referenced by
                [time_series][google.cloud.aiplatform.v1beta1.BatchReadTensorboardTimeSeriesDataRequest.time_series]
                must be sub resources of this Tensorboard.

                This corresponds to the ``tensorboard`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.BatchReadTensorboardTimeSeriesDataResponse:
                Response message for
                   [TensorboardService.BatchReadTensorboardTimeSeriesData][google.cloud.aiplatform.v1beta1.TensorboardService.BatchReadTensorboardTimeSeriesData].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest
        ):
            request = tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard is not None:
                request.tensorboard = tensorboard

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_read_tensorboard_time_series_data
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard", request.tensorboard),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def read_tensorboard_time_series_data(
        self,
        request: Union[
            tensorboard_service.ReadTensorboardTimeSeriesDataRequest, dict
        ] = None,
        *,
        tensorboard_time_series: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_service.ReadTensorboardTimeSeriesDataResponse:
        r"""Reads a TensorboardTimeSeries' data. By default, if the number
        of data points stored is less than 1000, all data will be
        returned. Otherwise, 1000 data points will be randomly selected
        from this time series and returned. This value can be changed by
        changing max_data_points, which can't be greater than 10k.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_read_tensorboard_time_series_data():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.ReadTensorboardTimeSeriesDataRequest(
                    tensorboard_time_series="tensorboard_time_series_value",
                )

                # Make the request
                response = client.read_tensorboard_time_series_data(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.ReadTensorboardTimeSeriesDataRequest, dict]):
                The request object. Request message for
                [TensorboardService.ReadTensorboardTimeSeriesData][google.cloud.aiplatform.v1beta1.TensorboardService.ReadTensorboardTimeSeriesData].
            tensorboard_time_series (str):
                Required. The resource name of the TensorboardTimeSeries
                to read data from. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}/timeSeries/{time_series}``

                This corresponds to the ``tensorboard_time_series`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.ReadTensorboardTimeSeriesDataResponse:
                Response message for
                [TensorboardService.ReadTensorboardTimeSeriesData][google.cloud.aiplatform.v1beta1.TensorboardService.ReadTensorboardTimeSeriesData].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard_time_series])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.ReadTensorboardTimeSeriesDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.ReadTensorboardTimeSeriesDataRequest
        ):
            request = tensorboard_service.ReadTensorboardTimeSeriesDataRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard_time_series is not None:
                request.tensorboard_time_series = tensorboard_time_series

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.read_tensorboard_time_series_data
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard_time_series", request.tensorboard_time_series),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def read_tensorboard_blob_data(
        self,
        request: Union[tensorboard_service.ReadTensorboardBlobDataRequest, dict] = None,
        *,
        time_series: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[tensorboard_service.ReadTensorboardBlobDataResponse]:
        r"""Gets bytes of TensorboardBlobs.
        This is to allow reading blob data stored in consumer
        project's Cloud Storage bucket without users having to
        obtain Cloud Storage access permission.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_read_tensorboard_blob_data():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.ReadTensorboardBlobDataRequest(
                    time_series="time_series_value",
                )

                # Make the request
                stream = client.read_tensorboard_blob_data(request=request)

                # Handle the response
                for response in stream:
                    print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.ReadTensorboardBlobDataRequest, dict]):
                The request object. Request message for
                [TensorboardService.ReadTensorboardBlobData][google.cloud.aiplatform.v1beta1.TensorboardService.ReadTensorboardBlobData].
            time_series (str):
                Required. The resource name of the TensorboardTimeSeries
                to list Blobs. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}/timeSeries/{time_series}``

                This corresponds to the ``time_series`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.cloud.aiplatform_v1beta1.types.ReadTensorboardBlobDataResponse]:
                Response message for
                [TensorboardService.ReadTensorboardBlobData][google.cloud.aiplatform.v1beta1.TensorboardService.ReadTensorboardBlobData].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([time_series])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.ReadTensorboardBlobDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.ReadTensorboardBlobDataRequest):
            request = tensorboard_service.ReadTensorboardBlobDataRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if time_series is not None:
                request.time_series = time_series

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.read_tensorboard_blob_data
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("time_series", request.time_series),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def write_tensorboard_experiment_data(
        self,
        request: Union[
            tensorboard_service.WriteTensorboardExperimentDataRequest, dict
        ] = None,
        *,
        tensorboard_experiment: str = None,
        write_run_data_requests: Sequence[
            tensorboard_service.WriteTensorboardRunDataRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_service.WriteTensorboardExperimentDataResponse:
        r"""Write time series data points of multiple
        TensorboardTimeSeries in multiple TensorboardRun's. If
        any data fail to be ingested, an error will be returned.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_write_tensorboard_experiment_data():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                write_run_data_requests = aiplatform_v1beta1.WriteTensorboardRunDataRequest()
                write_run_data_requests.tensorboard_run = "tensorboard_run_value"
                write_run_data_requests.time_series_data.tensorboard_time_series_id = "tensorboard_time_series_id_value"
                write_run_data_requests.time_series_data.value_type = "BLOB_SEQUENCE"

                request = aiplatform_v1beta1.WriteTensorboardExperimentDataRequest(
                    tensorboard_experiment="tensorboard_experiment_value",
                    write_run_data_requests=write_run_data_requests,
                )

                # Make the request
                response = client.write_tensorboard_experiment_data(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.WriteTensorboardExperimentDataRequest, dict]):
                The request object. Request message for
                [TensorboardService.WriteTensorboardExperimentData][google.cloud.aiplatform.v1beta1.TensorboardService.WriteTensorboardExperimentData].
            tensorboard_experiment (str):
                Required. The resource name of the TensorboardExperiment
                to write data to. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}``

                This corresponds to the ``tensorboard_experiment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            write_run_data_requests (Sequence[google.cloud.aiplatform_v1beta1.types.WriteTensorboardRunDataRequest]):
                Required. Requests containing per-run
                TensorboardTimeSeries data to write.

                This corresponds to the ``write_run_data_requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.WriteTensorboardExperimentDataResponse:
                Response message for
                [TensorboardService.WriteTensorboardExperimentData][google.cloud.aiplatform.v1beta1.TensorboardService.WriteTensorboardExperimentData].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard_experiment, write_run_data_requests])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.WriteTensorboardExperimentDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.WriteTensorboardExperimentDataRequest
        ):
            request = tensorboard_service.WriteTensorboardExperimentDataRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard_experiment is not None:
                request.tensorboard_experiment = tensorboard_experiment
            if write_run_data_requests is not None:
                request.write_run_data_requests = write_run_data_requests

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.write_tensorboard_experiment_data
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard_experiment", request.tensorboard_experiment),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def write_tensorboard_run_data(
        self,
        request: Union[tensorboard_service.WriteTensorboardRunDataRequest, dict] = None,
        *,
        tensorboard_run: str = None,
        time_series_data: Sequence[tensorboard_data.TimeSeriesData] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tensorboard_service.WriteTensorboardRunDataResponse:
        r"""Write time series data points into multiple
        TensorboardTimeSeries under a TensorboardRun. If any
        data fail to be ingested, an error will be returned.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_write_tensorboard_run_data():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                time_series_data = aiplatform_v1beta1.TimeSeriesData()
                time_series_data.tensorboard_time_series_id = "tensorboard_time_series_id_value"
                time_series_data.value_type = "BLOB_SEQUENCE"

                request = aiplatform_v1beta1.WriteTensorboardRunDataRequest(
                    tensorboard_run="tensorboard_run_value",
                    time_series_data=time_series_data,
                )

                # Make the request
                response = client.write_tensorboard_run_data(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.WriteTensorboardRunDataRequest, dict]):
                The request object. Request message for
                [TensorboardService.WriteTensorboardRunData][google.cloud.aiplatform.v1beta1.TensorboardService.WriteTensorboardRunData].
            tensorboard_run (str):
                Required. The resource name of the TensorboardRun to
                write data to. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}``

                This corresponds to the ``tensorboard_run`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            time_series_data (Sequence[google.cloud.aiplatform_v1beta1.types.TimeSeriesData]):
                Required. The TensorboardTimeSeries
                data to write. Values with in a time
                series are indexed by their step value.
                Repeated writes to the same step will
                overwrite the existing value for that
                step.
                The upper limit of data points per write
                request is 5000.

                This corresponds to the ``time_series_data`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.types.WriteTensorboardRunDataResponse:
                Response message for
                [TensorboardService.WriteTensorboardRunData][google.cloud.aiplatform.v1beta1.TensorboardService.WriteTensorboardRunData].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard_run, time_series_data])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.WriteTensorboardRunDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, tensorboard_service.WriteTensorboardRunDataRequest):
            request = tensorboard_service.WriteTensorboardRunDataRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard_run is not None:
                request.tensorboard_run = tensorboard_run
            if time_series_data is not None:
                request.time_series_data = time_series_data

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.write_tensorboard_run_data
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard_run", request.tensorboard_run),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def export_tensorboard_time_series_data(
        self,
        request: Union[
            tensorboard_service.ExportTensorboardTimeSeriesDataRequest, dict
        ] = None,
        *,
        tensorboard_time_series: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ExportTensorboardTimeSeriesDataPager:
        r"""Exports a TensorboardTimeSeries' data. Data is
        returned in paginated responses.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import aiplatform_v1beta1

            def sample_export_tensorboard_time_series_data():
                # Create a client
                client = aiplatform_v1beta1.TensorboardServiceClient()

                # Initialize request argument(s)
                request = aiplatform_v1beta1.ExportTensorboardTimeSeriesDataRequest(
                    tensorboard_time_series="tensorboard_time_series_value",
                )

                # Make the request
                page_result = client.export_tensorboard_time_series_data(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.aiplatform_v1beta1.types.ExportTensorboardTimeSeriesDataRequest, dict]):
                The request object. Request message for
                [TensorboardService.ExportTensorboardTimeSeriesData][google.cloud.aiplatform.v1beta1.TensorboardService.ExportTensorboardTimeSeriesData].
            tensorboard_time_series (str):
                Required. The resource name of the TensorboardTimeSeries
                to export data from. Format:
                ``projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}/timeSeries/{time_series}``

                This corresponds to the ``tensorboard_time_series`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.aiplatform_v1beta1.services.tensorboard_service.pagers.ExportTensorboardTimeSeriesDataPager:
                Response message for
                [TensorboardService.ExportTensorboardTimeSeriesData][google.cloud.aiplatform.v1beta1.TensorboardService.ExportTensorboardTimeSeriesData].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tensorboard_time_series])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a tensorboard_service.ExportTensorboardTimeSeriesDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, tensorboard_service.ExportTensorboardTimeSeriesDataRequest
        ):
            request = tensorboard_service.ExportTensorboardTimeSeriesDataRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if tensorboard_time_series is not None:
                request.tensorboard_time_series = tensorboard_time_series

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.export_tensorboard_time_series_data
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard_time_series", request.tensorboard_time_series),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ExportTensorboardTimeSeriesDataPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: operations_pb2.ListOperationsRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_operation(
        self,
        request: operations_pb2.GetOperationRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def wait_operation(
        self,
        request: operations_pb2.WaitOperationRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Waits until the specified long-running operation is done or reaches at most
        a specified timeout, returning the latest state.

        If the operation is already done, the latest state is immediately returned.
        If the timeout specified is greater than the default HTTP/RPC timeout, the HTTP/RPC
        timeout is used.  If the server does not support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.WaitOperationRequest`):
                The request object. Request message for
                `WaitOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.WaitOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.wait_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM access control policy on the specified function.

        Replaces any existing policy.

        Args:
            request (:class:`~.iam_policy_pb2.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM access control policy for a function.

        Returns an empty policy if the function exists and does not have a
        policy set.

        Args:
            request (:class:`~.iam_policy_pb2.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if
                any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Tests the specified IAM permissions against the IAM access control
            policy for a function.

        If the function does not exist, this will return an empty set
        of permissions, not a NOT_FOUND error.

        Args:
            request (:class:`~.iam_policy_pb2.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.test_iam_permissions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_location(
        self,
        request: locations_pb2.GetLocationRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.Location:
                Location object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.GetLocationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_location,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_locations(
        self,
        request: locations_pb2.ListLocationsRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.ListLocationsResponse:
                Response message for ``ListLocations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.ListLocationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_locations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-aiplatform",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TensorboardServiceClient",)
