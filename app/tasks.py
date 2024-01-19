from celery import Celery


class CeleryTasks(Celery):
    def __init__(self, main: str, broker: str, database):
        super().__init__(
            main, 
            broker=broker, 
            task_always_eager=True
        )

        self.database = database
        
        @self.task
        async def give_income(self):
            ...