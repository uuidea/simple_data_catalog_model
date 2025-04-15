from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'sdc',
     'default_range': 'string',
     'id': 'https://w3id.org/linkml/examples/personinfo',
     'imports': ['linkml:types'],
     'name': 'data_catalog_model',
     'prefixes': {'dcat': {'prefix_prefix': 'dcat',
                           'prefix_reference': 'http://www.w3.org/ns/dcat#'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'foaf': {'prefix_prefix': 'foaf',
                           'prefix_reference': 'http://xmlns.com/foaf/0.1/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'odrl': {'prefix_prefix': 'odrl',
                           'prefix_reference': 'http://www.w3.org/ns/odrl/2/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'sdc': {'prefix_prefix': 'sdc',
                          'prefix_reference': 'https://w3id.org/simpledatacatalog/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'vcard': {'prefix_prefix': 'vcard',
                            'prefix_reference': 'http://www.w3.org/2006/vcard/ns#'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'source_file': 'src/simple_data_catalog_model/dataset_model.yaml'} )


class Dataset(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dcat:Dataset',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    identifier: str = Field(default=..., description="""An unambiguous reference to the resource within a given context.""", json_schema_extra = { "linkml_meta": {'alias': 'identifier',
         'domain_of': ['Dataset'],
         'slot_uri': 'dcterms:identifier'} })
    description: Optional[str] = Field(default=None, description="""Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Dataset'],
         'slot_uri': 'dcterms:identifier'} })
    title: Optional[str] = Field(default=None, description="""A name given to the resource.""", json_schema_extra = { "linkml_meta": {'alias': 'title', 'domain_of': ['Dataset'], 'slot_uri': 'dcterms:title'} })
    publisher: Optional[Union[Agent, str]] = Field(default=None, description="""An entity responsible for making the resource available.""", json_schema_extra = { "linkml_meta": {'alias': 'publisher',
         'any_of': [{'range': 'uri'}, {'range': 'Agent'}],
         'domain_of': ['Dataset'],
         'slot_uri': 'dcterms:publisher'} })
    contactPoint: Optional[Union[Kind, str]] = Field(default=None, description="""Relevant contact information for the cataloged resource. Use of vCard is recommended""", json_schema_extra = { "linkml_meta": {'alias': 'contactPoint',
         'any_of': [{'range': 'string'}, {'range': 'Kind'}],
         'domain_of': ['Dataset'],
         'slot_uri': 'vcard:contactPoint'} })


class Agent(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'foaf:Agent',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    name: Optional[str] = Field(default=None, description="""A name for some thing""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent'], 'slot_uri': 'foaf:name'} })


class Kind(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'vcard:Kind',
         'from_schema': 'https://w3id.org/linkml/examples/personinfo'})

    hasEmail: Optional[str] = Field(default=None, description="""Relevant contact information for the cataloged resource. Use of vCard is recommended""", json_schema_extra = { "linkml_meta": {'alias': 'hasEmail', 'domain_of': ['Kind'], 'slot_uri': 'vcard:hasEmail'} })


class Container(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/examples/personinfo',
         'tree_root': True})

    datasets: Optional[List[Dataset]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'datasets', 'domain_of': ['Container']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Dataset.model_rebuild()
Agent.model_rebuild()
Kind.model_rebuild()
Container.model_rebuild()

