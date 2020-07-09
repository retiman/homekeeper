load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "package",
    srcs = ["__init__.py"],
    deps = [
        ":config",
        ":core",
    ],
)

py_library(
    name = "cli",
    srcs = ["cli.py"],
    visibility = ["//visibility:public"],
    deps = [
        requirement("click"),
        ":package",
    ],
)

py_library(
    name = "common",
    srcs = ["common.py"]
)

py_library(
    name = "config",
    srcs = ["config.py"],
    deps = [
        ":common",
    ],
)

py_library(
    name = "core",
    srcs = ["core.py"],
    deps = [
        ":common",
    ],
)