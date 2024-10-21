# csvConvert.py
# Revision v0.02 - Oct, 2024
# Purpose: Convert Zero's CSV Output File to a JSON File of Layer Objects

import pandas as pd
import json
from layer import Layer, Team


def getTeamData(row: pd.Series, team_config: dict) -> Team:
    faction = row[team_config['faction']]
    subfaction = row[team_config['subfaction']]
    values = [
        round(float(row[attr]), 2)
        for attr in team_config['numerical_attributes']
    ]
    return Team(faction, subfaction, *values)


def getLayerProperties(row: pd.Series, layer_attributes: dict) -> tuple[str, str, str]:
    map_name = row[layer_attributes['map']]
    layer_data = row[layer_attributes['gamemode']]
    layer_properties = layer_data.split('_')
    gamemode = layer_properties[1] if len(layer_properties) > 1 else 'Unknown'
    version = layer_properties[2] if len(layer_properties) > 2 else 'v1'
    return map_name, gamemode, version


def convertZeroFile(csv_filepath: str,
                    json_filepath: str,
                    team1_config: dict,
                    team2_config: dict,
                    layer_attributes: dict) -> None:
    print('Opening Zeros File...')
    data_frame = pd.read_csv(csv_filepath)
    print(f'Processing {data_frame.shape[0]} Layers!')

    data_frame['team1'] = data_frame.apply(lambda row: getTeamData(row, team1_config), axis=1)
    data_frame['team2'] = data_frame.apply(lambda row: getTeamData(row, team2_config), axis=1)
    data_frame[['map_name', 'gamemode', 'version']] = data_frame.apply(
        lambda row: pd.Series(getLayerProperties(row, layer_attributes)), axis=1
    )

    layers = data_frame.apply(
        lambda row: Layer(
            map=row['map_name'],
            gamemode=row['gamemode'],
            version=row['version'],
            team1=row['team1'],
            team2=row['team2'],
            balance_differential=round(float(row[layer_attributes['balance_differential']]), 2),
            asymmetry_score=round(float(row[layer_attributes['asymmetry_score']]), 2)
        ), axis=1
    ).tolist()

    layers_dict = [layer.dictMe() for layer in layers]
    print(f'Converted {len(layers)} layers.')
    with open(json_filepath, mode='w') as json_file:
        json.dump(layers_dict, json_file, indent=4)


if __name__ != "__main__":
    pass
else:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    convertZeroFile(
        'data/layer_pool.csv',
        'data/layer_pool.json',
        team1_config=config['team1_attributes'],
        team2_config=config['team2_attributes'],
        layer_attributes=config['layer_attributes']
    )
