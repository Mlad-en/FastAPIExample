import os
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator, SecretStr
from dotenv import load_dotenv


load_dotenv()


class DBConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    _db_name: SecretStr = SecretStr(os.getenv("POSTGRES_DB", ""))
    _username: SecretStr = SecretStr(os.getenv("POSTGRES_USER", ""))
    _password: SecretStr = SecretStr(os.getenv("POSTGRES_PASSWORD", ""))
    _db_host: SecretStr = SecretStr(os.getenv("DB_HOST", ""))
    _db_port: SecretStr = SecretStr(os.getenv("DB_PORT", ""))

    @model_validator(mode="after")
    def validate_db_name(self) -> Self:
        if self._db_name.get_secret_value() == "":
            raise ValueError("db_name cannot be empty")
        return self

    def get_url(self) -> str:
        url = "postgresql://"
        user = self._username.get_secret_value()
        password = self._password.get_secret_value()
        db_name = self._db_name.get_secret_value()
        host = self._db_host.get_secret_value()
        port = self._db_port.get_secret_value()

        if user:
            url += f"{user}"
            url += f":{password}" if password else ""
            url += "@"

        if host:
            url += f"{host}"
            url += f":{port}" if port else ""

        url += f"/{db_name}"

        return url
