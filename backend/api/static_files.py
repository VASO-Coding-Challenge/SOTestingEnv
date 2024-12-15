"""This file is inspired by the csxl.unc.edu project, and aims to extend the static files class to support a statically built frontend"""

from fastapi.staticfiles import StaticFiles

class CustomStatic(StaticFiles):
    """Extends the StaticFiles class to support the routing conventions used in this website"""

    def __init__(self, *, directory = None, packages = None, html = False, check_dir = True, follow_symlink = False, index: str = "index.html") -> None:
        self.index = index
        super().__init__(directory=directory, packages=packages, html=html, check_dir=check_dir, follow_symlink=follow_symlink)
