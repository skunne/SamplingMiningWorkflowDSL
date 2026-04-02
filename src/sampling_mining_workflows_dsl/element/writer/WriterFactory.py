from sampling_mining_workflows_dsl.element.writer.JsonWriter import JsonWriter


class WriterFactory:
    @staticmethod
    def json_writer(path: str):
        return JsonWriter(path)
