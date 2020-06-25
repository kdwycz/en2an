from .version import VERSION
from .en2an import En2An
from .an2en import An2En

__version__ = VERSION

en2an = En2An().en2an
an2en = An2En().an2en

__all__ = [
    "__version__",
    "en2an",
    "an2en"
]
