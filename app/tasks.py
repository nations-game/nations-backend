from flask_apscheduler import APScheduler
from flask import Flask

from .database import database_instance as database
from .database.models import Nation, FactoryType, NationFactory

from .utils.math import clamp

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

                factory: NationFactory
                for factory in nation.factories:
                    factory_type = database.get_factory_type_by_id(factory.factory_id)
                    '''
                    match factory_type.commodity:
                        case "food":
                            nation.food += factory_type.production * factory_type.current_level
                            break
                        case "consumer_goods":
                            nation.consumer_goods += factory_type.production * factory_type.current_level
                            break
                        case "power":
                            nation.consumer_goods += factory_type.production * factory_type.current_level
                            break
                    '''
                    factory.production_resources += factory_type.production * factory_type.current_level
                    factory.production_resources = clamp(factory.production_resources, 24, 0)
                
                # Decrease food, power, and consumer goods according to population
                nation.food -= nation.population / 3
                nation.power -= nation.population / 6
                nation.consumer_goods -= nation.population / 4

                nation.food = max(nation.food, 0)
                nation.power = max(nation.power, 0)
                nation.consumer_goods = max(nation.consumer_goods, 0)

                nation.happiness = 50

                if nation.consumer_goods % nation.population > 0:
                    nation.happiness *= 1.15
                
                if nation.power % nation.population > 0:
                    nation.happiness *= 1.20

                if nation.food <= 0:
                    nation.happiness = 0

                # Taxes
                # Base tax is calculated by diving population by 1000 so that there will almost always be an okay amount
                base_tax = nation.population / 1000
                
                # Happiness tax is the tax paid when citizens are happy. :)
                happiness_tax = nation.happiness * 10

                nation.money += base_tax + happiness_tax


            

            database.session.commit()


        self.scheduler.start()