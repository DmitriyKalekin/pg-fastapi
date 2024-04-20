class IRepProject:  # pragma: no cover
    async def create_project(self, req: dict) -> dict:
        raise NotImplementedError

    async def get_all_project(self) -> dict:
        raise NotImplementedError

    async def get_project(self, project_key: str) -> dict:
        raise NotImplementedError

    async def update_project(self, project_key: str,req: dict) -> dict:
        raise NotImplementedError

    async def delete_project(self, project_key: str) -> dict:
        raise NotImplementedError
