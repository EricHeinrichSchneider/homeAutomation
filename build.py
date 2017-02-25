from pybuilder.core import init, use_plugin, Author


use_plugin("filter_resources")

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

default_task = "publish"

version = "0.0.1"
summary = "Server running on a Raspberry PI for Home Automation"
description = __doc__
authors = (Author("Eric Schneider", "eric.h.schneider@gmx.de"),)
url = "https://github.com/EricHeinrichSchneider/homeAutomationServer.git"
license = "Apache Software License"
@init
def initialize(project):
    project.build_depends_on('mockito')
    project.get_property('filter_resources_glob').append('**/util/__init__.py')
