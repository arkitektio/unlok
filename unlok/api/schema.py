import builtins
from datetime import datetime
from enum import Enum
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from rath.scalars import ID, IDCoercible
from typing import Annotated, Any, Iterable, Literal


class GraphQLDefault:
    """Records a GraphQL field schema default value. The client omits the field so the server applies its own default; this preserves the value for introspection."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "GraphQLDefault(" + repr(self.value) + ")"


class UnsetType:
    """Sentinel for arguments the caller did not provide. Such fields are omitted on serialization so the GraphQL server applies its own default."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "UNSET"

    def __bool__(self):
        return False


UNSET = UnsetType()


class ClientKind(str, Enum):
    """No documentation"""

    DEVELOPMENT = "DEVELOPMENT"
    WEBSITE = "WEBSITE"
    DESKTOP = "DESKTOP"
    MOBILE = "MOBILE"
    HUB = "HUB"
    RELYING_PARTY = "RELYING_PARTY"
    __str__ = str.__str__


class ClientRole(str, Enum):
    """No documentation"""

    INTERFACE = "INTERFACE"
    AGENT = "AGENT"
    __str__ = str.__str__


class PublicSourceKind(str, Enum):
    """No documentation"""

    GITHUB = "GITHUB"
    WEBSITE = "WEBSITE"
    __str__ = str.__str__


