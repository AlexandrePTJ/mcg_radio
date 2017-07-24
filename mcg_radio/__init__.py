import json


class Settings:
    radios = []
    current_index = 0
    settings_path = 'mcg_radios.json'

    def read(self):
        with open(self.settings_path) as f:
            data = json.load(f)
        self.radios = data['radios']
        self.current_index = data['current_index']

    def save(self):
        data = dict()
        data['radios'] = self.radios
        data['current_index'] = self.current_index

        with open(self.settings_path, "w") as f:
            json.dump({
                'radios': self.radios,
                'current_index': self.current_index},
                f, indent=4)
