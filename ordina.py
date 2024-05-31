from pathlib import Path
for path in Path('c:/Users/ITFERON/OneDrive - ABB/python/ordensomeanse').rglob('*'):
#    print(path.suffix)
    if not path.is_dir:
        print(path)