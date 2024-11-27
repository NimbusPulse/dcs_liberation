from dataclasses import dataclass, asdict
from typing import List, Optional
from uuid import UUID
import httpx


@dataclass
class DcsCredentials:
    username: str
    password: str


@dataclass
class DcsSettingsPayload:
    initial_server_name: str
    initial_server_password: str
    initial_max_players: int
    use_own_credentials: bool
    credentials: Optional[DcsCredentials]
    initial_use_voice_chat: bool


@dataclass
class CreateInstanceRequest:
    user_id: str
    product_id: UUID
    settings: DcsSettingsPayload
    active_mods: List[str]
    wanted_terrains: List[str]


class Client:
    BASE_URL = "https://coordinator.nimbuspulse.com"

    def __init__(self, api_key: str):
        """
        Initialize the Client instance.
        """
        self.api_key = api_key
        self.client = httpx.Client()

    def set_api_key(self, api_key: str):
        """
        Set the API key for authentication.
        """
        self.api_key = api_key

    def create_server(
        self,
        name: str,
        password: Optional[str],
        max_players: int,
        plan: UUID,
        active_mods: List[str],
        terrains: List[str],
        credentials: Optional[DcsCredentials],
        use_voice_chat: bool,
    ) -> dict:
        """
        Create a new game server.
        
        Args:
            name (str): Name of the server.
            password (Optional[str]): Password for the server.
            max_players (int): Maximum number of players allowed.
            plan (UUID): Plan identifier for the server.
            active_mods (List[str]): List of active mods.
            terrains (List[str]): List of terrains to use.
            credentials (Optional[DcsCredentials]): Optional credentials for the server.
            use_voice_chat (bool): Whether to enable voice chat.

        Returns:
            dict: Response from the server.
        """
        payload = CreateInstanceRequest(
            user_id="",  # Adjust user_id assignment as needed.
            product_id=plan,
            settings=DcsSettingsPayload(
                initial_server_name=name,
                initial_server_password=password or "",
                initial_max_players=max_players,
                use_own_credentials=bool(credentials),
                credentials=credentials,
                initial_use_voice_chat=use_voice_chat,
            ),
            active_mods=active_mods,
            wanted_terrains=terrains,
        )
        response = self.client.post(
            f"{self.BASE_URL}/game_servers",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=asdict(payload),  # Serialize the payload using asdict
        )
        if response.status_code != 201:
            raise Exception(f"Failed to create server: {response.text}")

        return response.json()

    def get_servers(self) -> List[dict]:
        """
        Retrieve the list of existing servers.

        Returns:
            List[dict]: List of server details.
        """
        response = self.client.get(
            f"{self.BASE_URL}/game_servers",
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve servers: {response.text}")

        return response.json()
