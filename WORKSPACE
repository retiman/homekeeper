workspace(name = "homekeeper")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "bazel_federation",
    url = "https://github.com/bazelbuild/bazel-federation/archive/130c84ec6d60f31b711400e8445a8d0d4a2b5de8.zip",
    sha256 = "9d4fdf7cc533af0b50f7dd8e58bea85df3b4454b7ae00056d7090eb98e3515cc",
    strip_prefix = "bazel-federation-130c84ec6d60f31b711400e8445a8d0d4a2b5de8",
    type = "zip",
)

load("@bazel_federation//:repositories.bzl", "rules_python")
rules_python()

load("@bazel_federation//setup:rules_python.bzl", "rules_python_setup")
rules_python_setup(use_pip=True)

load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()

load("@rules_python//python:pip.bzl", "pip_import", "pip_repositories")
pip_repositories()

pip_import(
    name = "pip",
    requirements = "//:requirements.txt"
)

load("@pip//:requirements.bzl", "pip_install")
pip_install()