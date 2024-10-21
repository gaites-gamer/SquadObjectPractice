# layer.py


# Zero's Col names below....
# Level,Layer,Size,
# Faction_1,SubFac_1,Logistics_1,Transportation_1,Anti-Infantry_1,Armor_1,ZERO_Score_1,
# Faction_2,SubFac_2,Logistics_2,Transportation_2,Anti-Infantry_2,Armor_2,ZERO_Score_2,
# Balance_Differential,Asymmetry Score

class Team:
    def __init__(
            self,
            faction: str = 'Unknown',
            subfaction: str = 'Unknown',
            logistics: float = 0.0,
            transportation: float = 0.0,
            anti_infantry: float = 0.0,
            armor: float = 0.0,
            zero_score: float = 0.0
    ):
        self.faction: str = faction
        self.subfaction: str = subfaction
        self.logistics: float = logistics
        self.transportation: float = transportation
        self.anti_infantry: float = anti_infantry
        self.armor: float = armor
        self.zero_score: float = zero_score

    def __str__(self) -> str:
        return f'{self.faction}+{self.subfaction}'

    def dictMe(self) -> dict:
        return {
            'Faction': self.faction,
            'SubFaction': self.subfaction,
            'Logistics': self.logistics,
            'Transportation': self.transportation,
            'AntiInfantry': self.anti_infantry,
            'Armor': self.armor,
            'ZeroScore': self.zero_score
        }


class Layer:
    def __init__(
            self,
            setcode: str = 'Unknown',
            map: str = 'Unknown',
            gamemode: str = 'Unknown',
            version: str = 'v1',
            team1: Team = None,
            team2: Team = None,
            balance_differential: float = 0.0,
            asymmetry_score: float = 0.0
    ):
        self._setcode: str = setcode
        self.map: str = map
        self.gamemode: str = gamemode
        self.version: str = version
        self.team1: Team = team1 if team1 is not None else Team()
        self.team2: Team = team2 if team2 is not None else Team()
        self.balance_differential: float = balance_differential
        self.asymmetry_score: float = asymmetry_score

    def __str__(self):
        return f'{self.map}_{self.gamemode}_'

    def dictMe(self) -> dict:
        return {
            'Setcode': self.setcode,
            'Map': self.map,
            'Gamemode': self.gamemode,
            "Version": self.version,
            "Team1": self.team1.dictMe(),
            "Team2": self.team2.dictMe(),
            "Balance_Differential": self.balance_differential,
            "Asymmetry_Score": self.asymmetry_score
        }

    @property
    def setcode(self) -> str:
        # This property generates the setcode value on-demand
        if self._setcode == 'Unknown':
            self._setcode = (
                f'{self.map}_{self.gamemode}_{self.version} '
                f'{self.team1.faction}+{self.team1.subfaction} '
                f'{self.team2.faction}+{self.team2.subfaction}'
            )
        return self._setcode
