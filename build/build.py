"""Python transcription of original build.bat for platform independence.
   Includes several invocations of the co-located setup.py for setuptools
   passes (testing, building, etc.).
"""

import os
import sys
import shutil
import subprocess

def getPackageName():
    """Returns package name from top-level package folder
    """
    buildPath, _ = os.path.split(os.path.abspath(__file__))
    packagePath, _ = os.path.split(buildPath)
    _, packageName = os.path.split(packagePath)
    return packageName

def copy():
    """Copies package contents to build directory
    """
    name = getPackageName()
    print("Copying package contents to build directory...")
    buildPath, _ = os.path.split(os.path.abspath(__file__))
    buildCopy = buildPath + "/" + name
    packagePath, _ = os.path.split(buildPath)
    os.mkdir(buildCopy)
    for item in os.listdir(packagePath):
        fromPath = packagePath + "/" + item
        toPath = buildCopy + "/" + item
        _, fromName = os.path.split(fromPath)
        if os.path.isdir(fromPath) and fromName.lower() != "build" and not fromName.startswith("."):
            shutil.copytree(fromPath, toPath)

def test(isSilent=True):
    """Runs setuptools with "test" mode. At some point this should be extended
       to verify that the test suite(s?) completed successfully.
    """
    print("Running setuptools in 'test' mode...")
    buildPath, _ = os.path.split(os.path.abspath(__file__))
    args = {}
    if isSilent:
        args["stdout"] = subprocess.PIPE
        args["stderr"] = subprocess.PIPE
    subp = subprocess.Popen(["python", buildPath + "/setup.py", "test"], **args)
    subp.communicate()

def build(isSilent=True):
    """Runs setuptools build pass with targz target for source distribution
    """
    print("Running setuptools to build source targz...")
    buildPath, _ = os.path.split(os.path.abspath(__file__))
    args = {}
    if isSilent:
        args["stdout"] = subprocess.PIPE
        args["stderr"] = subprocess.PIPE
    subp = subprocess.Popen(["python", buildPath + "/setup.py", "sdist", "--format=gztar"], **args)
    subp.communicate()

def register():
    """
    """
    pass

def publish():
    """
    """
    pass

def cleanup():
    """Remove all contents of copied build folder and other artifacts
    """
    print("Cleaning up build artifacts...")
    name = getPackageName()
    buildPath, _ = os.path.split(os.path.abspath(__file__))
    buildCopy = buildPath + "/" + name
    if os.path.isdir(buildCopy):
        shutil.rmtree(buildCopy)
    eggPath = buildPath + "/.eggs"
    if os.path.isdir(eggPath):
        shutil.rmtree(eggPath)
    infoPath = buildPath + "/%s.egg-info" % name
    if os.path.isdir(infoPath):
        shutil.rmtree(infoPath)
    distPath = buildPath + "/dist"
    if os.path.isdir(distPath):
        shutil.rmtree(distPath)

def main(isCleanOnly=False):
    """
    """
    if not isCleanOnly:
        print("Building package %s..." % getPackageName())
        copy()
        test()
        build()
        register()
        publish()
    if isCleanOnly:
        print("Cleaning build for package %s..." % getPackageName())
    cleanup()

if __name__ == "__main__":
    main("--clean" in sys.argv)
