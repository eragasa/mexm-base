from abc import ABC
import os
import socket
import platform
import getpass

from mexm.exception import MexmUnsupportedOperationSystemError

class AbstractMexmUserInfo(ABC):

    @property
    def username(self) -> str:
        return getpass.getuser()

    @property
    def configuration_path(self) -> str:
        home_directory = os.path.expanduser("~") 
        os.path.join(home_directory, ".mexm-")
        return 

    @property
    def hostname(self) -> str:
        return socket.gethostname()


class WindowsMexmUserInfo(AbstractMexmUserInfo):
    pass

class LinuxMexmUserInfo(AbstractMexmUserInfo):
    pass

class MacMexmUserInfo(AbstractMexmUserInfo):
    pass

class MexmUserInfoFactory(AbstractMexmUserInfo):
    
    @staticmethod
    def get_object(self) -> AbstractMexmUserInfo:
        os_2_object_map = {
            'Linux': LinuxMexmUserInfo,
            'Mac': MacMexmUserInfo,
            'Windows': WindowsMexmUserInfo
        }

        os_type = platform.system()

        # raise error if not supported operating system type
        # if this error is raised then platform.system is returning an unsupported OS type
        if os_type not in  os_2_object_map:
            msg = '{} is not a supported operation system. '.format(os_type)
            msg += 'The supported OS types are '
            msg += ",".join(list(os_2_object_map.keys())) + "."
            raise MexmUnsupportedOperationSystemError(msg)

        return os_2_object_map[os_type]()

