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

py_library(
    name = "test_case",
    srcs = ["test_case.py"],
    deps = [
        requirement("mock"),
        requirement("pyfakefs"),
        requirement("pytest"),
        ":common",
    ],
)

py_test(
    name = "test_homekeeper",
    size = "small",
    srcs = ["test_homekeeper.py"],
    deps = [
        requirement("pytest"),
        ":common",
        ":config",
        ":package",
        ":test_case",
    ],
)

py_test(
    name = "test_core",
    size = "small",
    srcs = ["test_core.py"],
    deps = [
        requirement("pytest"),
        ":common",
        ":config",
        ":core",
        ":test_case",
    ]
)

py_test(
    name = "test_cli",
    size = "small",
    srcs = ["test_cli.py"],
    deps = [
        requirement("click"),
        requirement("mock"),
        requirement("pytest"),
        ":cli",
        ":package",
        ":test_case",
    ],
)

py_test(
    name = "test_config",
    size = "small",
    srcs = ["test_config.py"],
    deps = [
        requirement("pytest"),
        ":config",
        ":test_case",
    ],
)