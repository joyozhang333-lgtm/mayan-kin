#!/usr/bin/env python3
"""Core Mayan Kin calculation logic.

Backwards-compatible facade. The implementation now lives in sibling
modules (constants, styling, calculations, profiles, presentation,
analysis, reports). This module re-exports everything so existing imports
— ``from mayan_kin.core import X`` and ``from mayan_kin import core`` —
keep working unchanged.
"""

from .knowledge import (  # noqa: F401
    build_auto_plan,
    load_knowledge_index,
    recommend_knowledge_cards,
    recommend_report_mode,
    recommend_report_style,
    route_query,
)
from .constants import *  # noqa: F401,F403
from .styling import *  # noqa: F401,F403
from .calculations import *  # noqa: F401,F403
from .profiles import *  # noqa: F401,F403
from .presentation import *  # noqa: F401,F403
from .analysis import *  # noqa: F401,F403
from .reports import *  # noqa: F401,F403
