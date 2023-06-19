# coding: utf-8

from .buffer import Buffer
from .symbol import Symbol
from .utils import access_to_uml


class Variable(Symbol):
    """ validation guaranteed by caller, no need to validate
    """

    # {"_type": "tag", "name": "leveldb::VersionEdit::deleted_files_", "path": "db/version_edit.h", "pattern": "/^  DeletedFileSet deleted_files_;$/", "language": "C++", "typeref": "typename:DeletedFileSet", "kind": "member", "access": "private", "scope": "leveldb::VersionEdit", "scopeKind": "class"}
    def __init__(self, tag: dict) -> None:
        super().__init__(tag)
        scope = tag.get("scope", None)
        self.scope = scope
        # if name startwiths scope, remove scope prefix
        if scope and self.name.startswith(scope):
            self.name = self.name[len(scope) + 2:]  # +2 is "::"

        # typeref remove typename:
        self.typeref = tag.get("typeref", "")
        if self.typeref.startswith("typename:"):
            self.typeref = self.typeref[len("typename:"):]

        # FIXME(Drogon):
        # {"_type": "tag", "name": "leveldb::CacheTest::current_", "path": "util/cache_test.cc", "pattern": "/^  static CacheTest* current_;$/", "file": true, "language": "C++", "typeref": "typename:CacheTest *", "kind": "member", "access": "public", "scope": "leveldb::CacheTest", "scopeKind": "class"}
        # {"_type": "tag", "name": "leveldb::CacheTest::current_", "path": "util/cache_test.cc", "pattern": "/^CacheTest* CacheTest::current_;$/", "language": "C++", "typeref": "typename:CacheTest *", "kind": "member", "scope": "leveldb::CacheTest", "scopeKind": "class"}
        # class CacheTest : public testing::Test {
        #   static CacheTest* current_;
        # }
        # CacheTest* CacheTest::current_;
        # when meet class static function/variable, we will see multi tag from unversial ctags, check merge && see static tag
        self.access = tag.get("access", "public")
        assert (self.access in ["private", "public", "protected"])

    def __str__(self) -> str:
        return f"{self.access} {self.typeref} {self.name}"

    def to_plantuml(self, buffer: Buffer) -> None:
        buffer << f"{access_to_uml(self.access)} {self.typeref} {self.name};"
