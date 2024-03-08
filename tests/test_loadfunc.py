import unittest
from textwrap import dedent

import yaml
from yamlinclude import (
    YamlIncludeCtor,
    load_yaml_include,
    iload_yaml_include,
)

from ._internal import YAML_LOADERS, YAML1, YAML2


class LoadFuncTestCase(unittest.TestCase):
    ctor = YamlIncludeCtor(base_dir="tests/data", auto_load=False)

    @classmethod
    def setUpClass(cls):
        for loader_cls in YAML_LOADERS:
            yaml.add_constructor("!inc", cls.ctor, loader_cls)

    @classmethod
    def tearDownClass(cls) -> None:
        for loader_class in YAML_LOADERS:
            del loader_class.yaml_constructors["!inc"]

    def test_normal(self):
        yaml_string = dedent(
            """
            list:
                - !inc include.d/1.yaml
                - !inc include.d/2.yaml
            dict:
                yaml1: !inc include.d/1.yaml
                yaml2: !inc include.d/2.yaml
            """
        ).strip()
        for loader_cls in YAML_LOADERS:
            d0 = yaml.load(yaml_string, loader_cls)
            d1 = load_yaml_include(d0, loader_cls, self.ctor)
            self.assertDictEqual(YAML1, d1["list"][0])
            self.assertDictEqual(YAML2, d1["list"][1])
            self.assertDictEqual(YAML1, d1["dict"]["yaml1"])
            self.assertDictEqual(YAML2, d1["dict"]["yaml2"])

    def test_inplace(self):
        yaml_string = dedent(
            """
            list:
                - !inc include.d/1.yaml
                - !inc include.d/2.yaml
            dict:
                yaml1: !inc include.d/1.yaml
                yaml2: !inc include.d/2.yaml
            """
        ).strip()
        for loader_cls in YAML_LOADERS:
            d0 = yaml.load(yaml_string, loader_cls)
            load_yaml_include(d0, loader_cls, self.ctor, inplace=True)
            self.assertDictEqual(YAML1, d0["list"][0])
            self.assertDictEqual(YAML2, d0["list"][1])
            self.assertDictEqual(YAML1, d0["dict"]["yaml1"])
            self.assertDictEqual(YAML2, d0["dict"]["yaml2"])

    def test_nested(self):
        yaml_string = dedent(
            """
            nested: !inc nested.yaml
            """
        ).strip()
        for loader_cls in YAML_LOADERS:
            d0 = yaml.load(yaml_string, loader_cls)
            d1 = load_yaml_include(d0, loader_cls, self.ctor, nested=True)
            self.assertDictEqual(YAML1, d1["nested"]["list"][0])
            self.assertDictEqual(YAML2, d1["nested"]["list"][1])
            self.assertDictEqual(YAML1, d1["nested"]["dict"]["yaml1"])
            self.assertDictEqual(YAML2, d1["nested"]["dict"]["yaml2"])

    def test_inplace_nested(self):
        yaml_string = dedent(
            """
            nested: !inc nested.yaml
            """
        ).strip()
        for loader_cls in YAML_LOADERS:
            d0 = yaml.load(yaml_string, loader_cls)
            load_yaml_include(d0, loader_cls, self.ctor, inplace=True, nested=True)
            self.assertDictEqual(YAML1, d0["nested"]["list"][0])
            self.assertDictEqual(YAML2, d0["nested"]["list"][1])
            self.assertDictEqual(YAML1, d0["nested"]["dict"]["yaml1"])
            self.assertDictEqual(YAML2, d0["nested"]["dict"]["yaml2"])


class IterableLoadFuncTestCase(unittest.TestCase):
    ctor = YamlIncludeCtor(base_dir="tests/data", auto_load=False)

    @classmethod
    def setUpClass(cls):
        for loader_cls in YAML_LOADERS:
            yaml.add_constructor("!inc", cls.ctor, loader_cls)

    @classmethod
    def tearDownClass(cls) -> None:
        for loader_class in YAML_LOADERS:
            del loader_class.yaml_constructors["!inc"]

    def test_inplace(self):
        yaml_string = dedent(
            """
            list:
                - !inc include.d/1.yaml
                - !inc include.d/2.yaml
            dict:
                yaml1: !inc include.d/1.yaml
                yaml2: !inc include.d/2.yaml
            """
        ).strip()
        for loader_cls in YAML_LOADERS:
            d0 = yaml.load(yaml_string, loader_cls)
            for _ in iload_yaml_include(d0, loader_cls, self.ctor):
                pass
            self.assertDictEqual(YAML1, d0["list"][0])
            self.assertDictEqual(YAML2, d0["list"][1])
            self.assertDictEqual(YAML1, d0["dict"]["yaml1"])
            self.assertDictEqual(YAML2, d0["dict"]["yaml2"])

    def test_inplace_nested(self):
        yaml_string = dedent(
            """
            nested: !inc nested.yaml
            """
        ).strip()
        for loader_cls in YAML_LOADERS:
            d0 = yaml.load(yaml_string, loader_cls)
            for _ in iload_yaml_include(d0, loader_cls, self.ctor, nested=True):
                pass
            self.assertDictEqual(YAML1, d0["nested"]["list"][0])
            self.assertDictEqual(YAML2, d0["nested"]["list"][1])
            self.assertDictEqual(YAML1, d0["nested"]["dict"]["yaml1"])
            self.assertDictEqual(YAML2, d0["nested"]["dict"]["yaml2"])