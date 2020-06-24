from .version import VERSION
from .en2an import En2An

__version__ = VERSION

en2an = En2An().en2an

__all__ = [
    "__version__",
    "en2an"
]