class AppFilter(BaseModel):
    """App(id, name, identifier, organization, logo)"""

    and_: "AppFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "AppFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "AppFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ClientFilter(BaseModel):
    """The one client model: every OAuth2 principal is a row here.

    Kinds of rows and their lifecycle:

    - **App clients** (`development`/`website`/`desktop`/`mobile`): the row is created by
      dynamic registration at ``/o/app-authorization/`` with identity fields
      only; human approval *binds* it (membership, organization, release, hub,
      mappings, scope). ``membership`` null == not yet approved.
    - **Hub identities** (`hub`): same lifecycle via ``/o/hub-authorization/``;
      the created ``Hub`` links back via ``Hub.client`` (reverse:
      ``client.hub_identity``).
    - **Relying parties** (`relying_party`): confidential OIDC clients
      provisioned from config by ``ensureopenid``; global (no organization).

    Implements authlib's ``ClientMixin`` directly — there is no separate
    OAuth2 client table anymore."""

    and_: "ClientFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "ClientFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "ClientFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    role: ClientRole | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateGroupProfileInput(BaseModel):
    """No documentation"""

    group: ID
    name: str
    avatar: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateProfileInput(BaseModel):
    """No documentation"""

    user: ID
    name: str
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateServiceInstanceInput(BaseModel):
    """No documentation"""

    identifier: str
    service: ID
    allowed_users: tuple[ID, ...] | None = Field(
        validation_alias=AliasChoices("allowed_users", "allowedUsers"),
        serialization_alias="allowedUsers",
        default=None,
    )
    allowed_groups: tuple[ID, ...] | None = Field(
        validation_alias=AliasChoices("allowed_groups", "allowedGroups"),
        serialization_alias="allowedGroups",
        default=None,
    )
    denied_groups: tuple[ID, ...] | None = Field(
        validation_alias=AliasChoices("denied_groups", "deniedGroups"),
        serialization_alias="deniedGroups",
        default=None,
    )
    denied_users: tuple[ID, ...] | None = Field(
        validation_alias=AliasChoices("denied_users", "deniedUsers"),
        serialization_alias="deniedUsers",
        default=None,
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DevelopmentClientInput(BaseModel):
    """No documentation"""

    manifest: "ManifestInput"
    hub: ID | None = None
    layers: Annotated[tuple[str, ...] | None, GraphQLDefault("['web']")] = None
    "Default: ['web']"
    role: ClientRole | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GroupFilter(BaseModel):
    """__doc__"""

    name: "StrFilterLookup | None" = None
    and_: "GroupFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "GroupFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "GroupFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class LayerFilter(BaseModel):
    """Layer(id, name, identifier, organization, logo, description, dns_probe, get_probe, kind)"""

    and_: "LayerFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "LayerFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "LayerFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ManifestInput(BaseModel):
    """No documentation"""

    identifier: str
    version: str
    title: str | None = None
    description: str | None = None
    logo: str | None = None
    scopes: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = None
    "Default: []"
    requirements: Annotated[
        tuple["RequirementInput", ...] | None, GraphQLDefault("[]")
    ] = None
    "Default: []"
    node_id: str | None = Field(
        validation_alias=AliasChoices("node_id", "nodeId"),
        serialization_alias="nodeId",
        default=None,
    )
    authors: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = None
    "Default: []"
    keywords: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = None
    "Default: []"
    license: str | None = None
    homepage: str | None = None
    repo_url: str | None = Field(
        validation_alias=AliasChoices("repo_url", "repoUrl"),
        serialization_alias="repoUrl",
        default=None,
    )
    public_sources: tuple["PublicSourceInput", ...] | None = Field(
        validation_alias=AliasChoices("public_sources", "publicSources"),
        serialization_alias="publicSources",
        default=None,
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class OffsetPaginationInput(BaseModel):
    """No documentation"""

    offset: Annotated[int | None, GraphQLDefault("0")] = None
    "Default: 0"
    limit: int | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class PublicSourceInput(BaseModel):
    """No documentation"""

    kind: PublicSourceKind
    url: str
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RedeemTokenFilter(BaseModel):
    """A redeem token is a token that can be used to redeem the rights to create
    a client. It is used to give the recipient the right to create a client.

    If the token is not redeemed within the expires_at time, it will be invalid.
    If the token has been redeemed, but the manifest has changed, the token will be invalid.
    """

    and_: "RedeemTokenFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "RedeemTokenFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "RedeemTokenFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RedeemTokenInput(BaseModel):
    """No documentation"""

    manifest: ManifestInput
    token: str | None = None
    expires_in_days: int | None = Field(
        validation_alias=AliasChoices("expires_in_days", "expiresInDays"),
        serialization_alias="expiresInDays",
        default=None,
    )
    max_redemptions: int | None = Field(
        validation_alias=AliasChoices("max_redemptions", "maxRedemptions"),
        serialization_alias="maxRedemptions",
        default=None,
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RequirementInput(BaseModel):
    """No documentation"""

    service: str
    optional: Annotated[bool | None, GraphQLDefault("False")] = None
    "Default: False"
    description: str | None = None
    key: str
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ServiceFilter(BaseModel):
    """Service(id, name, identifier, organization, logo, description)"""

    and_: "ServiceFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "ServiceFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "ServiceFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ServiceInstanceFilter(BaseModel):
    """ServiceInstance(id, hub, release, logo, instance_id, private_key, steward, organization, device, template, public_key, token)"""

    and_: "ServiceInstanceFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "ServiceInstanceFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "ServiceInstanceFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ServiceReleaseFilter(BaseModel):
    """ServiceRelease(id, service, version)"""

    and_: "ServiceReleaseFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "ServiceReleaseFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "ServiceReleaseFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StrFilterLookup(BaseModel):
    """No documentation"""

    exact: str | None = None
    i_exact: str | None = Field(
        validation_alias=AliasChoices("i_exact", "iExact"),
        serialization_alias="iExact",
        default=None,
    )
    contains: str | None = None
    i_contains: str | None = Field(
        validation_alias=AliasChoices("i_contains", "iContains"),
        serialization_alias="iContains",
        default=None,
    )
    in_list: tuple[str, ...] | None = Field(
        validation_alias=AliasChoices("in_list", "inList"),
        serialization_alias="inList",
        default=None,
    )
    gt: str | None = None
    gte: str | None = None
    lt: str | None = None
    lte: str | None = None
    starts_with: str | None = Field(
        validation_alias=AliasChoices("starts_with", "startsWith"),
        serialization_alias="startsWith",
        default=None,
    )
    i_starts_with: str | None = Field(
        validation_alias=AliasChoices("i_starts_with", "iStartsWith"),
        serialization_alias="iStartsWith",
        default=None,
    )
    ends_with: str | None = Field(
        validation_alias=AliasChoices("ends_with", "endsWith"),
        serialization_alias="endsWith",
        default=None,
    )
    i_ends_with: str | None = Field(
        validation_alias=AliasChoices("i_ends_with", "iEndsWith"),
        serialization_alias="iEndsWith",
        default=None,
    )
    range: tuple[str, ...] | None = None
    is_null: bool | None = Field(
        validation_alias=AliasChoices("is_null", "isNull"),
        serialization_alias="isNull",
        default=None,
    )
    regex: str | None = None
    i_regex: str | None = Field(
        validation_alias=AliasChoices("i_regex", "iRegex"),
        serialization_alias="iRegex",
        default=None,
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateGroupProfileInput(BaseModel):
    """No documentation"""

    id: ID
    name: str
    avatar: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateProfileInput(BaseModel):
    """No documentation"""

    id: ID
    name: str
    avatar: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateServiceInstanceInput(BaseModel):
    """No documentation"""

    allowed_users: tuple[ID, ...] | None = Field(
        validation_alias=AliasChoices("allowed_users", "allowedUsers"),
        serialization_alias="allowedUsers",
        default=None,
    )
    allowed_groups: tuple[ID, ...] | None = Field(
        validation_alias=AliasChoices("allowed_groups", "allowedGroups"),
        serialization_alias="allowedGroups",
        default=None,
    )
    denied_groups: tuple[ID, ...] | None = Field(
        validation_alias=AliasChoices("denied_groups", "deniedGroups"),
        serialization_alias="deniedGroups",
        default=None,
    )
    denied_users: tuple[ID, ...] | None = Field(
        validation_alias=AliasChoices("denied_users", "deniedUsers"),
        serialization_alias="deniedUsers",
        default=None,
    )
    id: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UserFilter(BaseModel):
    """A User of the System

    Lok Users are the main users of the system. They can be assigned to groups and have profiles, that can be used to display information about them.
    Each user is identifier by a unique username, and can have an email address associated with them.
    """

    username: StrFilterLookup | None = Field(
        default=None,
        description="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    and_: "UserFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "UserFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "UserFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ListAppLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class ListApp(BaseModel):
    """An App is the Arkitekt equivalent of a Software Application. It is a collection of `Releases` that can be all part of the same application. E.g the App `Napari` could have the releases `0.1.0` and `0.2.0`."""

    typename: Literal["App"] = Field(alias="__typename", default="App", exclude=True)
    id: ID
    identifier: str
    "The identifier of the app. This should be a globally unique string that identifies the app. We encourage you to use the reverse domain name notation. E.g. `com.example.myapp`"
    logo: ListAppLogo | None = Field(default=None)
    "The logo of the app. This should be a url to a logo that can be used to represent the app."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListApp"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}"
        name = "ListApp"
        type = "App"


class ListClientUser(BaseModel):
    """
    A User is a person that can log in to the system. They are uniquely identified by their username.
    And can have an email address associated with them (but don't have to).

    A user can be assigned to groups and has a profile that can be used to display information about them.
    Detail information about a user can be found in the profile.

    All users can have social accounts associated with them. These are used to authenticate the user with external services,
    such as ORCID or GitHub.
    """

    typename: Literal["User"] = Field(alias="__typename", default="User", exclude=True)
    id: ID
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    model_config = ConfigDict(frozen=True)


class ListClientReleaseLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class ListClientReleaseAppLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class ListClientReleaseApp(BaseModel):
    """An App is the Arkitekt equivalent of a Software Application. It is a collection of `Releases` that can be all part of the same application. E.g the App `Napari` could have the releases `0.1.0` and `0.2.0`."""

    typename: Literal["App"] = Field(alias="__typename", default="App", exclude=True)
    id: ID
    identifier: str
    "The identifier of the app. This should be a globally unique string that identifies the app. We encourage you to use the reverse domain name notation. E.g. `com.example.myapp`"
    logo: ListClientReleaseAppLogo | None = Field(default=None)
    "The logo of the app. This should be a url to a logo that can be used to represent the app."
    model_config = ConfigDict(frozen=True)


class ListClientRelease(BaseModel):
    """A Release is a version of an app. Releases might change over time. E.g. a release might be updated to fix a bug, and the release might be updated to add a new feature. This is why they are the home for `scopes` and `requirements`, which might change over the release cycle."""

    typename: Literal["Release"] = Field(
        alias="__typename", default="Release", exclude=True
    )
    version: str
    "The version of the release. This should be a string that identifies the version of the release. We enforce semantic versioning notation. E.g. `0.1.0`. The version is unique per app."
    logo: ListClientReleaseLogo | None = Field(default=None)
    "The logo of the release. This should be a url to a logo that can be used to represent the release."
    app: ListClientReleaseApp
    "The app that this release belongs to."
    model_config = ConfigDict(frozen=True)


class ListClient(BaseModel):
    """A client is a way of authenticating users with a release.
    The strategy of authentication is defined by the kind of client. And allows for different authentication flow.
    E.g a client can be a DESKTOP app, that might be used by multiple users, or a WEBSITE that wants to connect to a user's account,
    but also a DEVELOPMENT client that is used by a developer to test the app. The client model thinly wraps the oauth2 client model, which is used to authenticate users.
    """

    typename: Literal["Client"] = Field(
        alias="__typename", default="Client", exclude=True
    )
    id: ID
    user: ListClientUser | None = Field(default=None)
    "The user this client acts for (derived from its membership)."
    name: str
    "A human-readable label for the client that folds in the app, version, operator and device — e.g. `com.example.app:v0.1.1 by Johannes on my-laptop`."
    kind: ClientKind
    "What kind of principal this client is (its authentication strategy): DEVELOPMENT, WEBSITE, DESKTOP, MOBILE, HUB or RELYING_PARTY."
    release: ListClientRelease | None = Field(default=None)
    "The release that this client belongs to. Null for clients that are not bound to an app release (hub identities, relying parties, pending registrations)."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListClient"""

        document = "fragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
        name = "ListClient"
        type = "Client"


class PresignedPostCredentials(BaseModel):
    """Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)"""

    typename: Literal["PresignedPostCredentials"] = Field(
        alias="__typename", default="PresignedPostCredentials", exclude=True
    )
    x_amz_algorithm: str = Field(alias="xAmzAlgorithm")
    x_amz_credential: str = Field(alias="xAmzCredential")
    x_amz_date: str = Field(alias="xAmzDate")
    x_amz_signature: str = Field(alias="xAmzSignature")
    key: str
    bucket: str
    datalayer: str
    policy: str
    store: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for PresignedPostCredentials"""

        document = "fragment PresignedPostCredentials on PresignedPostCredentials {\n  xAmzAlgorithm\n  xAmzCredential\n  xAmzDate\n  xAmzSignature\n  key\n  bucket\n  datalayer\n  policy\n  store\n  __typename\n}"
        name = "PresignedPostCredentials"
        type = "PresignedPostCredentials"


class ListGroupProfileAvatar(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class ListGroupProfile(BaseModel):
    """
    A Profile of a Group. A GroupProfile can be used to display information about a group,
    such as a display name, a short bio and an avatar."""

    typename: Literal["GroupProfile"] = Field(
        alias="__typename", default="GroupProfile", exclude=True
    )
    id: ID
    bio: str | None = Field(default=None)
    "A short bio of the group"
    avatar: ListGroupProfileAvatar | None = Field(default=None)
    "The avatar of the group"
    model_config = ConfigDict(frozen=True)


class ListGroup(BaseModel):
    """
    A Group is the base unit of Role Based Access Control. A Group can have many users and many permissions. A user can have many groups. A user with a group that has a permission can perform the action that the permission allows.
    Groups are propagated to the respecting subservices. Permissions are not. Each subservice has to define its own permissions and mappings to groups.
    """

    typename: Literal["Group"] = Field(
        alias="__typename", default="Group", exclude=True
    )
    id: ID
    name: str
    profile: ListGroupProfile | None = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListGroup"""

        document = "fragment ListGroup on Group {\n  id\n  name\n  profile {\n    id\n    bio\n    avatar {\n      presignedUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
        name = "ListGroup"
        type = "Group"


class GroupProfileAvatar(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class GroupProfile(BaseModel):
    """
    A Profile of a Group. A GroupProfile can be used to display information about a group,
    such as a display name, a short bio and an avatar."""

    typename: Literal["GroupProfile"] = Field(
        alias="__typename", default="GroupProfile", exclude=True
    )
    id: ID
    name: str | None = Field(default=None)
    "The name of the group"
    avatar: GroupProfileAvatar | None = Field(default=None)
    "The avatar of the group"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for GroupProfile"""

        document = "fragment GroupProfile on GroupProfile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}"
        name = "GroupProfile"
        type = "GroupProfile"


class LayerLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class Layer(BaseModel):
    """A Layer is a network through which service instances can be reached (e.g. the public web, a tailnet, a VPN, or a docker network). Instance aliases are resolved relative to the layer they belong to."""

    typename: Literal["Layer"] = Field(
        alias="__typename", default="Layer", exclude=True
    )
    id: ID
    name: str
    "The name of the layer"
    identifier: str
    "The identifier of the layer. This should be a globally unique string that identifies the layer. We encourage you to use the reverse domain name notation. E.g. `com.example.mylayer`"
    description: str | None = Field(default=None)
    "The description of the layer. This should be a human readable description of the layer."
    logo: LayerLogo | None = Field(default=None)
    "The logo of the layer. This should be a url to a logo that can be used to represent the layer."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Layer"""

        document = "fragment Layer on Layer {\n  id\n  name\n  identifier\n  description\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}"
        name = "Layer"
        type = "Layer"


class ListLayerLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class ListLayer(BaseModel):
    """A Layer is a network through which service instances can be reached (e.g. the public web, a tailnet, a VPN, or a docker network). Instance aliases are resolved relative to the layer they belong to."""

    typename: Literal["Layer"] = Field(
        alias="__typename", default="Layer", exclude=True
    )
    id: ID
    name: str
    "The name of the layer"
    description: str | None = Field(default=None)
    "The description of the layer. This should be a human readable description of the layer."
    logo: ListLayerLogo | None = Field(default=None)
    "The logo of the layer. This should be a url to a logo that can be used to represent the layer."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListLayer"""

        document = "fragment ListLayer on Layer {\n  id\n  name\n  description\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}"
        name = "ListLayer"
        type = "Layer"


class ProfileAvatar(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class Profile(BaseModel):
    """
    A Profile of a User. A Profile can be used to display personalised information about a user,
    such as a display name, a short bio and an avatar."""

    typename: Literal["Profile"] = Field(
        alias="__typename", default="Profile", exclude=True
    )
    id: ID
    name: str | None = Field(default=None)
    "The name of the user"
    avatar: ProfileAvatar | None = Field(default=None)
    "The avatar of the user"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Profile"""

        document = "fragment Profile on Profile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}"
        name = "Profile"
        type = "Profile"


class ListRedeemTokenUser(BaseModel):
    """
    A User is a person that can log in to the system. They are uniquely identified by their username.
    And can have an email address associated with them (but don't have to).

    A user can be assigned to groups and has a profile that can be used to display information about them.
    Detail information about a user can be found in the profile.

    All users can have social accounts associated with them. These are used to authenticate the user with external services,
    such as ORCID or GitHub.
    """

    typename: Literal["User"] = Field(alias="__typename", default="User", exclude=True)
    id: ID
    email: str | None = Field(default=None)
    model_config = ConfigDict(frozen=True)


class ListRedeemTokenClientReleaseApp(BaseModel):
    """An App is the Arkitekt equivalent of a Software Application. It is a collection of `Releases` that can be all part of the same application. E.g the App `Napari` could have the releases `0.1.0` and `0.2.0`."""

    typename: Literal["App"] = Field(alias="__typename", default="App", exclude=True)
    identifier: str
    "The identifier of the app. This should be a globally unique string that identifies the app. We encourage you to use the reverse domain name notation. E.g. `com.example.myapp`"
    model_config = ConfigDict(frozen=True)


class ListRedeemTokenClientRelease(BaseModel):
    """A Release is a version of an app. Releases might change over time. E.g. a release might be updated to fix a bug, and the release might be updated to add a new feature. This is why they are the home for `scopes` and `requirements`, which might change over the release cycle."""

    typename: Literal["Release"] = Field(
        alias="__typename", default="Release", exclude=True
    )
    version: str
    "The version of the release. This should be a string that identifies the version of the release. We enforce semantic versioning notation. E.g. `0.1.0`. The version is unique per app."
    app: ListRedeemTokenClientReleaseApp
    "The app that this release belongs to."
    model_config = ConfigDict(frozen=True)


class ListRedeemTokenClient(BaseModel):
    """A client is a way of authenticating users with a release.
    The strategy of authentication is defined by the kind of client. And allows for different authentication flow.
    E.g a client can be a DESKTOP app, that might be used by multiple users, or a WEBSITE that wants to connect to a user's account,
    but also a DEVELOPMENT client that is used by a developer to test the app. The client model thinly wraps the oauth2 client model, which is used to authenticate users.
    """

    typename: Literal["Client"] = Field(
        alias="__typename", default="Client", exclude=True
    )
    id: ID
    release: ListRedeemTokenClientRelease | None = Field(default=None)
    "The release that this client belongs to. Null for clients that are not bound to an app release (hub identities, relying parties, pending registrations)."
    model_config = ConfigDict(frozen=True)


class ListRedeemToken(BaseModel):
    """A redeem token is a token that can be used to redeem the rights to create
    a client. It is used to give the recipient the right to create a client.

    If the token is not redeemed within the expires_at time, it will be invalid.
    If the token has been redeemed, but the manifest has changed, the token will be invalid.
    """

    typename: Literal["RedeemToken"] = Field(
        alias="__typename", default="RedeemToken", exclude=True
    )
    id: ID
    token: str
    "The token of the redeem token"
    user: ListRedeemTokenUser
    "The user that this redeem token belongs to."
    client: ListRedeemTokenClient | None = Field(default=None)
    "The client that this redeem token belongs to."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListRedeemToken"""

        document = "fragment ListRedeemToken on RedeemToken {\n  id\n  token\n  user {\n    id\n    email\n    __typename\n  }\n  client {\n    id\n    release {\n      version\n      app {\n        identifier\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
        name = "ListRedeemToken"
        type = "RedeemToken"


class DetailRedeemTokenUser(BaseModel):
    """
    A User is a person that can log in to the system. They are uniquely identified by their username.
    And can have an email address associated with them (but don't have to).

    A user can be assigned to groups and has a profile that can be used to display information about them.
    Detail information about a user can be found in the profile.

    All users can have social accounts associated with them. These are used to authenticate the user with external services,
    such as ORCID or GitHub.
    """

    typename: Literal["User"] = Field(alias="__typename", default="User", exclude=True)
    id: ID
    email: str | None = Field(default=None)
    model_config = ConfigDict(frozen=True)


class DetailRedeemTokenClientReleaseApp(BaseModel):
    """An App is the Arkitekt equivalent of a Software Application. It is a collection of `Releases` that can be all part of the same application. E.g the App `Napari` could have the releases `0.1.0` and `0.2.0`."""

    typename: Literal["App"] = Field(alias="__typename", default="App", exclude=True)
    identifier: str
    "The identifier of the app. This should be a globally unique string that identifies the app. We encourage you to use the reverse domain name notation. E.g. `com.example.myapp`"
    model_config = ConfigDict(frozen=True)


class DetailRedeemTokenClientRelease(BaseModel):
    """A Release is a version of an app. Releases might change over time. E.g. a release might be updated to fix a bug, and the release might be updated to add a new feature. This is why they are the home for `scopes` and `requirements`, which might change over the release cycle."""

    typename: Literal["Release"] = Field(
        alias="__typename", default="Release", exclude=True
    )
    version: str
    "The version of the release. This should be a string that identifies the version of the release. We enforce semantic versioning notation. E.g. `0.1.0`. The version is unique per app."
    app: DetailRedeemTokenClientReleaseApp
    "The app that this release belongs to."
    model_config = ConfigDict(frozen=True)


class DetailRedeemTokenClient(BaseModel):
    """A client is a way of authenticating users with a release.
    The strategy of authentication is defined by the kind of client. And allows for different authentication flow.
    E.g a client can be a DESKTOP app, that might be used by multiple users, or a WEBSITE that wants to connect to a user's account,
    but also a DEVELOPMENT client that is used by a developer to test the app. The client model thinly wraps the oauth2 client model, which is used to authenticate users.
    """

    typename: Literal["Client"] = Field(
        alias="__typename", default="Client", exclude=True
    )
    id: ID
    client_id: str = Field(alias="clientId")
    "The OAuth2 client id this client authenticates as."
    release: DetailRedeemTokenClientRelease | None = Field(default=None)
    "The release that this client belongs to. Null for clients that are not bound to an app release (hub identities, relying parties, pending registrations)."
    model_config = ConfigDict(frozen=True)


class DetailRedeemToken(BaseModel):
    """A redeem token is a token that can be used to redeem the rights to create
    a client. It is used to give the recipient the right to create a client.

    If the token is not redeemed within the expires_at time, it will be invalid.
    If the token has been redeemed, but the manifest has changed, the token will be invalid.
    """

    typename: Literal["RedeemToken"] = Field(
        alias="__typename", default="RedeemToken", exclude=True
    )
    id: ID
    token: str
    "The token of the redeem token"
    expires_at: datetime | None = Field(default=None, alias="expiresAt")
    "When this token stops being redeemable. Null means never."
    max_redemptions: int | None = Field(default=None, alias="maxRedemptions")
    "How many times this token may be redeemed. Null means unlimited."
    redemption_count: int = Field(alias="redemptionCount")
    "How many times this token has been redeemed so far."
    pinned_manifest: Any | None = Field(default=None, alias="pinnedManifest")
    "The manifest this token was pre-authorized for at mint time, or null for an unpinned token. A redeem must match its identifier, version and node_id exactly and may only request a subset of its scopes and requirements."
    user: DetailRedeemTokenUser
    "The user that this redeem token belongs to."
    client: DetailRedeemTokenClient | None = Field(default=None)
    "The client that this redeem token belongs to."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailRedeemToken"""

        document = "fragment DetailRedeemToken on RedeemToken {\n  id\n  token\n  expiresAt\n  maxRedemptions\n  redemptionCount\n  pinnedManifest\n  user {\n    id\n    email\n    __typename\n  }\n  client {\n    id\n    clientId\n    release {\n      version\n      app {\n        identifier\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
        name = "DetailRedeemToken"
        type = "RedeemToken"


class ServiceLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class Service(BaseModel):
    """A Service is a Webservice that a Client might want to access. It is not the configured instance of the service, but the service itself."""

    typename: Literal["Service"] = Field(
        alias="__typename", default="Service", exclude=True
    )
    identifier: str
    "The identifier of the service. This should be a globally unique string that identifies the service. We encourage you to use the reverse domain name notation. E.g. `com.example.myservice`"
    id: ID
    name: str
    "The name of the service"
    logo: ServiceLogo | None = Field(default=None)
    "The logo of the service. This should be a url to a logo that can be used to represent the service."
    description: str | None = Field(default=None)
    "The description of the service. This should be a human readable description of the service."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Service"""

        document = "fragment Service on Service {\n  identifier\n  id\n  name\n  logo {\n    presignedUrl\n    __typename\n  }\n  description\n  __typename\n}"
        name = "Service"
        type = "Service"


class ListServiceReleaseService(BaseModel):
    """A Service is a Webservice that a Client might want to access. It is not the configured instance of the service, but the service itself."""

    typename: Literal["Service"] = Field(
        alias="__typename", default="Service", exclude=True
    )
    id: ID
    name: str
    "The name of the service"
    model_config = ConfigDict(frozen=True)


class ListServiceRelease(BaseModel):
    """A ServiceRelease is a specific release of a Service. It contains the configuration for a particular version of the service."""

    typename: Literal["ServiceRelease"] = Field(
        alias="__typename", default="ServiceRelease", exclude=True
    )
    id: ID
    service: ListServiceReleaseService
    "The service that this release belongs to."
    version: str
    "The version of the service. This should be a human readable version string."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListServiceRelease"""

        document = "fragment ListServiceRelease on ServiceRelease {\n  id\n  service {\n    id\n    name\n    __typename\n  }\n  version\n  __typename\n}"
        name = "ListServiceRelease"
        type = "ServiceRelease"


class ListUser(BaseModel):
    """
    A User is a person that can log in to the system. They are uniquely identified by their username.
    And can have an email address associated with them (but don't have to).

    A user can be assigned to groups and has a profile that can be used to display information about them.
    Detail information about a user can be found in the profile.

    All users can have social accounts associated with them. These are used to authenticate the user with external services,
    such as ORCID or GitHub.
    """

    typename: Literal["User"] = Field(alias="__typename", default="User", exclude=True)
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    email: str | None = Field(default=None)
    avatar: str | None = Field(default=None)
    id: ID
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListUser"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}"
        name = "ListUser"
        type = "User"


class MeUser(BaseModel):
    """
    A User is a person that can log in to the system. They are uniquely identified by their username.
    And can have an email address associated with them (but don't have to).

    A user can be assigned to groups and has a profile that can be used to display information about them.
    Detail information about a user can be found in the profile.

    All users can have social accounts associated with them. These are used to authenticate the user with external services,
    such as ORCID or GitHub.
    """

    typename: Literal["User"] = Field(alias="__typename", default="User", exclude=True)
    id: ID
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    email: str | None = Field(default=None)
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    avatar: str | None = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MeUser"""

        document = "fragment MeUser on User {\n  id\n  username\n  email\n  firstName\n  lastName\n  avatar\n  __typename\n}"
        name = "MeUser"
        type = "User"


class ListReleaseLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class ListRelease(BaseModel):
    """A Release is a version of an app. Releases might change over time. E.g. a release might be updated to fix a bug, and the release might be updated to add a new feature. This is why they are the home for `scopes` and `requirements`, which might change over the release cycle."""

    typename: Literal["Release"] = Field(
        alias="__typename", default="Release", exclude=True
    )
    id: ID
    version: str
    "The version of the release. This should be a string that identifies the version of the release. We enforce semantic versioning notation. E.g. `0.1.0`. The version is unique per app."
    logo: ListReleaseLogo | None = Field(default=None)
    "The logo of the release. This should be a url to a logo that can be used to represent the release."
    app: ListApp
    "The app that this release belongs to."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListRelease"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}"
        name = "ListRelease"
        type = "Release"


class DetailReleaseLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class DetailRelease(BaseModel):
    """A Release is a version of an app. Releases might change over time. E.g. a release might be updated to fix a bug, and the release might be updated to add a new feature. This is why they are the home for `scopes` and `requirements`, which might change over the release cycle."""

    typename: Literal["Release"] = Field(
        alias="__typename", default="Release", exclude=True
    )
    id: ID
    version: str
    "The version of the release. This should be a string that identifies the version of the release. We enforce semantic versioning notation. E.g. `0.1.0`. The version is unique per app."
    logo: DetailReleaseLogo | None = Field(default=None)
    "The logo of the release. This should be a url to a logo that can be used to represent the release."
    app: ListApp
    "The app that this release belongs to."
    clients: tuple[ListClient, ...]
    "The clients of the release"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailRelease"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment DetailRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  clients {\n    ...ListClient\n    __typename\n  }\n  __typename\n}"
        name = "DetailRelease"
        type = "Release"


class DetailUserGroups(BaseModel):
    """
    A Group is the base unit of Role Based Access Control. A Group can have many users and many permissions. A user can have many groups. A user with a group that has a permission can perform the action that the permission allows.
    Groups are propagated to the respecting subservices. Permissions are not. Each subservice has to define its own permissions and mappings to groups.
    """

    typename: Literal["Group"] = Field(
        alias="__typename", default="Group", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class DetailUser(BaseModel):
    """
    A User is a person that can log in to the system. They are uniquely identified by their username.
    And can have an email address associated with them (but don't have to).

    A user can be assigned to groups and has a profile that can be used to display information about them.
    Detail information about a user can be found in the profile.

    All users can have social accounts associated with them. These are used to authenticate the user with external services,
    such as ORCID or GitHub.
    """

    typename: Literal["User"] = Field(alias="__typename", default="User", exclude=True)
    id: ID
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    email: str | None = Field(default=None)
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    avatar: str | None = Field(default=None)
    groups: tuple[DetailUserGroups, ...]
    "The groups this user belongs to. A user will get all permissions granted to each of their groups."
    profile: Profile
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailUser"""

        document = "fragment Profile on Profile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment DetailUser on User {\n  id\n  username\n  email\n  firstName\n  lastName\n  avatar\n  groups {\n    id\n    name\n    __typename\n  }\n  profile {\n    ...Profile\n    __typename\n  }\n  __typename\n}"
        name = "DetailUser"
        type = "User"


class ListService(BaseModel):
    """A Service is a Webservice that a Client might want to access. It is not the configured instance of the service, but the service itself."""

    typename: Literal["Service"] = Field(
        alias="__typename", default="Service", exclude=True
    )
    identifier: str
    "The identifier of the service. This should be a globally unique string that identifies the service. We encourage you to use the reverse domain name notation. E.g. `com.example.myservice`"
    id: ID
    name: str
    "The name of the service"
    releases: tuple[ListServiceRelease, ...]
    "The releases of the service. A service release is a specific version of a service. It will be configured by a configuration backend and will be used to send to the client as a configuration. It should never contain sensitive information."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListService"""

        document = "fragment ListServiceRelease on ServiceRelease {\n  id\n  service {\n    id\n    name\n    __typename\n  }\n  version\n  __typename\n}\n\nfragment ListService on Service {\n  identifier\n  id\n  name\n  releases {\n    ...ListServiceRelease\n    __typename\n  }\n  __typename\n}"
        name = "ListService"
        type = "Service"


class DetailGroup(BaseModel):
    """
    A Group is the base unit of Role Based Access Control. A Group can have many users and many permissions. A user can have many groups. A user with a group that has a permission can perform the action that the permission allows.
    Groups are propagated to the respecting subservices. Permissions are not. Each subservice has to define its own permissions and mappings to groups.
    """

    typename: Literal["Group"] = Field(
        alias="__typename", default="Group", exclude=True
    )
    id: ID
    name: str
    users: tuple[ListUser, ...]
    "The users that are in the group"
    profile: GroupProfile | None = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailGroup"""

        document = "fragment GroupProfile on GroupProfile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment DetailGroup on Group {\n  id\n  name\n  users {\n    ...ListUser\n    __typename\n  }\n  profile {\n    ...GroupProfile\n    __typename\n  }\n  __typename\n}"
        name = "DetailGroup"
        type = "Group"


class ListServiceInstance(BaseModel):
    """A ServiceInstance is a configured instance of a Service. It will be configured by a configuration backend and will be used to send to the client as a configuration. It should never contain sensitive information."""

    typename: Literal["ServiceInstance"] = Field(
        alias="__typename", default="ServiceInstance", exclude=True
    )
    id: ID
    instance_id: ID = Field(alias="instanceId")
    "The instance id of the instance. This is a unique string that identifies the instance. It is used to identify the instance in the code and in the database."
    allowed_users: tuple[ListUser, ...] = Field(alias="allowedUsers")
    "The users that are allowed to use this instance."
    denied_users: tuple[ListUser, ...] = Field(alias="deniedUsers")
    "The users that are denied to use this instance."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListServiceInstance"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}"
        name = "ListServiceInstance"
        type = "ServiceInstance"


class DetailAppLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class DetailApp(BaseModel):
    """An App is the Arkitekt equivalent of a Software Application. It is a collection of `Releases` that can be all part of the same application. E.g the App `Napari` could have the releases `0.1.0` and `0.2.0`."""

    typename: Literal["App"] = Field(alias="__typename", default="App", exclude=True)
    id: ID
    identifier: str
    "The identifier of the app. This should be a globally unique string that identifies the app. We encourage you to use the reverse domain name notation. E.g. `com.example.myapp`"
    logo: DetailAppLogo | None = Field(default=None)
    "The logo of the app. This should be a url to a logo that can be used to represent the app."
    releases: tuple[ListRelease, ...]
    "The releases of the app. A release is a version of the app that can be installed by a user."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailApp"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}\n\nfragment DetailApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  releases {\n    ...ListRelease\n    __typename\n  }\n  __typename\n}"
        name = "DetailApp"
        type = "App"


class ServiceReleaseService(BaseModel):
    """A Service is a Webservice that a Client might want to access. It is not the configured instance of the service, but the service itself."""

    typename: Literal["Service"] = Field(
        alias="__typename", default="Service", exclude=True
    )
    id: ID
    name: str
    "The name of the service"
    model_config = ConfigDict(frozen=True)


class ServiceRelease(BaseModel):
    """A ServiceRelease is a specific release of a Service. It contains the configuration for a particular version of the service."""

    typename: Literal["ServiceRelease"] = Field(
        alias="__typename", default="ServiceRelease", exclude=True
    )
    id: ID
    service: ServiceReleaseService
    "The service that this release belongs to."
    version: str
    "The version of the service. This should be a human readable version string."
    instances: tuple[ListServiceInstance, ...]
    "The instances of the service. A service instance is a configured instance of a service. It will be configured by a configuration backend and will be used to send to the client as a configuration. It should never contain sensitive information."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ServiceRelease"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ServiceRelease on ServiceRelease {\n  id\n  service {\n    id\n    name\n    __typename\n  }\n  version\n  instances {\n    ...ListServiceInstance\n    __typename\n  }\n  __typename\n}"
        name = "ServiceRelease"
        type = "ServiceRelease"


class ListServiceInstanceMapping(BaseModel):
    """A ServiceInstanceMapping binds one of a client's requirements (by key) to the ServiceInstance that fulfils it. The set of mappings of a client is its composed configuration."""

    typename: Literal["ServiceInstanceMapping"] = Field(
        alias="__typename", default="ServiceInstanceMapping", exclude=True
    )
    id: ID
    key: str
    "The requirement key of the client that this mapping fulfils. Unique per client."
    instance: ListServiceInstance
    "The service instance this requirement is mapped to."
    client: ListClient
    "The client whose requirement this mapping fulfils."
    optional: bool
    "Is this mapping optional? If a mapping is optional, you can configure the client without this mapping."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListServiceInstanceMapping"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}"
        name = "ListServiceInstanceMapping"
        type = "ServiceInstanceMapping"


class DetailClientUser(BaseModel):
    """
    A User is a person that can log in to the system. They are uniquely identified by their username.
    And can have an email address associated with them (but don't have to).

    A user can be assigned to groups and has a profile that can be used to display information about them.
    Detail information about a user can be found in the profile.

    All users can have social accounts associated with them. These are used to authenticate the user with external services,
    such as ORCID or GitHub.
    """

    typename: Literal["User"] = Field(alias="__typename", default="User", exclude=True)
    id: ID
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    model_config = ConfigDict(frozen=True)


class DetailClientLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class DetailClient(BaseModel):
    """A client is a way of authenticating users with a release.
    The strategy of authentication is defined by the kind of client. And allows for different authentication flow.
    E.g a client can be a DESKTOP app, that might be used by multiple users, or a WEBSITE that wants to connect to a user's account,
    but also a DEVELOPMENT client that is used by a developer to test the app. The client model thinly wraps the oauth2 client model, which is used to authenticate users.
    """

    typename: Literal["Client"] = Field(
        alias="__typename", default="Client", exclude=True
    )
    id: ID
    name: str
    "A human-readable label for the client that folds in the app, version, operator and device — e.g. `com.example.app:v0.1.1 by Johannes on my-laptop`."
    client_id: str = Field(alias="clientId")
    "The OAuth2 client id this client authenticates as."
    user: DetailClientUser | None = Field(default=None)
    "The user this client acts for (derived from its membership)."
    kind: ClientKind
    "What kind of principal this client is (its authentication strategy): DEVELOPMENT, WEBSITE, DESKTOP, MOBILE, HUB or RELYING_PARTY."
    release: ListRelease | None = Field(default=None)
    "The release that this client belongs to. Null for clients that are not bound to an app release (hub identities, relying parties, pending registrations)."
    logo: DetailClientLogo | None = Field(default=None)
    "The logo of the release. This should be a url to a logo that can be used to represent the release."
    mappings: tuple[ListServiceInstanceMapping, ...]
    "The mappings of the client. A mapping is a mapping of a service to a service instance. This is used to configure the hub."
    issue_url: str | None = Field(default=None, alias="issueUrl")
    "The issue url of the client. This is the url where users can report issues and get more information about the client."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailClient"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}\n\nfragment DetailClient on Client {\n  id\n  name\n  clientId\n  user {\n    id\n    username\n    __typename\n  }\n  kind\n  release {\n    ...ListRelease\n    __typename\n  }\n  logo {\n    presignedUrl\n    __typename\n  }\n  mappings {\n    ...ListServiceInstanceMapping\n    __typename\n  }\n  issueUrl\n  __typename\n}"
        name = "DetailClient"
        type = "Client"


class ServiceInstanceReleaseService(BaseModel):
    """A Service is a Webservice that a Client might want to access. It is not the configured instance of the service, but the service itself."""

    typename: Literal["Service"] = Field(
        alias="__typename", default="Service", exclude=True
    )
    id: ID
    identifier: str
    "The identifier of the service. This should be a globally unique string that identifies the service. We encourage you to use the reverse domain name notation. E.g. `com.example.myservice`"
    model_config = ConfigDict(frozen=True)


class ServiceInstanceRelease(BaseModel):
    """A ServiceRelease is a specific release of a Service. It contains the configuration for a particular version of the service."""

    typename: Literal["ServiceRelease"] = Field(
        alias="__typename", default="ServiceRelease", exclude=True
    )
    version: str
    "The version of the service. This should be a human readable version string."
    service: ServiceInstanceReleaseService
    "The service that this release belongs to."
    model_config = ConfigDict(frozen=True)


class ServiceInstanceLogo(BaseModel):
    """Small helper around S3-backed stored objects.

    Provides convenience helpers for generating presigned URLs and
    uploading content."""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    presigned_url: str = Field(alias="presignedUrl")
    model_config = ConfigDict(frozen=True)


class ServiceInstance(BaseModel):
    """A ServiceInstance is a configured instance of a Service. It will be configured by a configuration backend and will be used to send to the client as a configuration. It should never contain sensitive information."""

    typename: Literal["ServiceInstance"] = Field(
        alias="__typename", default="ServiceInstance", exclude=True
    )
    id: ID
    instance_id: ID = Field(alias="instanceId")
    "The instance id of the instance. This is a unique string that identifies the instance. It is used to identify the instance in the code and in the database."
    release: ServiceInstanceRelease
    "The service release that this instance belongs to."
    allowed_users: tuple[ListUser, ...] = Field(alias="allowedUsers")
    "The users that are allowed to use this instance."
    denied_users: tuple[ListUser, ...] = Field(alias="deniedUsers")
    "The users that are denied to use this instance."
    allowed_groups: tuple[ListGroup, ...] = Field(alias="allowedGroups")
    "The groups that are allowed to use this instance."
    denied_groups: tuple[ListGroup, ...] = Field(alias="deniedGroups")
    "The groups that are denied to use this instance."
    mappings: tuple[ListServiceInstanceMapping, ...]
    "The mappings of the hub. A mapping is a mapping of a service to a service instance. This is used to configure the hub."
    logo: ServiceInstanceLogo | None = Field(default=None)
    "The logo of the app. This should be a url to a logo that can be used to represent the app."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ServiceInstance"""

        document = "fragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListGroup on Group {\n  id\n  name\n  profile {\n    id\n    bio\n    avatar {\n      presignedUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}\n\nfragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ServiceInstance on ServiceInstance {\n  id\n  instanceId\n  release {\n    version\n    service {\n      id\n      identifier\n      __typename\n    }\n    __typename\n  }\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  allowedGroups {\n    ...ListGroup\n    __typename\n  }\n  deniedGroups {\n    ...ListGroup\n    __typename\n  }\n  mappings {\n    ...ListServiceInstanceMapping\n    __typename\n  }\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}"
        name = "ServiceInstance"
        type = "ServiceInstance"


class CreateClientMutation(BaseModel):
    """No documentation found for this operation."""

    create_developmental_client: DetailClient = Field(alias="createDevelopmentalClient")

    class Arguments(BaseModel):
        """Arguments for CreateClient"""

        input: DevelopmentClientInput

    class Meta:
        """Meta class for CreateClient"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}\n\nfragment DetailClient on Client {\n  id\n  name\n  clientId\n  user {\n    id\n    username\n    __typename\n  }\n  kind\n  release {\n    ...ListRelease\n    __typename\n  }\n  logo {\n    presignedUrl\n    __typename\n  }\n  mappings {\n    ...ListServiceInstanceMapping\n    __typename\n  }\n  issueUrl\n  __typename\n}\n\nmutation CreateClient($input: DevelopmentClientInput!) {\n  createDevelopmentalClient(input: $input) {\n    ...DetailClient\n    __typename\n  }\n}"


class CreateGroupProfileMutation(BaseModel):
    """No documentation found for this operation."""

    create_group_profile: GroupProfile = Field(alias="createGroupProfile")

    class Arguments(BaseModel):
        """Arguments for CreateGroupProfile"""

        input: CreateGroupProfileInput

    class Meta:
        """Meta class for CreateGroupProfile"""

        document = "fragment GroupProfile on GroupProfile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nmutation CreateGroupProfile($input: CreateGroupProfileInput!) {\n  createGroupProfile(input: $input) {\n    ...GroupProfile\n    __typename\n  }\n}"


class UpdateGroupProfileMutation(BaseModel):
    """No documentation found for this operation."""

    update_group_profile: GroupProfile = Field(alias="updateGroupProfile")

    class Arguments(BaseModel):
        """Arguments for UpdateGroupProfile"""

        input: UpdateGroupProfileInput

    class Meta:
        """Meta class for UpdateGroupProfile"""

        document = "fragment GroupProfile on GroupProfile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateGroupProfile($input: UpdateGroupProfileInput!) {\n  updateGroupProfile(input: $input) {\n    ...GroupProfile\n    __typename\n  }\n}"


class UpdateServiceInstanceMutation(BaseModel):
    """No documentation found for this operation."""

    update_service_instance: ServiceInstance = Field(alias="updateServiceInstance")

    class Arguments(BaseModel):
        """Arguments for UpdateServiceInstance"""

        input: UpdateServiceInstanceInput

    class Meta:
        """Meta class for UpdateServiceInstance"""

        document = "fragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListGroup on Group {\n  id\n  name\n  profile {\n    id\n    bio\n    avatar {\n      presignedUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}\n\nfragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ServiceInstance on ServiceInstance {\n  id\n  instanceId\n  release {\n    version\n    service {\n      id\n      identifier\n      __typename\n    }\n    __typename\n  }\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  allowedGroups {\n    ...ListGroup\n    __typename\n  }\n  deniedGroups {\n    ...ListGroup\n    __typename\n  }\n  mappings {\n    ...ListServiceInstanceMapping\n    __typename\n  }\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateServiceInstance($input: UpdateServiceInstanceInput!) {\n  updateServiceInstance(input: $input) {\n    ...ServiceInstance\n    __typename\n  }\n}"


class CreateServiceInstanceMutation(BaseModel):
    """No documentation found for this operation."""

    create_service_instance: ServiceInstance = Field(alias="createServiceInstance")

    class Arguments(BaseModel):
        """Arguments for CreateServiceInstance"""

        input: CreateServiceInstanceInput

    class Meta:
        """Meta class for CreateServiceInstance"""

        document = "fragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListGroup on Group {\n  id\n  name\n  profile {\n    id\n    bio\n    avatar {\n      presignedUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}\n\nfragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ServiceInstance on ServiceInstance {\n  id\n  instanceId\n  release {\n    version\n    service {\n      id\n      identifier\n      __typename\n    }\n    __typename\n  }\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  allowedGroups {\n    ...ListGroup\n    __typename\n  }\n  deniedGroups {\n    ...ListGroup\n    __typename\n  }\n  mappings {\n    ...ListServiceInstanceMapping\n    __typename\n  }\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nmutation CreateServiceInstance($input: CreateServiceInstanceInput!) {\n  createServiceInstance(input: $input) {\n    ...ServiceInstance\n    __typename\n  }\n}"


class CreateUserProfileMutation(BaseModel):
    """No documentation found for this operation."""

    create_profile: Profile = Field(alias="createProfile")

    class Arguments(BaseModel):
        """Arguments for CreateUserProfile"""

        input: CreateProfileInput

    class Meta:
        """Meta class for CreateUserProfile"""

        document = "fragment Profile on Profile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nmutation CreateUserProfile($input: CreateProfileInput!) {\n  createProfile(input: $input) {\n    ...Profile\n    __typename\n  }\n}"


class UpdateUserProfileMutation(BaseModel):
    """No documentation found for this operation."""

    update_profile: Profile = Field(alias="updateProfile")

    class Arguments(BaseModel):
        """Arguments for UpdateUserProfile"""

        input: UpdateProfileInput

    class Meta:
        """Meta class for UpdateUserProfile"""

        document = "fragment Profile on Profile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateUserProfile($input: UpdateProfileInput!) {\n  updateProfile(input: $input) {\n    ...Profile\n    __typename\n  }\n}"


class CreateRedeemTokenMutation(BaseModel):
    """No documentation found for this operation."""

    create_redeem_token: DetailRedeemToken = Field(alias="createRedeemToken")

    class Arguments(BaseModel):
        """Arguments for CreateRedeemToken"""

        input: RedeemTokenInput

    class Meta:
        """Meta class for CreateRedeemToken"""

        document = "fragment DetailRedeemToken on RedeemToken {\n  id\n  token\n  expiresAt\n  maxRedemptions\n  redemptionCount\n  pinnedManifest\n  user {\n    id\n    email\n    __typename\n  }\n  client {\n    id\n    clientId\n    release {\n      version\n      app {\n        identifier\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation CreateRedeemToken($input: RedeemTokenInput!) {\n  createRedeemToken(input: $input) {\n    ...DetailRedeemToken\n    __typename\n  }\n}"


class DeleteRedeemTokenMutation(BaseModel):
    """No documentation found for this operation."""

    delete_redeem_token: ID = Field(alias="deleteRedeemToken")

    class Arguments(BaseModel):
        """Arguments for DeleteRedeemToken"""

        id: ID

    class Meta:
        """Meta class for DeleteRedeemToken"""

        document = "mutation DeleteRedeemToken($id: ID!) {\n  deleteRedeemToken(input: {id: $id})\n}"


class RequestMediaUploadMutation(BaseModel):
    """No documentation found for this operation."""

    request_media_upload: PresignedPostCredentials = Field(alias="requestMediaUpload")

    class Arguments(BaseModel):
        """Arguments for RequestMediaUpload"""

        key: str
        datalayer: str

    class Meta:
        """Meta class for RequestMediaUpload"""

        document = "fragment PresignedPostCredentials on PresignedPostCredentials {\n  xAmzAlgorithm\n  xAmzCredential\n  xAmzDate\n  xAmzSignature\n  key\n  bucket\n  datalayer\n  policy\n  store\n  __typename\n}\n\nmutation RequestMediaUpload($key: String!, $datalayer: String!) {\n  requestMediaUpload(input: {key: $key, datalayer: $datalayer}) {\n    ...PresignedPostCredentials\n    __typename\n  }\n}"


class AppsQuery(BaseModel):
    """No documentation found for this operation."""

    apps: tuple[ListApp, ...]

    class Arguments(BaseModel):
        """Arguments for Apps"""

        filters: AppFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for Apps"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nquery Apps($filters: AppFilter, $pagination: OffsetPaginationInput) {\n  apps(filters: $filters, pagination: $pagination) {\n    ...ListApp\n    __typename\n  }\n}"


class AppQuery(BaseModel):
    """No documentation found for this operation."""

    app: DetailApp

    class Arguments(BaseModel):
        """Arguments for App"""

        identifier: str | None = Field(default=None)
        id: ID | None = Field(default=None)
        client_id: ID | None = Field(
            validation_alias=AliasChoices("client_id", "clientId"),
            serialization_alias="clientId",
            default=None,
        )

    class Meta:
        """Meta class for App"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}\n\nfragment DetailApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  releases {\n    ...ListRelease\n    __typename\n  }\n  __typename\n}\n\nquery App($identifier: AppIdentifier, $id: ID, $clientId: ID) {\n  app(identifier: $identifier, id: $id, clientId: $clientId) {\n    ...DetailApp\n    __typename\n  }\n}"


class DetailAppQuery(BaseModel):
    """No documentation found for this operation."""

    app: DetailApp

    class Arguments(BaseModel):
        """Arguments for DetailApp"""

        id: ID

    class Meta:
        """Meta class for DetailApp"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}\n\nfragment DetailApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  releases {\n    ...ListRelease\n    __typename\n  }\n  __typename\n}\n\nquery DetailApp($id: ID!) {\n  app(id: $id) {\n    ...DetailApp\n    __typename\n  }\n}"


class ClientsQuery(BaseModel):
    """No documentation found for this operation."""

    clients: tuple[ListClient, ...]

    class Arguments(BaseModel):
        """Arguments for Clients"""

        filters: ClientFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for Clients"""

        document = "fragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery Clients($filters: ClientFilter, $pagination: OffsetPaginationInput) {\n  clients(filters: $filters, pagination: $pagination) {\n    ...ListClient\n    __typename\n  }\n}"


class DetailClientQuery(BaseModel):
    """No documentation found for this operation."""

    client: DetailClient

    class Arguments(BaseModel):
        """Arguments for DetailClient"""

        id: ID

    class Meta:
        """Meta class for DetailClient"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}\n\nfragment DetailClient on Client {\n  id\n  name\n  clientId\n  user {\n    id\n    username\n    __typename\n  }\n  kind\n  release {\n    ...ListRelease\n    __typename\n  }\n  logo {\n    presignedUrl\n    __typename\n  }\n  mappings {\n    ...ListServiceInstanceMapping\n    __typename\n  }\n  issueUrl\n  __typename\n}\n\nquery DetailClient($id: ID!) {\n  client(id: $id) {\n    ...DetailClient\n    __typename\n  }\n}"


class MyManagedClientsQuery(BaseModel):
    """No documentation found for this operation."""

    my_managed_clients: tuple[ListClient, ...] = Field(alias="myManagedClients")

    class Arguments(BaseModel):
        """Arguments for MyManagedClients"""

        kind: ClientKind

    class Meta:
        """Meta class for MyManagedClients"""

        document = "fragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery MyManagedClients($kind: ClientKind!) {\n  myManagedClients(kind: $kind) {\n    ...ListClient\n    __typename\n  }\n}"


class ClientQuery(BaseModel):
    """No documentation found for this operation."""

    client: DetailClient

    class Arguments(BaseModel):
        """Arguments for Client"""

        client_id: ID = Field(
            validation_alias=AliasChoices("client_id", "clientId"),
            serialization_alias="clientId",
        )

    class Meta:
        """Meta class for Client"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}\n\nfragment DetailClient on Client {\n  id\n  name\n  clientId\n  user {\n    id\n    username\n    __typename\n  }\n  kind\n  release {\n    ...ListRelease\n    __typename\n  }\n  logo {\n    presignedUrl\n    __typename\n  }\n  mappings {\n    ...ListServiceInstanceMapping\n    __typename\n  }\n  issueUrl\n  __typename\n}\n\nquery Client($clientId: ID!) {\n  client(clientId: $clientId) {\n    ...DetailClient\n    __typename\n  }\n}"


class GroupOptionsQueryOptions(BaseModel):
    """
    A Group is the base unit of Role Based Access Control. A Group can have many users and many permissions. A user can have many groups. A user with a group that has a permission can perform the action that the permission allows.
    Groups are propagated to the respecting subservices. Permissions are not. Each subservice has to define its own permissions and mappings to groups.
    """

    typename: Literal["Group"] = Field(
        alias="__typename", default="Group", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class GroupOptionsQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[GroupOptionsQueryOptions, ...]

    class Arguments(BaseModel):
        """Arguments for GroupOptions"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for GroupOptions"""

        document = "query GroupOptions($search: String, $values: [ID!]) {\n  options: groups(filters: {search: $search, ids: $values}) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class DetailGroupQuery(BaseModel):
    """No documentation found for this operation."""

    group: DetailGroup

    class Arguments(BaseModel):
        """Arguments for DetailGroup"""

        id: ID

    class Meta:
        """Meta class for DetailGroup"""

        document = "fragment GroupProfile on GroupProfile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment DetailGroup on Group {\n  id\n  name\n  users {\n    ...ListUser\n    __typename\n  }\n  profile {\n    ...GroupProfile\n    __typename\n  }\n  __typename\n}\n\nquery DetailGroup($id: ID!) {\n  group(id: $id) {\n    ...DetailGroup\n    __typename\n  }\n}"


class GroupsQuery(BaseModel):
    """No documentation found for this operation."""

    groups: tuple[ListGroup, ...]

    class Arguments(BaseModel):
        """Arguments for Groups"""

        filters: GroupFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for Groups"""

        document = "fragment ListGroup on Group {\n  id\n  name\n  profile {\n    id\n    bio\n    avatar {\n      presignedUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery Groups($filters: GroupFilter, $pagination: OffsetPaginationInput) {\n  groups(filters: $filters, pagination: $pagination) {\n    ...ListGroup\n    __typename\n  }\n}"


class LayersQuery(BaseModel):
    """No documentation found for this operation."""

    layers: tuple[ListLayer, ...]

    class Arguments(BaseModel):
        """Arguments for Layers"""

        filters: LayerFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for Layers"""

        document = "fragment ListLayer on Layer {\n  id\n  name\n  description\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nquery Layers($filters: LayerFilter, $pagination: OffsetPaginationInput) {\n  layers(filters: $filters, pagination: $pagination) {\n    ...ListLayer\n    __typename\n  }\n}"


class DetailLayerQuery(BaseModel):
    """No documentation found for this operation."""

    layer: Layer

    class Arguments(BaseModel):
        """Arguments for DetailLayer"""

        id: ID

    class Meta:
        """Meta class for DetailLayer"""

        document = "fragment Layer on Layer {\n  id\n  name\n  identifier\n  description\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nquery DetailLayer($id: ID!) {\n  layer(id: $id) {\n    ...Layer\n    __typename\n  }\n}"


class RedeemTokenQuery(BaseModel):
    """No documentation found for this operation."""

    redeem_token: DetailRedeemToken = Field(alias="redeemToken")

    class Arguments(BaseModel):
        """Arguments for RedeemToken"""

        id: ID

    class Meta:
        """Meta class for RedeemToken"""

        document = "fragment DetailRedeemToken on RedeemToken {\n  id\n  token\n  expiresAt\n  maxRedemptions\n  redemptionCount\n  pinnedManifest\n  user {\n    id\n    email\n    __typename\n  }\n  client {\n    id\n    clientId\n    release {\n      version\n      app {\n        identifier\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery RedeemToken($id: ID!) {\n  redeemToken(id: $id) {\n    ...DetailRedeemToken\n    __typename\n  }\n}"


class RedeemTokensQuery(BaseModel):
    """No documentation found for this operation."""

    redeem_tokens: tuple[ListRedeemToken, ...] = Field(alias="redeemTokens")

    class Arguments(BaseModel):
        """Arguments for RedeemTokens"""

        filters: RedeemTokenFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for RedeemTokens"""

        document = "fragment ListRedeemToken on RedeemToken {\n  id\n  token\n  user {\n    id\n    email\n    __typename\n  }\n  client {\n    id\n    release {\n      version\n      app {\n        identifier\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery RedeemTokens($filters: RedeemTokenFilter, $pagination: OffsetPaginationInput) {\n  redeemTokens(filters: $filters, pagination: $pagination) {\n    ...ListRedeemToken\n    __typename\n  }\n}"


class ReleasesQuery(BaseModel):
    """No documentation found for this operation."""

    releases: tuple[ListRelease, ...]

    class Arguments(BaseModel):
        """Arguments for Releases"""

        pass

    class Meta:
        """Meta class for Releases"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  __typename\n}\n\nquery Releases {\n  releases {\n    ...ListRelease\n    __typename\n  }\n}"


class ReleaseQuery(BaseModel):
    """No documentation found for this operation."""

    release: DetailRelease

    class Arguments(BaseModel):
        """Arguments for Release"""

        identifier: str | None = Field(default=None)
        version: str | None = Field(default=None)
        id: ID | None = Field(default=None)
        client_id: ID | None = Field(
            validation_alias=AliasChoices("client_id", "clientId"),
            serialization_alias="clientId",
            default=None,
        )

    class Meta:
        """Meta class for Release"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment DetailRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  clients {\n    ...ListClient\n    __typename\n  }\n  __typename\n}\n\nquery Release($identifier: AppIdentifier, $version: Version, $id: ID, $clientId: ID) {\n  release(\n    identifier: $identifier\n    version: $version\n    id: $id\n    clientId: $clientId\n  ) {\n    ...DetailRelease\n    __typename\n  }\n}"


class DetailReleaseQuery(BaseModel):
    """No documentation found for this operation."""

    release: DetailRelease

    class Arguments(BaseModel):
        """Arguments for DetailRelease"""

        id: ID

    class Meta:
        """Meta class for DetailRelease"""

        document = "fragment ListApp on App {\n  id\n  identifier\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment DetailRelease on Release {\n  id\n  version\n  logo {\n    presignedUrl\n    __typename\n  }\n  app {\n    ...ListApp\n    __typename\n  }\n  clients {\n    ...ListClient\n    __typename\n  }\n  __typename\n}\n\nquery DetailRelease($id: ID!) {\n  release(id: $id) {\n    ...DetailRelease\n    __typename\n  }\n}"


class ScopesQueryScopes(BaseModel):
    """A scope that can be assigned to a client. Scopes are used to limit the access of a client to a user's data. They represent app-level permissions."""

    typename: Literal["Scope"] = Field(
        alias="__typename", default="Scope", exclude=True
    )
    description: str
    "The description of the scope. This is a human readable description of the scope."
    value: str
    "The value of the scope. This is the value that is used in the OAuth2 flow."
    label: str
    "The label of the scope. This is the human readable name of the scope."
    model_config = ConfigDict(frozen=True)


class ScopesQuery(BaseModel):
    """No documentation found for this operation."""

    scopes: tuple[ScopesQueryScopes, ...]

    class Arguments(BaseModel):
        """Arguments for Scopes"""

        pass

    class Meta:
        """Meta class for Scopes"""

        document = "query Scopes {\n  scopes {\n    description\n    value\n    label\n    __typename\n  }\n}"


class ScopesOptionsQueryOptions(BaseModel):
    """A scope that can be assigned to a client. Scopes are used to limit the access of a client to a user's data. They represent app-level permissions."""

    typename: Literal["Scope"] = Field(
        alias="__typename", default="Scope", exclude=True
    )
    value: str
    "The value of the scope. This is the value that is used in the OAuth2 flow."
    label: str
    "The label of the scope. This is the human readable name of the scope."
    model_config = ConfigDict(frozen=True)


class ScopesOptionsQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[ScopesOptionsQueryOptions, ...]

    class Arguments(BaseModel):
        """Arguments for ScopesOptions"""

        pass

    class Meta:
        """Meta class for ScopesOptions"""

        document = "query ScopesOptions {\n  options: scopes {\n    value\n    label\n    __typename\n  }\n}"


class GlobalSearchQuery(BaseModel):
    """No documentation found for this operation."""

    users: tuple[ListUser, ...] | None = Field(default=None)
    groups: tuple[ListGroup, ...] | None = Field(default=None)

    class Arguments(BaseModel):
        """Arguments for GlobalSearch"""

        search: str | None = Field(default=None)
        no_users: bool = Field(
            validation_alias=AliasChoices("no_users", "noUsers"),
            serialization_alias="noUsers",
        )
        no_groups: bool = Field(
            validation_alias=AliasChoices("no_groups", "noGroups"),
            serialization_alias="noGroups",
        )
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for GlobalSearch"""

        document = "fragment ListGroup on Group {\n  id\n  name\n  profile {\n    id\n    bio\n    avatar {\n      presignedUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nquery GlobalSearch($search: String, $noUsers: Boolean!, $noGroups: Boolean!, $pagination: OffsetPaginationInput) {\n  users: users(filters: {search: $search}, pagination: $pagination) @skip(if: $noUsers) {\n    ...ListUser\n    __typename\n  }\n  groups: groups(filters: {search: $search}, pagination: $pagination) @skip(if: $noGroups) {\n    ...ListGroup\n    __typename\n  }\n}"


class ListServiceInstancesQuery(BaseModel):
    """No documentation found for this operation."""

    service_instances: tuple[ListServiceInstance, ...] = Field(alias="serviceInstances")

    class Arguments(BaseModel):
        """Arguments for ListServiceInstances"""

        pagination: OffsetPaginationInput | None = Field(default=None)
        filters: ServiceInstanceFilter | None = Field(default=None)

    class Meta:
        """Meta class for ListServiceInstances"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nquery ListServiceInstances($pagination: OffsetPaginationInput, $filters: ServiceInstanceFilter) {\n  serviceInstances(pagination: $pagination, filters: $filters) {\n    ...ListServiceInstance\n    __typename\n  }\n}"


class GetServiceInstanceQuery(BaseModel):
    """No documentation found for this operation."""

    service_instance: ServiceInstance = Field(alias="serviceInstance")

    class Arguments(BaseModel):
        """Arguments for GetServiceInstance"""

        id: ID

    class Meta:
        """Meta class for GetServiceInstance"""

        document = "fragment ListClient on Client {\n  id\n  user {\n    id\n    username\n    __typename\n  }\n  name\n  kind\n  release {\n    version\n    logo {\n      presignedUrl\n      __typename\n    }\n    app {\n      id\n      identifier\n      logo {\n        presignedUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ListGroup on Group {\n  id\n  name\n  profile {\n    id\n    bio\n    avatar {\n      presignedUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ListServiceInstanceMapping on ServiceInstanceMapping {\n  id\n  key\n  instance {\n    ...ListServiceInstance\n    __typename\n  }\n  client {\n    ...ListClient\n    __typename\n  }\n  optional\n  __typename\n}\n\nfragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ServiceInstance on ServiceInstance {\n  id\n  instanceId\n  release {\n    version\n    service {\n      id\n      identifier\n      __typename\n    }\n    __typename\n  }\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  allowedGroups {\n    ...ListGroup\n    __typename\n  }\n  deniedGroups {\n    ...ListGroup\n    __typename\n  }\n  mappings {\n    ...ListServiceInstanceMapping\n    __typename\n  }\n  logo {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nquery GetServiceInstance($id: ID!) {\n  serviceInstance(id: $id) {\n    ...ServiceInstance\n    __typename\n  }\n}"


class ListServiceReleasesQuery(BaseModel):
    """No documentation found for this operation."""

    service_releases: tuple[ListServiceRelease, ...] = Field(alias="serviceReleases")

    class Arguments(BaseModel):
        """Arguments for ListServiceReleases"""

        pagination: OffsetPaginationInput | None = Field(default=None)
        filters: ServiceReleaseFilter | None = Field(default=None)

    class Meta:
        """Meta class for ListServiceReleases"""

        document = "fragment ListServiceRelease on ServiceRelease {\n  id\n  service {\n    id\n    name\n    __typename\n  }\n  version\n  __typename\n}\n\nquery ListServiceReleases($pagination: OffsetPaginationInput, $filters: ServiceReleaseFilter) {\n  serviceReleases(pagination: $pagination, filters: $filters) {\n    ...ListServiceRelease\n    __typename\n  }\n}"


class GetServiceReleaseQuery(BaseModel):
    """No documentation found for this operation."""

    service_release: ServiceRelease = Field(alias="serviceRelease")

    class Arguments(BaseModel):
        """Arguments for GetServiceRelease"""

        id: ID

    class Meta:
        """Meta class for GetServiceRelease"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nfragment ListServiceInstance on ServiceInstance {\n  id\n  instanceId\n  allowedUsers {\n    ...ListUser\n    __typename\n  }\n  deniedUsers {\n    ...ListUser\n    __typename\n  }\n  __typename\n}\n\nfragment ServiceRelease on ServiceRelease {\n  id\n  service {\n    id\n    name\n    __typename\n  }\n  version\n  instances {\n    ...ListServiceInstance\n    __typename\n  }\n  __typename\n}\n\nquery GetServiceRelease($id: ID!) {\n  serviceRelease(id: $id) {\n    ...ServiceRelease\n    __typename\n  }\n}"


class ListServicesQuery(BaseModel):
    """No documentation found for this operation."""

    services: tuple[ListService, ...]

    class Arguments(BaseModel):
        """Arguments for ListServices"""

        pagination: OffsetPaginationInput | None = Field(default=None)
        filters: ServiceFilter | None = Field(default=None)

    class Meta:
        """Meta class for ListServices"""

        document = "fragment ListServiceRelease on ServiceRelease {\n  id\n  service {\n    id\n    name\n    __typename\n  }\n  version\n  __typename\n}\n\nfragment ListService on Service {\n  identifier\n  id\n  name\n  releases {\n    ...ListServiceRelease\n    __typename\n  }\n  __typename\n}\n\nquery ListServices($pagination: OffsetPaginationInput, $filters: ServiceFilter) {\n  services(pagination: $pagination, filters: $filters) {\n    ...ListService\n    __typename\n  }\n}"


class GetServiceQuery(BaseModel):
    """No documentation found for this operation."""

    service: Service

    class Arguments(BaseModel):
        """Arguments for GetService"""

        id: ID

    class Meta:
        """Meta class for GetService"""

        document = "fragment Service on Service {\n  identifier\n  id\n  name\n  logo {\n    presignedUrl\n    __typename\n  }\n  description\n  __typename\n}\n\nquery GetService($id: ID!) {\n  service(id: $id) {\n    ...Service\n    __typename\n  }\n}"


class MeQuery(BaseModel):
    """No documentation found for this operation."""

    me: DetailUser

    class Arguments(BaseModel):
        """Arguments for Me"""

        pass

    class Meta:
        """Meta class for Me"""

        document = "fragment Profile on Profile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment DetailUser on User {\n  id\n  username\n  email\n  firstName\n  lastName\n  avatar\n  groups {\n    id\n    name\n    __typename\n  }\n  profile {\n    ...Profile\n    __typename\n  }\n  __typename\n}\n\nquery Me {\n  me {\n    ...DetailUser\n    __typename\n  }\n}"


class UserQuery(BaseModel):
    """No documentation found for this operation."""

    user: DetailUser

    class Arguments(BaseModel):
        """Arguments for User"""

        id: ID

    class Meta:
        """Meta class for User"""

        document = "fragment Profile on Profile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment DetailUser on User {\n  id\n  username\n  email\n  firstName\n  lastName\n  avatar\n  groups {\n    id\n    name\n    __typename\n  }\n  profile {\n    ...Profile\n    __typename\n  }\n  __typename\n}\n\nquery User($id: ID!) {\n  user(id: $id) {\n    ...DetailUser\n    __typename\n  }\n}"


class DetailUserQuery(BaseModel):
    """No documentation found for this operation."""

    user: DetailUser

    class Arguments(BaseModel):
        """Arguments for DetailUser"""

        id: ID

    class Meta:
        """Meta class for DetailUser"""

        document = "fragment Profile on Profile {\n  id\n  name\n  avatar {\n    presignedUrl\n    __typename\n  }\n  __typename\n}\n\nfragment DetailUser on User {\n  id\n  username\n  email\n  firstName\n  lastName\n  avatar\n  groups {\n    id\n    name\n    __typename\n  }\n  profile {\n    ...Profile\n    __typename\n  }\n  __typename\n}\n\nquery DetailUser($id: ID!) {\n  user(id: $id) {\n    ...DetailUser\n    __typename\n  }\n}"


class UsersQuery(BaseModel):
    """No documentation found for this operation."""

    users: tuple[ListUser, ...]

    class Arguments(BaseModel):
        """Arguments for Users"""

        filters: UserFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for Users"""

        document = "fragment ListUser on User {\n  username\n  firstName\n  lastName\n  email\n  avatar\n  id\n  __typename\n}\n\nquery Users($filters: UserFilter, $pagination: OffsetPaginationInput) {\n  users(filters: $filters, pagination: $pagination) {\n    ...ListUser\n    __typename\n  }\n}"


class UserOptionsQueryOptions(BaseModel):
    """
    A User is a person that can log in to the system. They are uniquely identified by their username.
    And can have an email address associated with them (but don't have to).

    A user can be assigned to groups and has a profile that can be used to display information about them.
    Detail information about a user can be found in the profile.

    All users can have social accounts associated with them. These are used to authenticate the user with external services,
    such as ORCID or GitHub.
    """

    typename: Literal["User"] = Field(alias="__typename", default="User", exclude=True)
    value: ID
    label: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    model_config = ConfigDict(frozen=True)


class UserOptionsQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[UserOptionsQueryOptions, ...]

    class Arguments(BaseModel):
        """Arguments for UserOptions"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for UserOptions"""

        document = "query UserOptions($search: String, $values: [ID!]) {\n  options: users(filters: {search: $search, ids: $values}) {\n    value: id\n    label: username\n    __typename\n  }\n}"


class ProfileQuery(BaseModel):
    """No documentation found for this operation."""

    me: MeUser

    class Arguments(BaseModel):
        """Arguments for Profile"""

        pass

    class Meta:
        """Meta class for Profile"""

        document = "fragment MeUser on User {\n  id\n  username\n  email\n  firstName\n  lastName\n  avatar\n  __typename\n}\n\nquery Profile {\n  me {\n    ...MeUser\n    __typename\n  }\n}"


class UnlokApi:
    """Every operation of this API as a method. Generated by turms.

    Each method hands its operation to ``execute``, ``aexecute``, ``subscribe``, ``asubscribe`` of ``self``, which the class this one is mixed into (or a base of it) provides.
    """

    async def acreate_client(
        self,
        manifest: ManifestInput,
        hub: IDCoercible | None | UnsetType = UNSET,
        layers: Iterable[str] | None | UnsetType = UNSET,
        role: ClientRole | None | UnsetType = UNSET,
    ) -> DetailClient:
        """CreateClient


        Args:
            manifest:  (required)
            hub: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
            layers: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required) (list)
            role: ClientRole

        Returns:
            DetailClient"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["manifest"] = manifest
        if hub is not UNSET:
            _input["hub"] = hub
        if layers is not UNSET:
            _input["layers"] = layers
        if role is not UNSET:
            _input["role"] = role
        variables["input"] = _input
        return (
            await self.aexecute(CreateClientMutation, variables)
        ).create_developmental_client

    def create_client(
        self,
        manifest: ManifestInput,
        hub: IDCoercible | None | UnsetType = UNSET,
        layers: Iterable[str] | None | UnsetType = UNSET,
        role: ClientRole | None | UnsetType = UNSET,
    ) -> DetailClient:
        """CreateClient


        Args:
            manifest:  (required)
            hub: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
            layers: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required) (list)
            role: ClientRole

        Returns:
            DetailClient"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["manifest"] = manifest
        if hub is not UNSET:
            _input["hub"] = hub
        if layers is not UNSET:
            _input["layers"] = layers
        if role is not UNSET:
            _input["role"] = role
        variables["input"] = _input
        return self.execute(CreateClientMutation, variables).create_developmental_client

    async def acreate_group_profile(
        self, group: IDCoercible, name: str, avatar: IDCoercible
    ) -> GroupProfile:
        """CreateGroupProfile


        Args:
            group: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            avatar: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)

        Returns:
            GroupProfile"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["group"] = group
        _input["name"] = name
        _input["avatar"] = avatar
        variables["input"] = _input
        return (
            await self.aexecute(CreateGroupProfileMutation, variables)
        ).create_group_profile

    def create_group_profile(
        self, group: IDCoercible, name: str, avatar: IDCoercible
    ) -> GroupProfile:
        """CreateGroupProfile


        Args:
            group: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            avatar: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)

        Returns:
            GroupProfile"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["group"] = group
        _input["name"] = name
        _input["avatar"] = avatar
        variables["input"] = _input
        return self.execute(CreateGroupProfileMutation, variables).create_group_profile

    async def aupdate_group_profile(
        self, id: IDCoercible, name: str, avatar: IDCoercible
    ) -> GroupProfile:
        """UpdateGroupProfile


        Args:
            id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            avatar: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)

        Returns:
            GroupProfile"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        _input["name"] = name
        _input["avatar"] = avatar
        variables["input"] = _input
        return (
            await self.aexecute(UpdateGroupProfileMutation, variables)
        ).update_group_profile

    def update_group_profile(
        self, id: IDCoercible, name: str, avatar: IDCoercible
    ) -> GroupProfile:
        """UpdateGroupProfile


        Args:
            id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            avatar: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)

        Returns:
            GroupProfile"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        _input["name"] = name
        _input["avatar"] = avatar
        variables["input"] = _input
        return self.execute(UpdateGroupProfileMutation, variables).update_group_profile

    async def aupdate_service_instance(
        self,
        id: IDCoercible,
        allowed_users: Iterable[IDCoercible] | None | UnsetType = UNSET,
        allowed_groups: Iterable[IDCoercible] | None | UnsetType = UNSET,
        denied_groups: Iterable[IDCoercible] | None | UnsetType = UNSET,
        denied_users: Iterable[IDCoercible] | None | UnsetType = UNSET,
    ) -> ServiceInstance:
        """UpdateServiceInstance


        Args:
            allowed_users: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            allowed_groups: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            denied_groups: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            denied_users: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)

        Returns:
            ServiceInstance"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        if allowed_users is not UNSET:
            _input["allowedUsers"] = allowed_users
        if allowed_groups is not UNSET:
            _input["allowedGroups"] = allowed_groups
        if denied_groups is not UNSET:
            _input["deniedGroups"] = denied_groups
        if denied_users is not UNSET:
            _input["deniedUsers"] = denied_users
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(UpdateServiceInstanceMutation, variables)
        ).update_service_instance

    def update_service_instance(
        self,
        id: IDCoercible,
        allowed_users: Iterable[IDCoercible] | None | UnsetType = UNSET,
        allowed_groups: Iterable[IDCoercible] | None | UnsetType = UNSET,
        denied_groups: Iterable[IDCoercible] | None | UnsetType = UNSET,
        denied_users: Iterable[IDCoercible] | None | UnsetType = UNSET,
    ) -> ServiceInstance:
        """UpdateServiceInstance


        Args:
            allowed_users: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            allowed_groups: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            denied_groups: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            denied_users: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)

        Returns:
            ServiceInstance"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        if allowed_users is not UNSET:
            _input["allowedUsers"] = allowed_users
        if allowed_groups is not UNSET:
            _input["allowedGroups"] = allowed_groups
        if denied_groups is not UNSET:
            _input["deniedGroups"] = denied_groups
        if denied_users is not UNSET:
            _input["deniedUsers"] = denied_users
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            UpdateServiceInstanceMutation, variables
        ).update_service_instance

    async def acreate_service_instance(
        self,
        identifier: str,
        service: IDCoercible,
        allowed_users: Iterable[IDCoercible] | None | UnsetType = UNSET,
        allowed_groups: Iterable[IDCoercible] | None | UnsetType = UNSET,
        denied_groups: Iterable[IDCoercible] | None | UnsetType = UNSET,
        denied_users: Iterable[IDCoercible] | None | UnsetType = UNSET,
    ) -> ServiceInstance:
        """CreateServiceInstance


        Args:
            identifier: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            service: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            allowed_users: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            allowed_groups: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            denied_groups: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            denied_users: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)

        Returns:
            ServiceInstance"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["identifier"] = identifier
        _input["service"] = service
        if allowed_users is not UNSET:
            _input["allowedUsers"] = allowed_users
        if allowed_groups is not UNSET:
            _input["allowedGroups"] = allowed_groups
        if denied_groups is not UNSET:
            _input["deniedGroups"] = denied_groups
        if denied_users is not UNSET:
            _input["deniedUsers"] = denied_users
        variables["input"] = _input
        return (
            await self.aexecute(CreateServiceInstanceMutation, variables)
        ).create_service_instance

    def create_service_instance(
        self,
        identifier: str,
        service: IDCoercible,
        allowed_users: Iterable[IDCoercible] | None | UnsetType = UNSET,
        allowed_groups: Iterable[IDCoercible] | None | UnsetType = UNSET,
        denied_groups: Iterable[IDCoercible] | None | UnsetType = UNSET,
        denied_users: Iterable[IDCoercible] | None | UnsetType = UNSET,
    ) -> ServiceInstance:
        """CreateServiceInstance


        Args:
            identifier: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            service: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            allowed_users: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            allowed_groups: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            denied_groups: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)
            denied_users: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required) (list)

        Returns:
            ServiceInstance"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["identifier"] = identifier
        _input["service"] = service
        if allowed_users is not UNSET:
            _input["allowedUsers"] = allowed_users
        if allowed_groups is not UNSET:
            _input["allowedGroups"] = allowed_groups
        if denied_groups is not UNSET:
            _input["deniedGroups"] = denied_groups
        if denied_users is not UNSET:
            _input["deniedUsers"] = denied_users
        variables["input"] = _input
        return self.execute(
            CreateServiceInstanceMutation, variables
        ).create_service_instance

    async def acreate_user_profile(self, user: IDCoercible, name: str) -> Profile:
        """CreateUserProfile


        Args:
            user: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)

        Returns:
            Profile"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["user"] = user
        _input["name"] = name
        variables["input"] = _input
        return (
            await self.aexecute(CreateUserProfileMutation, variables)
        ).create_profile

    def create_user_profile(self, user: IDCoercible, name: str) -> Profile:
        """CreateUserProfile


        Args:
            user: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)

        Returns:
            Profile"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["user"] = user
        _input["name"] = name
        variables["input"] = _input
        return self.execute(CreateUserProfileMutation, variables).create_profile

    async def aupdate_user_profile(
        self, id: IDCoercible, name: str, avatar: IDCoercible
    ) -> Profile:
        """UpdateUserProfile


        Args:
            id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            avatar: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)

        Returns:
            Profile"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        _input["name"] = name
        _input["avatar"] = avatar
        variables["input"] = _input
        return (
            await self.aexecute(UpdateUserProfileMutation, variables)
        ).update_profile

    def update_user_profile(
        self, id: IDCoercible, name: str, avatar: IDCoercible
    ) -> Profile:
        """UpdateUserProfile


        Args:
            id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
            name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            avatar: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)

        Returns:
            Profile"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        _input["name"] = name
        _input["avatar"] = avatar
        variables["input"] = _input
        return self.execute(UpdateUserProfileMutation, variables).update_profile

    async def acreate_redeem_token(
        self,
        manifest: ManifestInput,
        token: str | None | UnsetType = UNSET,
        expires_in_days: int | None | UnsetType = UNSET,
        max_redemptions: int | None | UnsetType = UNSET,
    ) -> DetailRedeemToken:
        """CreateRedeemToken


        Args:
            manifest:  (required)
            token: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
            expires_in_days: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
            max_redemptions: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

        Returns:
            DetailRedeemToken"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["manifest"] = manifest
        if token is not UNSET:
            _input["token"] = token
        if expires_in_days is not UNSET:
            _input["expiresInDays"] = expires_in_days
        if max_redemptions is not UNSET:
            _input["maxRedemptions"] = max_redemptions
        variables["input"] = _input
        return (
            await self.aexecute(CreateRedeemTokenMutation, variables)
        ).create_redeem_token

    def create_redeem_token(
        self,
        manifest: ManifestInput,
        token: str | None | UnsetType = UNSET,
        expires_in_days: int | None | UnsetType = UNSET,
        max_redemptions: int | None | UnsetType = UNSET,
    ) -> DetailRedeemToken:
        """CreateRedeemToken


        Args:
            manifest:  (required)
            token: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
            expires_in_days: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
            max_redemptions: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

        Returns:
            DetailRedeemToken"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["manifest"] = manifest
        if token is not UNSET:
            _input["token"] = token
        if expires_in_days is not UNSET:
            _input["expiresInDays"] = expires_in_days
        if max_redemptions is not UNSET:
            _input["maxRedemptions"] = max_redemptions
        variables["input"] = _input
        return self.execute(CreateRedeemTokenMutation, variables).create_redeem_token

    async def adelete_redeem_token(self, id: IDCoercible) -> ID:
        """DeleteRedeemToken


        Args:
            id (ID): No description

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(DeleteRedeemTokenMutation, variables)
        ).delete_redeem_token

    def delete_redeem_token(self, id: IDCoercible) -> ID:
        """DeleteRedeemToken


        Args:
            id (ID): No description

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(DeleteRedeemTokenMutation, variables).delete_redeem_token

    async def arequest_media_upload(
        self, key: str, datalayer: str
    ) -> PresignedPostCredentials:
        """RequestMediaUpload


        Args:
            key (str): No description
            datalayer (str): No description

        Returns:
            PresignedPostCredentials"""
        variables: dict[str, builtins.object] = {}
        variables["key"] = key
        variables["datalayer"] = datalayer
        return (
            await self.aexecute(RequestMediaUploadMutation, variables)
        ).request_media_upload

    def request_media_upload(
        self, key: str, datalayer: str
    ) -> PresignedPostCredentials:
        """RequestMediaUpload


        Args:
            key (str): No description
            datalayer (str): No description

        Returns:
            PresignedPostCredentials"""
        variables: dict[str, builtins.object] = {}
        variables["key"] = key
        variables["datalayer"] = datalayer
        return self.execute(RequestMediaUploadMutation, variables).request_media_upload

    async def aapps(
        self,
        filters: AppFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListApp, ...]:
        """Apps


        Args:
            filters (AppFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListApp]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(AppsQuery, variables)).apps

    def apps(
        self,
        filters: AppFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListApp, ...]:
        """Apps


        Args:
            filters (AppFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListApp]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(AppsQuery, variables).apps

    async def aapp(
        self,
        identifier: str | None | UnsetType = UNSET,
        id: IDCoercible | None | UnsetType = UNSET,
        client_id: IDCoercible | None | UnsetType = UNSET,
    ) -> DetailApp:
        """App


        Args:
            identifier (str | None, optional): No description.
            id (ID | None, optional): No description.
            client_id (ID | None, optional): No description.

        Returns:
            DetailApp"""
        variables: dict[str, builtins.object] = {}
        if identifier is not UNSET:
            variables["identifier"] = identifier
        if id is not UNSET:
            variables["id"] = id
        if client_id is not UNSET:
            variables["clientId"] = client_id
        return (await self.aexecute(AppQuery, variables)).app

    def app(
        self,
        identifier: str | None | UnsetType = UNSET,
        id: IDCoercible | None | UnsetType = UNSET,
        client_id: IDCoercible | None | UnsetType = UNSET,
    ) -> DetailApp:
        """App


        Args:
            identifier (str | None, optional): No description.
            id (ID | None, optional): No description.
            client_id (ID | None, optional): No description.

        Returns:
            DetailApp"""
        variables: dict[str, builtins.object] = {}
        if identifier is not UNSET:
            variables["identifier"] = identifier
        if id is not UNSET:
            variables["id"] = id
        if client_id is not UNSET:
            variables["clientId"] = client_id
        return self.execute(AppQuery, variables).app

    async def adetail_app(self, id: IDCoercible) -> DetailApp:
        """DetailApp


        Args:
            id (ID): No description

        Returns:
            DetailApp"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(DetailAppQuery, variables)).app

    def detail_app(self, id: IDCoercible) -> DetailApp:
        """DetailApp


        Args:
            id (ID): No description

        Returns:
            DetailApp"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(DetailAppQuery, variables).app

    async def aclients(
        self,
        filters: ClientFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListClient, ...]:
        """Clients


        Args:
            filters (ClientFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListClient]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(ClientsQuery, variables)).clients

    def clients(
        self,
        filters: ClientFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListClient, ...]:
        """Clients


        Args:
            filters (ClientFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListClient]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(ClientsQuery, variables).clients

    async def adetail_client(self, id: IDCoercible) -> DetailClient:
        """DetailClient


        Args:
            id (ID): No description

        Returns:
            DetailClient"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(DetailClientQuery, variables)).client

    def detail_client(self, id: IDCoercible) -> DetailClient:
        """DetailClient


        Args:
            id (ID): No description

        Returns:
            DetailClient"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(DetailClientQuery, variables).client

    async def amy_managed_clients(self, kind: ClientKind) -> tuple[ListClient, ...]:
        """MyManagedClients


        Args:
            kind (ClientKind): No description

        Returns:
            list[ListClient]"""
        variables: dict[str, builtins.object] = {}
        variables["kind"] = kind
        return (
            await self.aexecute(MyManagedClientsQuery, variables)
        ).my_managed_clients

    def my_managed_clients(self, kind: ClientKind) -> tuple[ListClient, ...]:
        """MyManagedClients


        Args:
            kind (ClientKind): No description

        Returns:
            list[ListClient]"""
        variables: dict[str, builtins.object] = {}
        variables["kind"] = kind
        return self.execute(MyManagedClientsQuery, variables).my_managed_clients

    async def aclient(self, client_id: IDCoercible) -> DetailClient:
        """Client


        Args:
            client_id (ID): No description

        Returns:
            DetailClient"""
        variables: dict[str, builtins.object] = {}
        variables["clientId"] = client_id
        return (await self.aexecute(ClientQuery, variables)).client

    def client(self, client_id: IDCoercible) -> DetailClient:
        """Client


        Args:
            client_id (ID): No description

        Returns:
            DetailClient"""
        variables: dict[str, builtins.object] = {}
        variables["clientId"] = client_id
        return self.execute(ClientQuery, variables).client

    async def agroup_options(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
    ) -> tuple[GroupOptionsQueryOptions, ...]:
        """GroupOptions


        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.

        Returns:
            list[GroupOptionsQueryGroups]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (await self.aexecute(GroupOptionsQuery, variables)).options

    def group_options(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
    ) -> tuple[GroupOptionsQueryOptions, ...]:
        """GroupOptions


        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.

        Returns:
            list[GroupOptionsQueryGroups]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(GroupOptionsQuery, variables).options

    async def adetail_group(self, id: IDCoercible) -> DetailGroup:
        """DetailGroup


        Args:
            id (ID): No description

        Returns:
            DetailGroup"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(DetailGroupQuery, variables)).group

    def detail_group(self, id: IDCoercible) -> DetailGroup:
        """DetailGroup


        Args:
            id (ID): No description

        Returns:
            DetailGroup"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(DetailGroupQuery, variables).group

    async def agroups(
        self,
        filters: GroupFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListGroup, ...]:
        """Groups


        Args:
            filters (GroupFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListGroup]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(GroupsQuery, variables)).groups

    def groups(
        self,
        filters: GroupFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListGroup, ...]:
        """Groups


        Args:
            filters (GroupFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListGroup]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(GroupsQuery, variables).groups

    async def alayers(
        self,
        filters: LayerFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListLayer, ...]:
        """Layers


        Args:
            filters (LayerFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListLayer]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(LayersQuery, variables)).layers

    def layers(
        self,
        filters: LayerFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListLayer, ...]:
        """Layers


        Args:
            filters (LayerFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListLayer]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(LayersQuery, variables).layers

    async def adetail_layer(self, id: IDCoercible) -> Layer:
        """DetailLayer


        Args:
            id (ID): No description

        Returns:
            Layer"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(DetailLayerQuery, variables)).layer

    def detail_layer(self, id: IDCoercible) -> Layer:
        """DetailLayer


        Args:
            id (ID): No description

        Returns:
            Layer"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(DetailLayerQuery, variables).layer

    async def aredeem_token(self, id: IDCoercible) -> DetailRedeemToken:
        """RedeemToken


        Args:
            id (ID): No description

        Returns:
            DetailRedeemToken"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(RedeemTokenQuery, variables)).redeem_token

    def redeem_token(self, id: IDCoercible) -> DetailRedeemToken:
        """RedeemToken


        Args:
            id (ID): No description

        Returns:
            DetailRedeemToken"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(RedeemTokenQuery, variables).redeem_token

    async def aredeem_tokens(
        self,
        filters: RedeemTokenFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListRedeemToken, ...]:
        """RedeemTokens


        Args:
            filters (RedeemTokenFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListRedeemToken]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(RedeemTokensQuery, variables)).redeem_tokens

    def redeem_tokens(
        self,
        filters: RedeemTokenFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListRedeemToken, ...]:
        """RedeemTokens


        Args:
            filters (RedeemTokenFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListRedeemToken]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(RedeemTokensQuery, variables).redeem_tokens

    async def areleases(self) -> tuple[ListRelease, ...]:
        """Releases


        Args:

        Returns:
            list[ListRelease]"""
        variables: dict[str, builtins.object] = {}
        return (await self.aexecute(ReleasesQuery, variables)).releases

    def releases(self) -> tuple[ListRelease, ...]:
        """Releases


        Args:

        Returns:
            list[ListRelease]"""
        variables: dict[str, builtins.object] = {}
        return self.execute(ReleasesQuery, variables).releases

    async def arelease(
        self,
        identifier: str | None | UnsetType = UNSET,
        version: str | None | UnsetType = UNSET,
        id: IDCoercible | None | UnsetType = UNSET,
        client_id: IDCoercible | None | UnsetType = UNSET,
    ) -> DetailRelease:
        """Release


        Args:
            identifier (str | None, optional): No description.
            version (str | None, optional): No description.
            id (ID | None, optional): No description.
            client_id (ID | None, optional): No description.

        Returns:
            DetailRelease"""
        variables: dict[str, builtins.object] = {}
        if identifier is not UNSET:
            variables["identifier"] = identifier
        if version is not UNSET:
            variables["version"] = version
        if id is not UNSET:
            variables["id"] = id
        if client_id is not UNSET:
            variables["clientId"] = client_id
        return (await self.aexecute(ReleaseQuery, variables)).release

    def release(
        self,
        identifier: str | None | UnsetType = UNSET,
        version: str | None | UnsetType = UNSET,
        id: IDCoercible | None | UnsetType = UNSET,
        client_id: IDCoercible | None | UnsetType = UNSET,
    ) -> DetailRelease:
        """Release


        Args:
            identifier (str | None, optional): No description.
            version (str | None, optional): No description.
            id (ID | None, optional): No description.
            client_id (ID | None, optional): No description.

        Returns:
            DetailRelease"""
        variables: dict[str, builtins.object] = {}
        if identifier is not UNSET:
            variables["identifier"] = identifier
        if version is not UNSET:
            variables["version"] = version
        if id is not UNSET:
            variables["id"] = id
        if client_id is not UNSET:
            variables["clientId"] = client_id
        return self.execute(ReleaseQuery, variables).release

    async def adetail_release(self, id: IDCoercible) -> DetailRelease:
        """DetailRelease


        Args:
            id (ID): No description

        Returns:
            DetailRelease"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(DetailReleaseQuery, variables)).release

    def detail_release(self, id: IDCoercible) -> DetailRelease:
        """DetailRelease


        Args:
            id (ID): No description

        Returns:
            DetailRelease"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(DetailReleaseQuery, variables).release

    async def ascopes(self) -> tuple[ScopesQueryScopes, ...]:
        """Scopes


        Args:

        Returns:
            list[ScopesQueryScopes]"""
        variables: dict[str, builtins.object] = {}
        return (await self.aexecute(ScopesQuery, variables)).scopes

    def scopes(self) -> tuple[ScopesQueryScopes, ...]:
        """Scopes


        Args:

        Returns:
            list[ScopesQueryScopes]"""
        variables: dict[str, builtins.object] = {}
        return self.execute(ScopesQuery, variables).scopes

    async def ascopes_options(self) -> tuple[ScopesOptionsQueryOptions, ...]:
        """ScopesOptions


        Args:

        Returns:
            list[ScopesOptionsQueryScopes]"""
        variables: dict[str, builtins.object] = {}
        return (await self.aexecute(ScopesOptionsQuery, variables)).options

    def scopes_options(self) -> tuple[ScopesOptionsQueryOptions, ...]:
        """ScopesOptions


        Args:

        Returns:
            list[ScopesOptionsQueryScopes]"""
        variables: dict[str, builtins.object] = {}
        return self.execute(ScopesOptionsQuery, variables).options

    async def aglobal_search(
        self,
        no_users: bool,
        no_groups: bool,
        search: str | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> GlobalSearchQuery:
        """GlobalSearch


        Args:
            no_users (bool): No description
            no_groups (bool): No description
            search (str | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            GlobalSearchQuery"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        variables["noUsers"] = no_users
        variables["noGroups"] = no_groups
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return await self.aexecute(GlobalSearchQuery, variables)

    def global_search(
        self,
        no_users: bool,
        no_groups: bool,
        search: str | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> GlobalSearchQuery:
        """GlobalSearch


        Args:
            no_users (bool): No description
            no_groups (bool): No description
            search (str | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            GlobalSearchQuery"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        variables["noUsers"] = no_users
        variables["noGroups"] = no_groups
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(GlobalSearchQuery, variables)

    async def alist_service_instances(
        self,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        filters: ServiceInstanceFilter | None | UnsetType = UNSET,
    ) -> tuple[ListServiceInstance, ...]:
        """ListServiceInstances


        Args:
            pagination (OffsetPaginationInput | None, optional): No description.
            filters (ServiceInstanceFilter | None, optional): No description.

        Returns:
            list[ListServiceInstance]"""
        variables: dict[str, builtins.object] = {}
        if pagination is not UNSET:
            variables["pagination"] = pagination
        if filters is not UNSET:
            variables["filters"] = filters
        return (
            await self.aexecute(ListServiceInstancesQuery, variables)
        ).service_instances

    def list_service_instances(
        self,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        filters: ServiceInstanceFilter | None | UnsetType = UNSET,
    ) -> tuple[ListServiceInstance, ...]:
        """ListServiceInstances


        Args:
            pagination (OffsetPaginationInput | None, optional): No description.
            filters (ServiceInstanceFilter | None, optional): No description.

        Returns:
            list[ListServiceInstance]"""
        variables: dict[str, builtins.object] = {}
        if pagination is not UNSET:
            variables["pagination"] = pagination
        if filters is not UNSET:
            variables["filters"] = filters
        return self.execute(ListServiceInstancesQuery, variables).service_instances

    async def aget_service_instance(self, id: IDCoercible) -> ServiceInstance:
        """GetServiceInstance


        Args:
            id (ID): No description

        Returns:
            ServiceInstance"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetServiceInstanceQuery, variables)
        ).service_instance

    def get_service_instance(self, id: IDCoercible) -> ServiceInstance:
        """GetServiceInstance


        Args:
            id (ID): No description

        Returns:
            ServiceInstance"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetServiceInstanceQuery, variables).service_instance

    async def alist_service_releases(
        self,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        filters: ServiceReleaseFilter | None | UnsetType = UNSET,
    ) -> tuple[ListServiceRelease, ...]:
        """ListServiceReleases


        Args:
            pagination (OffsetPaginationInput | None, optional): No description.
            filters (ServiceReleaseFilter | None, optional): No description.

        Returns:
            list[ListServiceRelease]"""
        variables: dict[str, builtins.object] = {}
        if pagination is not UNSET:
            variables["pagination"] = pagination
        if filters is not UNSET:
            variables["filters"] = filters
        return (
            await self.aexecute(ListServiceReleasesQuery, variables)
        ).service_releases

    def list_service_releases(
        self,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        filters: ServiceReleaseFilter | None | UnsetType = UNSET,
    ) -> tuple[ListServiceRelease, ...]:
        """ListServiceReleases


        Args:
            pagination (OffsetPaginationInput | None, optional): No description.
            filters (ServiceReleaseFilter | None, optional): No description.

        Returns:
            list[ListServiceRelease]"""
        variables: dict[str, builtins.object] = {}
        if pagination is not UNSET:
            variables["pagination"] = pagination
        if filters is not UNSET:
            variables["filters"] = filters
        return self.execute(ListServiceReleasesQuery, variables).service_releases

    async def aget_service_release(self, id: IDCoercible) -> ServiceRelease:
        """GetServiceRelease


        Args:
            id (ID): No description

        Returns:
            ServiceRelease"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetServiceReleaseQuery, variables)).service_release

    def get_service_release(self, id: IDCoercible) -> ServiceRelease:
        """GetServiceRelease


        Args:
            id (ID): No description

        Returns:
            ServiceRelease"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetServiceReleaseQuery, variables).service_release

    async def alist_services(
        self,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        filters: ServiceFilter | None | UnsetType = UNSET,
    ) -> tuple[ListService, ...]:
        """ListServices


        Args:
            pagination (OffsetPaginationInput | None, optional): No description.
            filters (ServiceFilter | None, optional): No description.

        Returns:
            list[ListService]"""
        variables: dict[str, builtins.object] = {}
        if pagination is not UNSET:
            variables["pagination"] = pagination
        if filters is not UNSET:
            variables["filters"] = filters
        return (await self.aexecute(ListServicesQuery, variables)).services

    def list_services(
        self,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        filters: ServiceFilter | None | UnsetType = UNSET,
    ) -> tuple[ListService, ...]:
        """ListServices


        Args:
            pagination (OffsetPaginationInput | None, optional): No description.
            filters (ServiceFilter | None, optional): No description.

        Returns:
            list[ListService]"""
        variables: dict[str, builtins.object] = {}
        if pagination is not UNSET:
            variables["pagination"] = pagination
        if filters is not UNSET:
            variables["filters"] = filters
        return self.execute(ListServicesQuery, variables).services

    async def aget_service(self, id: IDCoercible) -> Service:
        """GetService


        Args:
            id (ID): No description

        Returns:
            Service"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetServiceQuery, variables)).service

    def get_service(self, id: IDCoercible) -> Service:
        """GetService


        Args:
            id (ID): No description

        Returns:
            Service"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetServiceQuery, variables).service

    async def ame(self) -> DetailUser:
        """Me


        Args:

        Returns:
            DetailUser"""
        variables: dict[str, builtins.object] = {}
        return (await self.aexecute(MeQuery, variables)).me

    def me(self) -> DetailUser:
        """Me


        Args:

        Returns:
            DetailUser"""
        variables: dict[str, builtins.object] = {}
        return self.execute(MeQuery, variables).me

    async def auser(self, id: IDCoercible) -> DetailUser:
        """User


        Args:
            id (ID): No description

        Returns:
            DetailUser"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(UserQuery, variables)).user

    def user(self, id: IDCoercible) -> DetailUser:
        """User


        Args:
            id (ID): No description

        Returns:
            DetailUser"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(UserQuery, variables).user

    async def adetail_user(self, id: IDCoercible) -> DetailUser:
        """DetailUser


        Args:
            id (ID): No description

        Returns:
            DetailUser"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(DetailUserQuery, variables)).user

    def detail_user(self, id: IDCoercible) -> DetailUser:
        """DetailUser


        Args:
            id (ID): No description

        Returns:
            DetailUser"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(DetailUserQuery, variables).user

    async def ausers(
        self,
        filters: UserFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListUser, ...]:
        """Users


        Args:
            filters (UserFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListUser]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(UsersQuery, variables)).users

    def users(
        self,
        filters: UserFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
    ) -> tuple[ListUser, ...]:
        """Users


        Args:
            filters (UserFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.

        Returns:
            list[ListUser]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(UsersQuery, variables).users

    async def auser_options(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
    ) -> tuple[UserOptionsQueryOptions, ...]:
        """UserOptions


        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.

        Returns:
            list[UserOptionsQueryUsers]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (await self.aexecute(UserOptionsQuery, variables)).options

    def user_options(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
    ) -> tuple[UserOptionsQueryOptions, ...]:
        """UserOptions


        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.

        Returns:
            list[UserOptionsQueryUsers]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(UserOptionsQuery, variables).options

    async def aprofile(self) -> MeUser:
        """Profile


        Args:

        Returns:
            MeUser"""
        variables: dict[str, builtins.object] = {}
        return (await self.aexecute(ProfileQuery, variables)).me

    def profile(self) -> MeUser:
        """Profile


        Args:

        Returns:
            MeUser"""
        variables: dict[str, builtins.object] = {}
        return self.execute(ProfileQuery, variables).me


AppFilter.model_rebuild()
ClientFilter.model_rebuild()
DevelopmentClientInput.model_rebuild()
GroupFilter.model_rebuild()
LayerFilter.model_rebuild()
ManifestInput.model_rebuild()
RedeemTokenFilter.model_rebuild()
ServiceFilter.model_rebuild()
ServiceInstanceFilter.model_rebuild()
ServiceReleaseFilter.model_rebuild()
UserFilter.model_rebuild()
