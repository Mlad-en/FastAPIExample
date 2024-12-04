# FastAPIExample


## Install project dependencies

1. Ensure the package manager and version tool [UV](https://docs.astral.sh/uv/) is installed:

   * Mac:
      ```bash
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```
   * Windows
      ```shell
      powershell -c "irm https://astral.sh/uv/install.ps1 | more"
      ```

2. ensure you have the correct python version installed - 3.12. 

   ```bash
   uv python install 3.12
   ```

3. Install the required dependencies:

   ```bash
   uv sync --frozen --all-extras
   ```
   
## Run App

1. Copy and modify the `example.env` to `.env`
    ```bash
    cp example.env .env
    ```

2. Build FastAPI image
    ```bash
    docker compose --profile db --profile fast_api up --build
    ```
   
2. use some of the http scratches to test out the api

**Note** If you need the postgres admin, you can additionally run:
```bash
docker compose --profile db --profile db_admin --profile fast_api up --build
```
The admin would then be available at: http://localhost:5050/