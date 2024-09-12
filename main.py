from repository.csv_repository import write_to_csv
from repository.json_repository import *
from service.mission_service import *


def main():
    aircrafts = load_aircrafts_from_json('./repository/files/aircrafts.json')
    print('Aircrafts: ', aircrafts)

    pilots = load_pilots_from_json('./repository/files/pilots.json')
    print('Pilots :', pilots)

    targets = load_targets_from_json('./repository/files/targets.json')
    print('Targets :', targets)

    targets_with_location_and_weather: List[Target] = pipe(
        targets,
        partial(map, update_target_distance),
        partial(map, update_target_weather_score),
        list
    )
    print('Targets with location and weather :', targets_with_location_and_weather)

    all_missions = generate_mission_combinations(targets, aircrafts, pilots)
    print('All missions', all_missions)

    recommended_missions = get_recommended_missions(all_missions)
    print('Recommended missions :', recommended_missions)

    write_to_csv(recommended_missions, './repository/files/missions.csv')


if __name__ == '__main__':
    main()
