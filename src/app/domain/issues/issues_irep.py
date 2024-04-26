class IrepIssue:
    async def create_issue(self, req: dict) -> dict:
        raise NotImplementedError
    
    async def get_all_issues(self) -> dict:
        raise NotImplementedError
    
    async def get_issue(self, req: str) -> dict:
        raise NotImplementedError
    
    async def update_issue(self, req: dict) -> dict:
        raise NotImplementedError
    
    async def delete_issue(self, req: str) -> dict:
        raise NotImplementedError