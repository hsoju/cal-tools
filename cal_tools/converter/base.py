from pathlib import Path
from cal_tools.loader.base import CalLoader
from cal_tools.exporter.base import CalExporter


class CalConverter:
    def __init__(self, loader: CalLoader, exporter: CalExporter):
        self.loader = loader
        self.exporter = exporter

    def convert(self, input_filepath: str, output_filepath: str = None):
        cal_object = self.loader.load(input_filepath)
        if output_filepath:
            self.exporter.export(output_filepath, cal_object)
        else:
            output_filepath = Path(input_filepath).with_suffix(self.exporter.extension)
            self.exporter.export(str(output_filepath), cal_object)
