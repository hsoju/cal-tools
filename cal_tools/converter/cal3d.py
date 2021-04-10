import argparse
from pathlib import Path
from cal_tools.converter.base import CalConverter
from cal_tools.loader.mesh import CalMeshLoader
from cal_tools.exporter.cal3d.xmf import XmfExporter


class CalMeshConverter(CalConverter):
    def __init__(self):
        super().__init__(CalMeshLoader(), XmfExporter())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()
    extension = Path(args.input).suffix
    if extension.lower() == '.xmf':
        converter = CalMeshConverter()
        converter.convert(args.input, args.output)
    else:
        print('Invalid file')
        exit()
