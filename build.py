#   -*- coding: utf-8 -*-

"""
CSCE 425/825 Semester Project
Project 4: Code Generation

Author: Robert Dyer <rdyer@unl.edu>
"""

import glob
import os
import shutil
import sys
from pybuilder.core import use_plugin, init, task, depends, description, Author
from pybuilder.plugins.core_plugin import compile_sources

use_plugin('python.core')
use_plugin('python.flake8')


name = '425project'
version = '4'
authors = (Author('Robert Dyer', 'rdyer@unl.edu'))
default_task = 'project4'


@init
def set_properties(project):
    project.depends_on('antlr4-python3-runtime', '==4.13.0')
    project.depends_on('debugpy')

    project.build_depends_on('flake8')
    project.set_property('flake8_break_build', True)

def verifytask(project, logger):
    inputfile=project.get_property('inputfile')
    inputstr=project.get_property('inputstr')

    if inputfile is None and inputstr is None:
        logger.error('You must specify the input file to compile, using: pyb projectN -P inputfile=<file path>')
        logger.error('or specify the input string to compile, using: pyb projectN -P inputstr="<source code>"')
        sys.exit(-1)

    return (inputfile, inputstr)

def setuptask(reactor):
    sys.path.append('src/main/python')
    sys.path.append('gen/src/antlr')

    venv = reactor.python_env_registry["build"]
    for p in venv.site_paths:
        sys.path.append(p)

@task
@depends(compile_sources)
@description('re-runs ANTLR')
def antlr(project, logger, reactor):
    import subprocess
    subprocess.call(['sh', './antlr-gen.sh'])

def debug(project):
    if project.get_property('debug'):
        import debugpy
        debugpy.listen(5678)
        debugpy.wait_for_client()
        debugpy.breakpoint()

@task
@depends(antlr)
@description('runs project 1 on an input (-P inputfile=<file>) or a string (-P inputstr="<code>")')
def project1(project, logger, reactor):
    (inputfile, inputstr) = verifytask(project, logger)
    setuptask(reactor)

    print('------------------------------------------------------------')
    print('COMPILER OUTPUT START')
    print('------------------------------------------------------------')

    debug(project)
    from project1 import main
    main(logger, inputfile=inputfile, inputstr=inputstr)

    print('------------------------------------------------------------')
    print('COMPILER OUTPUT END')
    print('------------------------------------------------------------')

@task
@depends(antlr)
@description('runs project 2 on an input (-P inputfile=<file>) or a string (-P inputstr="<code>")')
def project2(project, logger, reactor):
    (inputfile, inputstr) = verifytask(project, logger)
    setuptask(reactor)

    print('------------------------------------------------------------')
    print('COMPILER OUTPUT START')
    print('------------------------------------------------------------')

    debug(project)
    from project2 import main
    main(logger, inputfile=inputfile, inputstr=inputstr)

    print('------------------------------------------------------------')
    print('COMPILER OUTPUT END')
    print('------------------------------------------------------------')

@task
@depends(antlr)
@description('runs project 3 on an input (-P inputfile=<file>) or a string (-P inputstr="<code>")')
def project3(project, logger, reactor):
    (inputfile, inputstr) = verifytask(project, logger)
    setuptask(reactor)

    print('------------------------------------------------------------')
    print('COMPILER OUTPUT START')
    print('------------------------------------------------------------')

    debug(project)
    from project3 import main
    main(logger, inputfile=inputfile, inputstr=inputstr)

    print('------------------------------------------------------------')
    print('COMPILER OUTPUT END')
    print('------------------------------------------------------------')

@task
@depends(antlr)
@description('runs project 4 on an input (-P inputfile=<file>) or a string (-P inputstr="<code>")')
def project4(project, logger, reactor):
    (inputfile, inputstr) = verifytask(project, logger)
    setuptask(reactor)

    print('------------------------------------------------------------')
    print('COMPILER OUTPUT START')
    print('------------------------------------------------------------')

    debug(project)
    from project4 import main
    main(logger, inputfile=inputfile, inputstr=inputstr)

    print('------------------------------------------------------------')
    print('COMPILER OUTPUT END')
    print('------------------------------------------------------------')

@task
def clean(project, logger):
    clean_up("gen/", "generated files", logger)

def clean_up(path_or_glob, name, logger):
    if "*" in path_or_glob:
        directories_to_clean = glob.glob(path_or_glob)
    else:
        directories_to_clean = [os.path.expanduser(path_or_glob)]

    for directory_to_clean in directories_to_clean:
        if not os.path.exists(directory_to_clean):
            continue
        logger.info("Removing {0} directory: {1}".format(name, directory_to_clean))
        shutil.rmtree(directory_to_clean)
