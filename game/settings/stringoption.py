from dataclasses import dataclass, field
from typing import Any, Optional

from .optiondescription import OptionDescription, SETTING_DESCRIPTION_KEY


@dataclass(frozen=True)
class StringOption(OptionDescription):
    invert: str


def string_option(
    text: str,
    page: str,
    section: str,
    default: str,
    invert: str = "",
    detail: Optional[str] = None,
    tooltip: Optional[str] = None,
    causes_expensive_game_update: bool = False,
    remember_player_choice: bool = False,
    **kwargs: Any,
) -> bool:
    return field(
        metadata={
            SETTING_DESCRIPTION_KEY: StringOption(
                page,
                section,
                text,
                detail,
                tooltip,
                causes_expensive_game_update,
                remember_player_choice,
                invert,
            )
        },
        default=default,
        **kwargs,
    )

