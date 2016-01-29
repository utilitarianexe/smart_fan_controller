import json

class Profile():
    '''
    Basically holds all the state infomration for the fan
    '''
    profile_file_name = '/home/pi/smart_fan/profile_info'
    reset_profile_file_name = '/home/pi/smart_fan/profile_info_default'
    def __init__(self):
        self.import_state(Profile.profile_file_name)

    def hard_reset(self):
        self.import_state(Profile.reset_profile_file_name)

    def export(self):
        data = {}
        for attr, value in self.__dict__.items():
            if value is None:
                data[attr] = 'unknown'
            else:
                data[attr] = value

        return data

    def import_data(self, profile_info):
        for key, value in profile_info.items():
            if value == "unknown":
                value = None
            setattr(self, key, value)

    def save_state(self):
        with open(Profile.profile_file_name, 'w') as profile_file:
            json.dump(self.export(), profile_file)

    def import_state(self, location):
        with open(location, 'r') as profile_file:
            profile_info = json.load(profile_file)
        self.import_data(profile_info)
        

profile = Profile()

if __name__ == '__main__':
    profile.export_as_json()
