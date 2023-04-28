from datetime import datetime, date
from dateutil import parser

from typing import Dict, Any, List, Iterable

from objects.wrappers import execute_sql

TYPE_MAPPING: Dict[Any, str] = {
    int: "integer",
    str: "varchar(255)",
    bool: "tinyint",
    datetime: "datetime",
    date: "date",
}

CONSTRAINT_MAPPING: Dict[str, str] = {
    "primary_key": "primary key",
    "unique": "unique",
    "auto_increment": "autoincrement",
}

CONSTRAINT_KEYS = ["primary_key", "unique", "auto_increment"]


class SingletonClass(object):
    singleton_instance = None

    def __new__(cls):
        if not cls.singleton_instance:
            cls.singleton_instance = super().__new__(cls)
        return cls.singleton_instance


class OOPObject(object):
    table_name = None
    fields = []

    def __init__(self, *args, **kwargs):
        iterator = iter(args)
        self.field_annotations = vars(self.__class__)["__annotations__"]
        for idx, field in enumerate(self.fields):
            try:
                setattr(self, field, next(iterator))
            except StopIteration:
                default_value = self.field_annotations[field].get("default", None)
                if callable(default_value):
                    default_value = default_value()
                setattr(self, field, kwargs.get(field, default_value))
        self.is_creating = kwargs.get("is_creating", False)

    def __str__(self):
        return f"{self.table_name}(id={self.pk})"

    @property
    def pk(self):
        return getattr(self, self.fields[0], None)

    @property
    def primary_key(self):
        return "id"

    @property
    def editable_fields(self):
        return [field for field in self.fields if field != self.primary_key]

    def save(self):
        if not self.pk:
            sql, variables = self.get_create_sql()
        else:
            sql, variables = self.get_update_sql()
        result = execute_sql(sql, variables)[0]
        self.map_result_to_self(result)
        self.is_creating = False
        return self

    def map_result_to_self(self, result):
        fields_iterable = iter(self.fields)
        for value in result:
            field = next(fields_iterable)
            if value is None:
                setattr(self, field, value)
                continue
            field_type = self.field_annotations[field]["field_type"]
            if field_type in [datetime, date]:
                casted_value = parser.parse(value)
            else:
                casted_value = field_type(value)
            setattr(self, field, casted_value)

    def get_create_sql(self):
        return f"""
        insert into {self.table_name} ({", ".join(self.editable_fields)}) values
        ({(len(self.editable_fields) * '?, ')[:-2]})
        returning *;
        """, [getattr(self, field) for field in self.editable_fields]

    def get_update_sql(self):
        return f"""
        update {self.table_name}
        {self.get_update_sql_body()}
        where {self.primary_key} = {self.pk}
        returning *;
        """, [getattr(self, field) for field in self.editable_fields]

    def get_update_sql_body(self):
        sql = "set"
        for field in self.editable_fields:
            sql += f" {field}=?,"
        return sql[:-1]

    def delete(self):
        assert self.pk
        sql = f"""
        delete from {self.table_name} where {self.primary_key} = {self.pk};
        """
        execute_sql(sql)


class BaseFactory(object):
    object_class = None

    def __init__(self, object_class):
        self.object_class = object_class

    def get_object_class(self):
        return self.object_class

    def create(self, **kwargs):
        instance = self.get_object_class()(**kwargs, is_creating=True)
        instance.save()
        return instance

    def init(self, *args):
        return self.get_object_class()(*args)


class BaseManager(SingletonClass):
    object_class = None
    factory = None
    search_fields = []

    def __init__(self):
        self.factory = BaseFactory(self.get_object_class())

    def get_object_class(self):
        return self.object_class

    def create_table(self) -> None:
        assert self.object_class
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.object_class.table_name} (
            {self.get_create_table_data()}
        )
        """
        execute_sql(sql)

    def get_create_table_data(self) -> str:
        data = vars(self.object_class)["__annotations__"]
        definitions = []
        foreign_keys = {}
        for key, value in data.items():
            field_definition = f"{key} {TYPE_MAPPING[value['field_type']]}"
            for item in CONSTRAINT_KEYS:
                if item in value:
                    field_definition += f" {CONSTRAINT_MAPPING[item]}"
            if "default" in value:
                default_value = value["default"]
                if type(default_value) in [int, bool]:
                    field_definition += f" not null default {default_value}"
                else:
                    field_definition += f" not null default '{default_value}'"
            if "foreign_key" in value:
                foreign_keys[key] = value["foreign_key"]()
            definitions.append(field_definition)
        for key, object_class in foreign_keys.items():
            field_definition = f"foreign key({key}) references {object_class.table_name}({object_class.fields[0]})"
            definitions.append(field_definition)
        return ",".join(definitions)

    @property
    def primary_key(self):
        return "id"

    def create(self, **kwargs):
        return self.factory.create(**kwargs)

    def init(self, *args):
        return self.factory.init(*args)

    def init_list(self, values_list: List[Iterable] = None):
        values_list = values_list if values_list else []
        return [self.init(*values) for values in values_list]

    def handle_search_conditions(self, **kwargs):
        sql = "WHERE"
        for key in kwargs.keys():
            sql += f" {key}=? AND"
        sql += " ("
        for field in self.search_fields:
            sql += f" LOWER({field}) LIKE ? OR"
        return sql[:-3] + ")"

    def handle_ordering(self, ordering: List[str]):
        sql = "ORDER BY"
        for item in ordering:
            if item[0] == "-":
                sql += f" {item[1:]} DESC,"
            else:
                sql += f" {item},"
        return sql[:-1]

    def search(self, search: str, ordering: List[str] = None, sql: str = None, **kwargs):
        sql = f"""
        SELECT * FROM {self.object_class.table_name}
        """
        if self.search_fields:
            sql += f" {self.handle_search_conditions(**kwargs)}"
        if ordering:
            sql += f" {self.handle_ordering(ordering)}"

        pattern = f"%{search.lower()}%"
        variables = list(kwargs.values()) + ([pattern]*len(self.search_fields))
        results = execute_sql(sql, variables)
        if not results:
            return []
        values_list = [[item for item in result] for result in results]
        return self.init_list(values_list)

    def filter(self, **kwargs):
        ordering = None
        if isinstance(kwargs.get("ordering"), list):
            ordering = kwargs.pop("ordering")
        variables = []
        sql = f"""
        SELECT * FROM {self.object_class.table_name}
        """
        if kwargs:
            sql += "WHERE "
        for key, value in kwargs.items():
            variables.append(value)
            sql += f"{key}=?,"
        sql = sql[:-1]
        if ordering:
            sql += f" {self.handle_ordering(ordering)}"
        results = execute_sql(sql, variables)
        if not results:
            return []
        values_list = [[item for item in result] for result in results]
        return self.init_list(values_list)

    def get(self, id: int):
        sql = f"""
        SELECT * FROM {self.object_class.table_name}
        WHERE {self.primary_key} = {id};
        """
        results = execute_sql(sql)
        if not results:
            return
        return self.init(*[item for item in results[0]])
