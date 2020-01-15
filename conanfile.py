import os

from conans import ConanFile, CMake, tools


class QhullConan(ConanFile):
    name = "qhull"
    version = "7.3.0"
    url = "http://www.qhull.org/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    description = """Qhull computes the convex hull, Delaunay triangulation, Voronoi diagram, halfspace intersection about a point, furthest-site Delaunay triangulation, and furthest-site Voronoi diagram."""
    exports_sources = (
        "*",
        "!*-build-*",
        "!conan*",
        "!test_package",
        "!graph_info.json",
        "!.idea",
        "!manual",
        "!etc",
    )

    def configure_cmake(self, definitions={}):
        cmake = CMake(self)

        if "CCACHE" in os.environ:
            cmake.definitions["CMAKE_CXX_COMPILER_LAUNCHER"] = os.environ["CCACHE"]

        cmake.definitions.update(definitions)

        cmake.configure(source_folder=".")

        return cmake

    def build(self):
        cmake = cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
