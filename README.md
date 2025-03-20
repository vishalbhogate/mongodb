
# MongoDB Setup and Script for `sj_release` Database

## Setup MongoDB with `setup_mongo.sh`

To set up MongoDB in the Kind Kubernetes cluster, follow the instructions below.

### 1. Clone the Repository

Clone this repository if you haven't already:

```sh
git clone https://github.com/vishalbhogate/mongodb.git
cd mongodb
```

### 2. Run the Setup Script

Use the provided `setup_mongo.sh` script to install **MongoDB** using **Helm** in your Kubernetes cluster.

Run the following command:

```sh
chmod +x setup_mongo.sh
./setup_mongo.sh
```

This script will:
- Install **MongoDB** using the Bitnami Helm chart.
- Expose MongoDB through a **port-forward**.
- Retrieve the MongoDB root password.

After running this script, MongoDB should be accessible locally at `localhost:27017`.

### 3. Set Up MongoDB Credentials

If you're using the root user (`MONGODB_ROOT_PASSWORD`), connect with:

```sh
mongosh --host localhost -u root -p $MONGODB_ROOT_PASSWORD --authenticationDatabase admin
```

If you're using the application user (`MONGODB_PASSWORD`), connect with:

```sh
mongosh --host localhost -u admin -p $MONGODB_PASSWORD --authenticationDatabase mydb
```

### 4. Create a Database

MongoDB automatically creates a database when you insert a document. However, you can explicitly switch to a new database like this:

```javascript
use sj_release
```

Now, `sj_release` is your active database.

### 5. Create a Collection (Table Equivalent)

To create a collection named `audit_log`:

```javascript
db.createCollection("audit_log")
```

### 6. Insert a Sample Document

Insert a sample document into the `audit_log` collection:

```javascript
db.audit_log.insertOne({ msg: "Database initialized", time: new Date() })
```

### 7. Verify the Database and Collection

Check the available databases and collections:

```javascript
show dbs           // List all databases
use sj_release     // Switch to the database
show collections   // List all collections
db.audit_log.find().pretty() // View documents in the collection
```

1. **Connect to MongoDB as Root:**
```sh
mongosh --host localhost -u root -p $MONGODB_ROOT_PASSWORD --authenticationDatabase admin
```

2. **Switch to the `sj_release` Database:**
```javascript
use sj_release
```

3. **Create a User for `sj_release`:**
```javascript
db.createUser({
  user: "sj_user",
  pwd: "securepassword",
  roles: [
    {
      role: "readWrite",
      db: "sj_release"
    }
  ]
});
```

4. **Verify the User**

To check if the user was created successfully, run:

```javascript
db.getUsers()
```

### 8. Export the Credentials for the Script

Before running the script, set the environment variables:

```sh
export MONGODB_USERNAME="sj_user"
export MONGODB_PASSWORD="securepassword"
```

### 9. Run the Script

Run the Python script to insert logs into the `sj_release.audit_log` collection:

```sh
python release_info.py --user alice --service_name web-api --release_tag v1.2.3
```

### 10. Verify Data in MongoDB

Finally, verify that the data was inserted into the `audit_log` collection:

```sh
mongosh --host localhost -u sj_user -p $MONGODB_PASSWORD --authenticationDatabase sj_release
use sj_release
db.audit_log.find().pretty()
```

This `README.md` provides a clear, step-by-step guide for setting up MongoDB, creating a user, and automating the process of inserting logs into the `sj_release` database.

