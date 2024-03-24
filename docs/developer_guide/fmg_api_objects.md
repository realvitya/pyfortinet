# Guidelines for Implementing Objects for API Calls

As not all API calls are implemented, I'm happily accept help with your use case implemented here.
I'd like to describe the general logic of the API classes and how to develop them.

## 1. Which module to use?

FMG API reference and [FNDN](https://fndn.fortinet.net/index.php?/fortiapi/5-fortimanager) will give you the guidance
where to implement new classes. For example [`Address`][fmg_api.firewall.Address] firewall object is listed at [firewall](https://fndn.fortinet.net/index.php?/fortiapi/5-fortimanager/3197/5/pm/config/firewall/)
section. Therefore, any API route under the firewall section should go to module ``pyfortinet.fmg_api.firewall``.

## 2. API call type

There are two predefined base class you can start your development: [`FMGObject`][fmg_api.FMGObject] and [`FMGExecObject`][fmg_api.FMGExecObject].
These are base classes you must inherit your class and these provides couple of common services.

If API documentation shows ``exec`` operation, use the [`FMGExecObject`][fmg_api.FMGExecObject] as base class!

## 3. Writing an API route class

Pydantic is heavily used to check and convert data. This way we ensure data quality and coherent way of handling data.
For example, FMG tends to return data values as integer, but these need to be converted back to string, so it's easier
for humans to understand.

The goal of the classes to implement an object which can be easily used by the user and do only minimal initialization.
The structure of a class is looking like that:

```python
class SomeAPICall(FMGObject):
    """Short description what this object will do

    Attributes:
        ...  # proper docstring for all API data
    """

    # mandatory private attribute initialization
    ## _url usually contains {scope} which is handled by default _get_url method
    _url: str = "/pm/config/{scope}/obj/some/route"  # You need to specify the route for this API
    # optional private attribute initialization
    ## _version is supposed to indicate minimum FMG API version support for this class (TBD)
    _version: str = "7.2.4"
    ## other private attributes can be defined. The inherited attributes are not meant to be overridden
    #
    # API data fields
    # All of these should be Optional, except the primary key field which is indicated in the API documentation
    # Primary key for this object in FMG:
    name: str = Field(..., max_length=128)
    # Field with choices should be defined outside the class for clarity
    # E.g.: SOME_VALUES = Literal["value1", "value2"]
    some: Optional[SOME_VALUES] = None
    # If API field has space or dash, use underscore and utilize Pydantic 'validation_alias' and 'serialization_alias'!
    # AliasChoices is required so user can use either form!
    some_with_space: Optional[str] = Field(None, 
                                           validation_alias=AliasChoices("some with space", "some_with_space"), 
                                           serialization_alias="some with space")
    some_with_dash: Optional[str] = Field(None, validation_alias=AliasChoices("some-with-dash", "some_with_dash"), 
                                          serialization_alias="some-with-dash")
    # We can use our class as a result of a different API call or when we submit data
    # There are cases when we want to use data as a result but don't want to push back as an update
    # E.g. VDOM.get with loadsubs will return device. We should not set this when try to save VDOM.
    # 'exclude' keyword can be used to not add this field to the 'add', 'update' or 'set' methods.
    device: str = Field("", exclude=True, description="Assigned device (optional)")
    #
    # Validator example field:
    subnet: Optional[Union[str, list[str]]] = None

    # Validators are used to standardize data
    # All of these are optional, these are just examples
    @field_validator("subnet")
    def standardize_subnet(cls, v):
        """validator: x.x.x.x/y.y.y.y -> x.x.x.x/y"""
        if isinstance(v, list):
            return IPv4Interface("/".join(v)).compressed
        else:
            return IPv4Interface(v).compressed

    # Convert integer values back to string which is defined as Literal (SOME_VALUES)
    @field_validator("some", mode="before")
    def validate_some(cls, v: int) -> SOME_VALUES:
        return SOME_VALUES.__dict__.get("__args__")[v] if isinstance(v, int) else v

    # When check cannot be executed before instantiation of the class, we can post-check on the object
    # The following example changes field 'device' field based on the 'action' field.
    @model_validator(mode="after")
    def validate_devicejob(self) -> "DeviceTask":
        """Validate device job"""
        self._url = self._url.replace("{action}", self.action)
        if self.action == "del":
            self.device = self.device.name  # deleting a device requires device id or name
        return self
```

### URL handling

The mandatory private attribute to implement is the ``_url``. This defines the API route. It can have dynamic path,
which is derived by the ``get_url`` property. The built-in [`FMGObject.get_url`][fmg_api.FMGObject.get_url] will look
for ``{scope}`` string in the URL and will replace it with the ``_scope`` attribute.

This ``_scope`` attribute is uninitialized by default if the object is instantiated directly from the class. If it
remains uninitialized, when the object is used by ``FMG`` high-level object, it will use its own set scope instead.

!!! note "object scope"

    If you set a scope for the object, it will use that scope only! Object level scope overrides FMG scope (adom).

### Version handling

TBD, not implemented yet

### Field validation

All fields can be validated using Pydantic arsenal. The above example describes some use-cases.

You can check [Pydantic model usage](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage) or
[Pydantic Field usage](https://docs.pydantic.dev/latest/concepts/fields/) for more information and examples.
Using the ``Field`` value you can fine-tune the already specified type with more constraints. For example by strings,
it's possible to add regex constraint. If anytime a validation fails, the object instantiation will raise a
``ValidationError`` exception.

### Mandatory field handling

As a thumb rule, all field should be optional, because the class we define can be a result of an API get call, or we
just want to create an object with certain otherwise optional fields. There is one exception when we should set a field
mandatory: When API docs mention a field as primary key, then this field must be filled in every case, and it's just
better to have it defined in our code as well.

In Pydantic, there are two ways of defining mandatory fields:

1.By not specifying ``Optional`` type hinting and/or default value

```python
some: str
```

2.By using ``Field`` constraint with ``...`` (Ellipse) as default value

```python
some_other: str = Field(..., validation_alias=AliasChoices("some other", "some_other"), serialization_alias="some other")
```

### Class inheritance

There are cases when two API data is very similar and only slight differences need to be defined. In that case it's
easier to define a base and more general model and inherit from it the more specific ones. Such an example is
[`BaseDevice`][fmg_api.dvmdb.BaseDevice] which is the parent of [`Device`][fmg_api.dvmdb.Device]. Differences are
the default values and mandatory fields.

## 4. Writing tests for the new class

Each module should have its own test file. Please create such test-cases that the following rules are applied:

1. Cover all use-cases of your class.
     1. create using kwargs
     2. create using FMG object
     3. test all methods
2. There should be no leftover on the FMG after proper test-run! (cleanup!)
3. Utilize existing fixtures to access lab environment

!!! tip

    Best to check out existing test cases and work based on those!

## 5. Ensure proper documentation in docstrings and ``docs`` folder if necessary

This project uses Google docstring format and Markdown to enhance documentation.

## 6. Run linters to standardize and polish new code
