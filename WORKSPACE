workspace(name = "homekeeper")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/archive/94677401bc56ed5d756f50b441a6a5c7f735a6d4.tar.gz",
    strip_prefix = "rules_python-94677401bc56ed5d756f50b441a6a5c7f735a6d4",
    sha256 = "acbd018f11355ead06b250b352e59824fbb9e77f4874d250d230138231182c1c",
)

load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()

load("@rules_python//python:pip.bzl", "pip_repositories", "pip3_import")
pip_repositories()

pip3_import(
    name = "pip",
    requirements = "//:requirements.txt",
)

load("@pip//:requirements.bzl", "pip_install")
pip_install()