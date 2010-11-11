# Future improvements for Repoman

## Federated repositories
* Create a private API for communicating repository to repository.
  * Each repo must also have a client certificate.
  * The repository acts as a special trusted client when requesting data

* Force metadata to sync on every action.
* Image files are only transfered when needed.


## Multiple storage backends
* Ability to store and retrieve data from a number of different backends.
 * localdisk or network mounted filesystems
  * complete control of files
  * no max file size
 * Amazon S3 storage
  * 5GB max object size
  * can be directly used in ec2?
 * Cumulus
  * S3 clone.
  * upload in a way that allows for images to be used by cloud client
  *


## Decouple storage from metadata

