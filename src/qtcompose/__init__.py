try:
    from qtcompose._version import __version__, __version_tuple__  # type: ignore
except ImportError:
    __version__, __version_tuple__ = None, None


__all__ = ["__version__", "__version_tuple__"]
