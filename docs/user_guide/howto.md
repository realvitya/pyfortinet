# Howto Do ...

In the following examples it is assumed that the fmg connection object is already opened:

```python
config = {
    "base_url": "https://myfmg.com",
    "username": "myuser",
    "password": "verysecret",
    "adom": "root",
    "verify": False
}
with FMG(**config) as fmg:
    ...
```

## Create new objects

There are more options using the high-level API:

```python
# create an object
new_addr = Address(name="server1", subnet="1.1.1.1")

# the object is only created in memory. We need to add it to `fmg`
result = fmg.add(new_addr)

# we can examine result to check if the operation was successful
if result:  # same as result.success
    print(f"{new_addr.name} was successfully created")
```

We can also call objects' fmg operation methods:

```python
# create an object and assign to `fmg`
new_addr = fmg.get_obj(Address(name="server1", subnet="1.1.1.1"))

# then add it to fmg without using `fmg` directly
result = new_addr.add()
if result:  # same as result.success
    print(f"{new_addr.name} was successfully created")
```

## Creating / deleting dynamic mapping

Creating mapping:

```python
# create a new object
server: Address = fmg.get_obj(Address(name="test-server", subnet="10.0.0.1/32"))
fw: Device = fmg.get(Device).first()
# create server object in FMG
server.add()
# create a mapping to server object with the fw device and different IP
server.dynamic_mapping = Address(mapping__scope=fw.get_vdom_scope("root"), subnet="2.2.2.2")
# beware that FMG will convert this single element to a list!
server.update()
server = fmg.get(Address, F(name=server.name))
# dynamic_mapping became list!
print(server.dynamic_mapping[0].subnet)
```

Deleting mapping:

```python
del server.dynamic_mapping[0]
server.update()
server = fmg.get(Address, F(name=server.name))
# this should print empty output
print(server.dynamic_mapping)
```
