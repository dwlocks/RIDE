#  Copyright 2008-2011 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os

from robotide.controller.commands import FindOccurrences, _Command
from robotide.controller.macrocontrollers import KeywordNameController


class FindUsages(FindOccurrences):

    def execute(self, context):
        prev = None
        for occ in FindOccurrences.execute(self, context):
            if isinstance(occ.item, KeywordNameController):
                continue
            if prev == occ:
                prev.count += 1
            else:
                if prev:
                    yield prev
                prev = occ
        if prev:
            yield prev

class FindResourceUsages(_Command):

    def execute(self, context):
        for df in context.datafiles:
            if not hasattr(df, 'imports'):
                continue
            for import_ in df.imports:
                if import_.is_resource and \
                    context == import_.get_imported_resource_file_controller():
                    yield ResourceUsage(df)

class ResourceUsage(object):

    count = 1

    def __init__(self, user):
        self._user = user
        self.location = user.display_name
        self.usage = 'import'
        self.source = user.source
        self.parent = user.imports
        self.item = user.imports
