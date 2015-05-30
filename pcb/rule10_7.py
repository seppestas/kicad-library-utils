# -*- coding: utf-8 -*-

from rule import *
import os

class Rule10_7(KLCRule):
    """
    Create the methods check and fix to use with the kicad_mod files.
    """
    def __init__(self, module):
        super(Rule10_7, self).__init__('Rule 10.7', '3D Shape ".wrl" files are named the same as their footprint and are placed in a folder named the same as the footprint library replacing the ".pretty" with ".3dshapes".')

    def check(self, module):
        """
        Proceeds the checking of the rule.
        The following variables will be accessible after checking:
            * module_dir
            * model_dir
            * model_file
        """
        module_dir = os.path.split(os.path.dirname(module.filename))[-1]
        self.module_dir = os.path.splitext(module_dir)

        if len(module.models) == 0:
            return False
        elif len(module.models) > 1:
            return True

        model_file_path = module.models[0]['file']
        self.model_file = os.path.splitext(os.path.basename(model_file_path))
        model_dir = os.path.split(os.path.dirname(model_file_path))[-1]
        self.model_dir = os.path.splitext(model_dir)

        if (self.model_file[0] == module.name and
            self.model_file[1] == '.wrl' and
            self.model_dir[0] == self.module_dir[0] and
            self.model_dir[1] == '.3dshapes'):
            return False

        return True

    def fix(self, module):
        """
        Proceeds the fixing of the rule, if possible.
        """
        if self.check(module):
            if len(module.models) == 1:
                path = os.path.join(self.module_dir[0] + '.3dshapes', module.name + '.wrl')
                module.models[0]['file'] = path
            elif len(module.models) > 1:
                pass
                # TODO
