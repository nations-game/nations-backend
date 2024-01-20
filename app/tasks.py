from flask_apscheduler import APScheduler
from flask import Flask

from .database import database_instance as database
from .database.models import Nation, FactoryType

class TaskHandler:
    def __init__(self, flask_app: Flask) -> None:
        self.flask_app = flask_app

        self.scheduler = APScheduler()
        self.scheduler.init_app(self.flask_app)

        # Nation tick
        @self.scheduler.task("interval", id="do_tick", seconds=30, misfire_grace_time=900)
        def do_tick():
            print("Performing tick...")
            all_nations = database.get_all_nations()

            nation: Nation
            # Placeholder values
            for nation in all_nations:
                print(nation.factories)
                # Increase population by 5% each tick
                nation.population *= 1.05

                nation.happiness = 100

                if nation.consumer_goods < 0:
                    nation.happiness -= 20

                if nation.food < 0:
                    nation.happiness = 0

                # Increase money from taxes, 10 money from each member of population * 0.7
                nation.money += 10 * (nation.population * 0.7 * (nation.happiness / 100))

                factory: FactoryType
                for factory in nation.factories:
                    match factory.commodity:
                        case "food":
                            nation.food += factory.production * factory.current_level
                            break
                        case "consumer_goods":
                            nation.consumer_goods += factory.production * factory.current_level
                            break
                
                # Decrease food, power, and consumer goods according to population
                nation.food -= nation.population / 3
                nation.power -= nation.population / 6
                nation.consumer_goods -= nation.population / 4

                nation.food = max(nation.food, 0)
                nation.power = max(nation.power, 0)
                nation.consumer_goods = max(nation.consumer_goods, 0)
            

            database.session.commit()


        self.scheduler.start()