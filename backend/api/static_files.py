"""This file is inspired by the csxl.unc.edu project, and aims to extend the static files class to support a statically built frontend"""

from fastapi import Response
from starlette.staticfiles import StaticFiles
from starlette.types import Scope
import os

class CustomStatic(StaticFiles):
    """Extends the StaticFiles class to support the routing conventions used in this website"""

    def __init__(self, *, directory = None, packages = None, html = False, check_dir = True, follow_symlink = False, index: str = "index.html") -> None:
        self.index = index
        super().__init__(directory=directory, packages=packages, html=html, check_dir=check_dir, follow_symlink=follow_symlink)

    def lookup_path(self, path) -> tuple[str, os.stat_result | None]:
        """Super wrapper that returns index file if path cannot be found
        
        Args:
            path (str): Resource path
            
        Returns:
            tuple: Full path and stat results or None if the file was not found
        """
        full_path, stat_result = super().lookup_path(path)

        if stat_result == None:
            full_path, stat_result = super().lookup_path(self.index)
            return full_path, stat_result
        else:
            return full_path, stat_result

    async def get_response(self, path: str, scope: Scope) -> Response:
        """Adds cache-control headers for index.html"""

        # Treat root path as the index file
        if path in ["", "/", "."]:
            path = self.index
        
        return await super().get_response(path, scope)
