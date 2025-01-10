from uvmono_ml_core import hello as ml_core_hello
from uvmono_core import hello as core_hello


IS_PROGRESS_BAR_ENABLED = None

try:
    from evaluate import is_progress_bar_enabled

    IS_PROGRESS_BAR_ENABLED = is_progress_bar_enabled()
except ImportError:
    print("Training deps not available")
    pass


def hello() -> str:
    return (
        f"Hello from uvmono-ml project! Progress bar enabled: {IS_PROGRESS_BAR_ENABLED}"
    )


print(hello())
