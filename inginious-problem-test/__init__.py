# Inginious-problem-test

import os

from inginious.common.tasks_problems import Problem
from inginious.frontend.task_problems import DisplayableProblem
from inginious.frontend.parsable_text import ParsableText

PATH_TO_PLUGIN = os.path.abspath(os.path.dirname(__file__))
PATH_TO_TEMPLATES = os.path.join(PATH_TO_PLUGIN, "templates")

class TestProblem(Problem):
    """Add a different test set, using code from another problem"""

    def __init__(self, problemid, content, translations, taskfs):
        super(TestProblem, self).__init__(problemid, content, translations, taskfs)
        self._header = content['header'] if "header" in content else ""
        self._optional = True

    @classmethod
    def get_type(cls):
        return "extra_test"

    def input_is_consistent(self, task_input, default_allowed_extension, default_max_size):
        return True

    def input_type(self):
        return None

    def check_answer(self, _, __):
        return None, None, None, 0, ""

    @classmethod
    def parse_problem(self, problem_content):
        return Problem.parse_problem(problem_content)

    @classmethod
    def get_text_fields(cls):
        fields = Problem.get_text_fields()
        fields.update({"header": True})
        return fields

class DisplayableTestProblem(TestProblem, DisplayableProblem):
    """ A displayable match problem """

    def __init__(self, problemid, content, translations, taskfs):
        super(DisplayableTestProblem, self).__init__(problemid, content, translations, taskfs)

    @classmethod
    def get_type_name(cls, language):
        return _("extra_test")

    def show_input(self, template_helper, language, seed):
        """ Show Extra test """
        header = ParsableText(self.gettext(language, self._header), "rst",
                              translation=self.get_translation_obj(language))
        return template_helper.render("extra_test.html", template_folder=PATH_TO_TEMPLATES,
                                      inputId=self.get_id(), header=header)

    @classmethod
    def show_editbox(cls, template_helper, key, language):
        return template_helper.render("extra_test_edit.html",
                                      template_folder=PATH_TO_TEMPLATES,
                                      key=key)

    @classmethod
    def show_editbox_templates(cls, template_helper, key, language):
        return ""

class StaticMockPage(object):
    # TODO: Replace by shared static middleware and let webserver serve the files
    def GET(self, path):
        if not os.path.abspath(PATH_TO_PLUGIN) in os.path.abspath(os.path.join(PATH_TO_PLUGIN, path)):
            raise web.notfound()

        try:
            with open(os.path.join(PATH_TO_PLUGIN, "static", path), 'rb') as file:
                return file.read()
        except:
            raise web.notfound()

    def POST(self, path):
        return self.GET(path)

def init(plugin_manager, course_factory, client, plugin_config):
    plugin_manager.add_page('/plugins/extra_test/static/(.+)', StaticMockPage)
    plugin_manager.add_hook("javascript_header", lambda: "/plugins/extra_test/static/extra_test.js")
    course_factory.get_task_factory().add_problem_type(DisplayableTestProblem)
