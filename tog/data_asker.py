from enum import Enum
from typing import Callable, Generic, Protocol, TypeVar, List


class AskVerb(Enum):
    Set: str = "set"
    Get: str = "get"


S = TypeVar("S")

Source = List[tuple[str, S]]


T = TypeVar("T")


class Resource(Generic[T]):

    def __init__(self, source: Callable[[], Source[T]], allow_custom: bool = True):
        self.populate_list: Callable[[], Source[T]] = source
        self.allow_custom = allow_custom
        self.values: Source[T] | None = None

    def get_values(self) -> Source[T]:
        if self.values is None:
            self.values = self.populate_list()

        return self.values


TA = TypeVar('TA')


class Asker():
    def ask(self, resource_list: Source[TA]) -> TA:
        self.__present_options(resource_list)
        pass

    def __promptOption(self, resource_list) -> (str, any):
        i = int(input())

        match i:
            case x if x < 0:
                raise (ValueError("Can't choose a negative option!"))
            case x if x >= len(resource_list):
                raise (ValueError("Value too large!"))
            case x:
                return resource_list[x]

    def __promptYN(self, prompt=None, defaultAccept=False):
        legend: str
        if defaultAccept:
            legend = "[Y/n]"
        else:
            legend = "[y/N]"
        prompt = prompt or "Please choose"

        while True:
            print(f"{prompt} {legend}: ", end="")
            match input().lower():
                case "": return defaultAccept
                case "y": return True
                case "n": return False
                case _:
                    print(f"I did not understand, could you please try again?\n")
                    continue

    def __present_options(self, resource_list: Source[TA]) -> TA:
        match resource_list:
            case []:
                print("No data found!")
                return None
            case [(desc, val)]:
                print(
                    f"Found '{desc}' ({val}), would you like to apply? [Y/n]: ")
                if self.__promptYN():
                    return val
                else:
                    return None
            case _:
                for i, (desc, val) in enumerate(resource_list):
                    print(f"[{i}] {desc} ({val})")

                print("\nFound multiple matches! Please select one: ")

                d, obj = self.__promptOption(resource_list)
                print(f"Choose {d}!")
                return obj


class DataAsker():
    """
    A class repsponsible for asking for information and keeping
    a cache for future use
    """

    def __init__(self):
        self.sources: dict[str, Resource[any]] = {}
        self.asker: Asker = Asker()

    def register_source(self, resource: str, source: Resource[any]):
        self.sources[resource] = source
        pass

    def ask(self, verb: AskVerb, object, resource):
        match verb:
            case AskVerb.Set:
                try:
                    values = self.sources[resource].get_values()
                    match self.asker.ask(values):
                        case None:
                            print("No action!")
                        case value:
                            raise NotImplementedError(
                                f"should probably set {value} on {object} somewhere")
                except KeyError as e:
                    raise (e)

            case AskVerb.Get:
                pass
