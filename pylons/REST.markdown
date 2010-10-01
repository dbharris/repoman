
# RESTfull API

## URLs

    <host:port>/repository/users
    <host:port>/repository/users/{id}
    <host:port>/repository/groups
    <host:port>/repository/groups/{id}
    <host:port>/repository/images
    <host:port>/repository/images/{id}


### repository/users
#### GET
A GET request will return a list of all users in the system formatted as a json list of objects
    [
      {
        admin:VALUE,
        email:VALUE,
        name:VALUE,
        client_dn:VALUE,
        id:VALUE
      },
      {
        admin:VALUE,
        email:VALUE,
        name:VALUE,
        client_dn:VALUE,
        id:VALUE
      },
      ...
    ]

#### POST
POSTing to this url will insert a new entry into the database.

required params:
    name        - plain text name of the user
    email       - email address of the user
    client_dn   - client DN (must be unique among all users)

optional params:
    admin       - in the set of ['0', '1', 'true', 'false', 'True', False']
    suspended   - in the set of ['0', '1', 'true', 'false', 'True', False']
    groups      - a list of groups to add this user to

error codes returned:
* *409* - conflict with client_dn already in databse
* *400* - badly formed request due to invlaid input for *admin* or *suspended* or non-existant group specified
* *500* - internal error.  something bad happened.  look at the logs.

### repository/users/{id}
#### GET
A GET request on this url will retrieve an object describing the specified user in detail
    {
      groups: [
        {
          id:VALUE,
          name:VALUE
        },
        {
          id:VALUE,
          name:VALUE
        },
        ...
      ],
      name:VALUE,
      admin:VALUE,
      client_dn:VALUE,
      id:VALUE,
      suspended:VALUE,
      email:VALUE,
      images: [
        {
          # Image object
        },
        ...
      ]
    }

#### DELETE

#### PUT


### repository/groups

**MORE DOCS COMING**




