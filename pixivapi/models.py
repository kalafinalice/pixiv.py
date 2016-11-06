from __future__ import print_function

class ResultSet(list):

    def __init__(self, page=None):
        super(ResultSet, self).__init__()
        self._page = page

    def ids(self):
        return [item.id for item in self if hasattr(item, 'id')]

class Model(object):

    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        pickle = dict(self.__dict__)
        try:
            del pickle['_api']
        except KeyError:
            pass
        return pickle

    @classmethod
    def parse(cls, api, json):
        raise NotImplementedError

    @classmethod
    def parse_list(cls, api, json_list):
        results = ResultSet()
        for obj in json_list:
            if obj:
                results.append(cls.parse(api, obj))
        return results

    def __repr__(self):
        state = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))

class JSONModel(Model):

    @classmethod
    def parse(cls, api, json):
        return json

# Pixiv Public API Model
class Work(Model):

    @classmethod
    def parse(cls, api, json):
        work = cls(api)
        setattr(work, '_json', json)
        for k, v in json.items():
            if k == 'user':
                setattr(work, k, User.parse(api, v))
            elif k == 'metadata':
                if v:
                    setattr(work, k, Metadata.parse(api, v))
                else:
                    setattr(work, k, v)
            else:
                setattr(work, k, v)
        return work

    def __eq__(self, other):
        if isinstance(other, Work):
            return self.id == other.id

        return NotImplemented

    def __ne__(self, other):
        result = self == other

        if result is NotImplemented:
            return result

        return not result

class User(Model):

    @classmethod
    def parse(cls, api, json):
        user = cls(api)
        for k, v in json.items():
            if k == 'profile':
                if v:
                    setattr(user, k, Profile.parse(api, v))
                else:
                    setattr(user, k, v)
            else:
                setattr(user, k, v)
        return user

class Metadata(Model):

    @classmethod
    def parse(cls, api, json):
        metadata = cls(api)
        for k, v in json.items():
            setattr(metadata, k, v)
        return metadata

class Profile(Model):

    @classmethod
    def parse(cls, api, json):
        profile = cls(api)
        for k, v in json.items():
            setattr(profile, k, v)
        return profile

class ModelFactory(object):

    work = Work
    user = User

    json = JSONModel

# Pixiv App API Model
class AppIllust(Model):

    @classmethod
    def parse(cls, api, json):
        illust = cls(api)
        setattr(illust, '_json', json)
        for k, v in json.items():
            if k == 'user':
                setattr(illust, k, AppUser.parse(api, v))
            else:
                setattr(illust, k, v)
        return illust

    @classmethod
    def parse_list(cls, api, json_list):
        results = ResultSet()
        for obj in json_list['illusts']:
            if obj:
                results.append(cls.parse(api, obj))
        return results

    def __eq__(self, other):
        if isinstance(other, AppIllust):
            return self.id == other.id

        return NotImplemented

    def __ne__(self, other):
        result = self == other

        if result is NotImplemented:
            return result

        return not result

class AppUser(Model):

    @classmethod
    def parse(cls, api, json):
        user = cls(api)
        for k, v in json.items():
            if k == 'user':
                setattr(user, k, AppUser.parse(api, v))
            elif k == 'profile':
                setattr(user, k, AppProfile.parse(api, v))
            elif k == 'workspace':
                setattr(user, k, AppWorkspace.parse(api, v))
            else:
                setattr(user, k, v)
        return user

class AppProfile(Model):

    @classmethod
    def parse(cls, api, json):
        profile = cls(api)
        for k, v in json.items():
            setattr(profile, k, v)
        return profile

class AppWorkspace(Model):

    @classmethod
    def parse(cls, api, json):
        workspace = cls(api)
        for k, v in json.items():
            setattr(workspace, k, v)
        return workspace

class AppMetadata(Model):

    @classmethod
    def parse(cls, api, json):
        metadata = cls(api)
        for k, v in json.items():
            setattr(metadata, k, v)
        return metadata

class AppComment(Model):

    @classmethod
    def parse(cls, api, json):
        comment = cls(api)
        for k, v in json.items():
            if k == 'user':
                setattr(comment, k, AppUser.parse(api, v))
            else:
                setattr(comment, k, v)
        return comment

    @classmethod
    def parse_list(cls, api, json_list):
        results = ResultSet()
        for obj in json_list['comments']:
            if obj:
                results.append(cls.parse(api, obj))
        return results

class AppAutoComplete(Model):

    @classmethod
    def parse(cls, api, json):
        auto_complete = cls(api)
        for k, v in json.items():
            setattr(auto_complete, k, v)
        return auto_complete

class AppModelFactory(object):

    app_illust = AppIllust
    app_user = AppUser

    app_comment = AppComment
    app_metadata = AppMetadata
    app_auto_complete = AppAutoComplete

    json = JSONModel
