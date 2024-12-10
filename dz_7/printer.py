from common import FileObject

"""
    This thing accepts template where %field% is replaced with actuall value.
    However, we do need to support different templates for different gender
    Soooooo the easiest solution is to use %gender_ending% to add for female for right now
    In real life I would do two templates one for each gender
"""
class TemplatePrinter(FileObject):
    def __init__(self, file_name, template, row_formatter):
        super().__init__(file_name, "w")
        self.template = template
        self.__row_formatter = row_formatter
        self.__internal_template = []
        self.__subst_template = []
        self.__build_template()

    def __build_template(self):
        # The most difficult function here. We find % and not %% and find closing one %
        # Not really effective work with the strings, I would not write this logic in Python in real life
        prev_pos = 0
        cur_inside = False
        i = 0
        while i < len(self.template):
            if self.template[i] != "%":
                pass
            elif self.template[i] == "%" and i + 1 < len(self.template) and self.template[i + 1] == "%":
                i += 1
            else:
                if cur_inside == False:
                    self.__internal_template.append(self.template[prev_pos:i])
                    prev_pos = i
                    cur_inside = True
                else:
                    self.__internal_template.append(None)
                    self.__subst_template.append(self.template[prev_pos + 1:i])
                    prev_pos = i + 1
                    cur_inside = False
            i += 1
        # final part can only be outside
        if cur_inside == False:
            self.__internal_template.append(self.template[prev_pos:i])
        else:
            raise ValueError("Invalid template")

    def write(self, data):
        final_string = ""
        j = 0
        for part in self.__internal_template:
            if part is not None:
                final_string += part
            else:
                field = self.__subst_template[j]
                if field == "gender_ending":
                    if data["sex"] == "female":
                        final_string += "а"
                else:
                    if field not in data:
                        raise ValueError(f"{data} missing field {field}")
                    final_string += self.__row_formatter(field, data[field])
                j += 1
        final_string += "\n"
        self._file.write(final_string)
