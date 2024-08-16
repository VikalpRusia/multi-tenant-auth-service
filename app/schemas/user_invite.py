from typing import override, Literal, Any

from pydantic import BaseModel, SecretStr, ConfigDict
from pydantic.main import IncEx


class UserInvite(BaseModel):
    user_id: int
    org_id: int
    role_id: int
    token: SecretStr
    model_config = ConfigDict(from_attributes=True)

    @override
    def model_dump(
        self, show_token=False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        result = super().model_dump(**kwargs)
        if not show_token:
            result.pop('token')
        return result
