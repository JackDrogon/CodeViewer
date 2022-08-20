# coding: utf-8

from .buffer import Buffer
from .symbol import Symbol
from .variable import Variable
from .utils import remove_anon, access_to_uml


# maybe to all function
class ClassFunction(Symbol):
    # {"_type": "tag", "name": "leveldb_filterpolicy_create_bloom::Wrapper::CreateFilter", "path": "db/c.cc", "pattern": "/^    void CreateFilter(const Slice* keys, int n, std::string* dst) const {$/", "file": true, "language": "C++", "typeref": "typename:void", "kind": "function", "access": "public", "signature": "(const Slice * keys,int n,std::string * dst) const", "scope": "leveldb_filterpolicy_create_bloom::Wrapper", "scopeKind": "struct"}
    def __init__(self, tag: dict) -> None:
        super().__init__(tag)
        scope = tag.get("scope", None)
        # if name startwiths scope, remove scope prefix
        if scope and self.name.startswith(scope):
            self.name = self.name[len(scope) + 2:]  # +2 is "::"
        self.scope = scope

        # typeref remove typename:
        self.typeref = tag.get("typeref", "")
        if self.typeref.startswith("typename:"):
            self.typeref = self.typeref[len("typename:"):]

        self.signature = tag.get("signature", "")

        # FIXME(Drogon): like Variable
        self.access = tag.get("access", "public")
        assert (self.access in ["private", "public", "protected"])

    def __str__(self) -> str:
        return f"{self.access} {self.typeref} {self.name}{self.signature}"

    def to_plantuml(self, buffer: Buffer) -> None:
        buffer << f"{access_to_uml(self.access)} {self.typeref} {self.name}{self.signature};"


class Class(Symbol):
    """
    scope = "", class is in global namespace
    """

    # {"_type":"tag","name":"BlockBuilder","path":"table/block_builder.h","pattern":"/^class BlockBuilder {$/","language":"C++","kind":"class","scope":"leveldb","scopeKind":"namespace"}
    def __init__(self, tag: dict) -> None:
        super().__init__(tag)
        self.variables = []
        self.functions = []
        self.inherits = set()
        self.scope = tag.get('scope', "")
        self.is_anon = None

        self.merge(tag)

    """
    function add inherit class
    tag: {"_type": "tag", "name": "T3", "path": "t1.h", "pattern": "/^class T3 : public T1, T2, map<string, int> {};$/", "language": "C++", "kind": "class", "inherits": "T1,T2,map<string,int>"}
    split by ','
    """

    def __add_inherits(self, tag: dict) -> None:
        inherit = tag.get("inherits", None)
        if inherit is None:
            return

        inherits = inherit.split(",")
        self.inherits.update(inherits)
        # for inherit in inherits:
        #     # remove cpp template <type>
        #     # self.inherit[i] = remove_anon(self.inherit[i])
        #     self.inherits.append(inherit)

    # split __init__ in merge by multipass, because some classes inherit from other class && with other
    # generated tag
    def merge(self, tag: dict) -> None:
        if self.is_anon is None:
            self.__maybe_fix_name()

        self.__add_inherits(tag)

    """fix the name of class"""

    def __maybe_fix_name(self):
        # if name not start with scope name, add scope name to the front
        # like DataFile leveldb::SpecialEnv::NewWritableFile => leveldb::SpecialEnv::NewWritableFile::Data
        if not self.name.startswith(self.scope):
            self.name = self.scope + "::" + self.name

        name = remove_anon(self.name)
        if name != self.name:
            self.is_anon = True
            self.name = name
        else:
            self.is_anon = False

    def __str__(self) -> str:
        buffer = Buffer()

        buffer << f"class: {self.name}"

        if len(self.inherits) > 0:
            buffer << "\n"
            buffer << f"inherits: [\n"
            for inherit in self.inherits:
                buffer << f"\t{inherit}\n"
            buffer << f"]"

        if len(self.variables) > 0:
            buffer << "\n"
            buffer << f"members: [\n"
            for variable in self.variables:
                buffer << f"\t{variable}\n"
            buffer << f"]"

        if len(self.functions) > 0:
            buffer << "\n"
            buffer << f"functions: [\n"
            for function in self.functions:
                buffer << f"\t{function}\n"
            buffer << f"]"

        return str(buffer)

    def add_function(self, tag: dict) -> None:
        self.functions.append(ClassFunction(tag))

    def add_variable(self, tag: dict) -> None:
        self.variables.append(Variable(tag))

    # to plantuml
    def to_plantuml(self, buffer: Buffer) -> None:
        buffer << f"class {self.name} {{\n"

        # append functions
        for f in self.functions:
            buffer << '\t'
            f.to_plantuml(buffer)
            buffer << '\n'

        # append variables
        if len(self.variables) > 0:
            if len(self.functions) != 0:
                buffer << '\n'
            for v in self.variables:
                buffer << '\t'
                v.to_plantuml(buffer)
                buffer << '\n'

        buffer << '}'
