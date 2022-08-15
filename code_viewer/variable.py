# coding: utf-8

from .symbol import Symbol


class Variable(Symbol):

    # {"_type": "tag", "name": "leveldb::VersionEdit::deleted_files_", "path": "db/version_edit.h", "pattern": "/^  DeletedFileSet deleted_files_;$/", "language": "C++", "typeref": "typename:DeletedFileSet", "kind": "member", "access": "private", "scope": "leveldb::VersionEdit", "scopeKind": "class"}
    def __init__(self, tag: dict) -> None:
        super().__init__(tag)
        scope = tag.get("scope", None)
        # if name startwiths scope, remove scope prefix
        if scope and self.name.startswith(scope):
            self.name = self.name[len(scope) + 2:]  # +2 is "::"

        # typeref remove typename:
        self.typeref = tag.get("typeref", "")
        if self.typeref.startswith("typename:"):
            self.typeref = self.typeref[len("typename:"):]

        # access uml tag
        access = tag.get("access", "")
        if access == 'private':
            self.access = '-'
        elif access == 'protected':
            self.access = '#'
        else:
            self.access = '+'

    def __str__(self) -> str:
        return f"{self.access} {self.typeref} {self.name}"
