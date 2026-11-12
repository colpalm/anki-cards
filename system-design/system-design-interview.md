# System Design Interview Anki Cards

## Sources
- *System Design Interview – An Insider's Guide*, Volume 1 (Alex Xu)

## Cards

### Chapter 1: Scale From Zero to Millions of Users

### Vertical vs. Horizontal Scaling
<!-- anki:1794426131897 -->

**Front:**
What are the tradeoffs between vertical and horizontal scaling?

**Back:**
- **Vertical (scale up)**: a bigger machine with more CPU and RAM. It's simple because nothing in the architecture changes. But it has a **hard ceiling** (one box only gets so big), costs climb steeply at the high end, and there's **no redundancy**: one server is a single point of failure.
- **Horizontal (scale out)**: more machines. There's effectively no ceiling, and losing one machine doesn't take the system down. The cost is complexity: load balancing, stateless servers, and distributing data.

Vertical scaling is a good starting point and goes further than people expect. Horizontal scaling is what large systems need.

**Tags:**
system-design::scaling source::system-design-interview-xu

---

### Order of Database Scaling Steps
<!-- anki:1794426131940 -->

**Front:**
In what order do you typically scale a database as load grows, and why does sharding come last? (3 steps)

**Back:**
1. **Scale vertically**: a bigger machine adds no complexity.
2. **Add read replicas and a cache**: most apps are read-heavy, so moving reads elsewhere goes a long way.
3. **Shard**: only once write volume or data size outgrows a single primary.

Sharding comes last because it adds the most complexity and is the hardest to undo: choosing a shard key, hot shards, resharding, and losing cross-shard joins. Replicas and caches only scale reads. Sharding is the step that scales writes and storage.

**Tags:**
system-design::databases source::system-design-interview-xu

---

### When to Choose a NoSQL Database
<!-- anki:1794426131990 -->

**Front:**
When is a non-relational (NoSQL) database a better fit than a relational one? (4 cases)

**Back:**
Relational is the default because it's mature and supports joins and transactions. NoSQL fits when:
- You need **very low latency** at high throughput
- The data is **unstructured** or has no relational shape
- Access is simple **key-based reads and writes** of whole objects, with no joins
- You need to store a **massive amount of data**

Why: NoSQL systems usually give up joins and multi-row transactions. Without those, it's easy to partition data across many machines and keep simple lookups fast.

**Tags:**
system-design::databases source::system-design-interview-xu

---

### What Read Replicas Do and Don't Scale
<!-- anki:1794426132040 -->

**Front:**
What does adding database read replicas scale, and what does it *not* scale?

**Back:**
Replicas scale **reads** and improve **availability**. They don't scale **writes** or **storage**.

Why: all writes go to the primary, which streams them to every replica. Each replica still applies every write and holds the full dataset. So write throughput is capped at what one primary can handle, and the data has to fit on one machine.

This suits read-heavy workloads, which often run 10:1 reads to writes or more. To scale writes or storage, you need sharding.

**Tags:**
system-design::databases source::system-design-interview-xu

---

### Primary Database Failover
<!-- anki:1794426132090 -->

**Front:**
In primary-replica replication, what happens when the primary fails, and why is failover risky?

**Back:**
A replica is **promoted** to primary, and the other replicas start following it. (A replica failing is easy: its reads go to other replicas.)

The risk: replication is usually **asynchronous**, so the promoted replica may be missing the primary's most recent writes. Those writes are either lost or have to be recovered with repair scripts.

**Tags:**
system-design::databases source::system-design-interview-xu

---

### Replication Lag and Read-Your-Writes
<!-- anki:1794426132139 -->

**Front:**
What is replication lag, and how do you keep users from seeing stale data right after their own writes?

**Back:**
Replicas apply writes slightly after the primary, so a read from a replica can return old data. The classic bug: a user updates their profile, the page reloads from a replica, and the change seems to have vanished.

The fix is **read-your-writes consistency**: send a user's reads to the primary for a short window after they write, or always read a user's own data from the primary. Other users seeing slightly stale data is usually fine.

**Tags:**
system-design::databases source::system-design-interview-xu

---

### Challenges of Sharding
<!-- anki:1794426132188 -->

**Front:**
What are the main challenges sharding introduces? (3 challenges)

**Back:**
- **Resharding**: when shards fill up or become uneven, you have to change the shard function and move data between machines while still serving traffic.
- **Hotspots (the celebrity problem)**: a few keys get far more traffic than the rest and overload their shard, no matter how many shards you add.
- **Cross-shard joins**: related rows live on different machines, so no single database engine can see both sides of the join. The app has to query several shards and merge the results itself, which is slow and complex. The usual fix is to **denormalize** so that a query only needs one shard.

**Tags:**
system-design::databases source::system-design-interview-xu

---

### Choosing a Shard Key
<!-- anki:1794426132239 -->

**Front:**
What makes a good shard key?

**Back:**
One that **spreads data and traffic evenly** across shards. Ideally it also keeps data that's queried together on the same shard. For example, sharding by `user_id` keeps all of a user's data together and avoids cross-shard queries.

Bad keys:
- **Low cardinality** (e.g. country): only a few distinct values, so a few huge shards.
- **Ever-increasing values** (e.g. timestamp) with range-based sharding: every new write lands on the last shard.

Why it matters: each shard is a single machine. If one shard gets most of the load, adding more shards doesn't help.

**Tags:**
system-design::databases source::system-design-interview-xu

---

### Denormalization
<!-- anki:1794426132288 -->

**Front:**
What is denormalization, and what does it trade off?

**Back:**
Storing **copies of data where it's read** instead of keeping each fact in one place and joining at read time.

Normalized: showing an order with the buyer's name requires a join.

```
users:  { user_id: 42, name: "Colin" }
orders: { order_id: 900, user_id: 42, total: 30 }
```

Denormalized: the name is copied into the order, so one read gets everything. That matters once the two tables live on different shards.

```
orders: { order_id: 900, user_id: 42, user_name: "Colin", total: 30 }
```

- **Gain**: faster, simpler reads that need no joins and can stay on one shard.
- **Cost**: harder writes. A change must update every copy, missed copies leave the data inconsistent, and storage grows.

Denormalize fields that are **read often and change rarely**, like a display name, and not values that change constantly, like an inventory count.

**Tags:**
system-design::databases source::system-design-interview-xu

---

### What Data Belongs in a Cache
<!-- anki:1794426132338 -->

**Front:**
What kind of data is a good fit for a cache? (3 properties)

**Back:**
Data that is **read often, changed rarely**, and **safe to lose**.

Why:
- A cache lives in memory, which is fast but volatile: a restart wipes it. So the database must stay the source of truth.
- Data that changes often needs constant invalidation and causes more stale reads, which cancels out the benefit.

The common pattern is **cache-aside**: check the cache first. On a miss, read from the database and store the result in the cache.

**Tags:**
system-design::caching source::system-design-interview-xu

---

### Cache Expiration (TTL) Tradeoff
<!-- anki:1794426132393 -->

**Front:**
What's the tradeoff in choosing a cache entry's expiration time (TTL)?

**Back:**
- **Too short**: entries expire before they're reused, so reads keep going to the database and the cache adds little.
- **Too long**: the cache drifts out of sync with the database and serves stale data, and memory fills with entries nobody reads.

Choose the TTL for each kind of data based on how much staleness it can tolerate. A user's avatar can be stale for hours. An account balance can't be stale at all.

**Tags:**
system-design::caching source::system-design-interview-xu

---

### Cache Eviction Policies
<!-- anki:1794426132444 -->

**Front:**
When a cache is full, how do the LRU, LFU, and FIFO eviction policies differ?

**Back:**
- **LRU (least recently used)**: evicts the item that hasn't been accessed for the longest time. It's the usual default, because recent access is a good predictor of future access.
- **LFU (least frequently used)**: evicts the item with the fewest accesses. It suits stable popularity, where the same items stay hot. Its weakness is that items popular long ago can linger.
- **FIFO (first in, first out)**: evicts the oldest inserted item regardless of use. It's the simplest, but because it ignores access patterns it can evict hot items.

**Tags:**
system-design::caching source::system-design-interview-xu

---

### What Content Belongs on a CDN
<!-- anki:1794426132493 -->

**Front:**
How do you decide whether content can be served from a CDN?

**Back:**
Ask: **does every user get the same bytes?** If so, the content can be cached at the edge.

- **Yes**: images, video, CSS, fonts, and **JavaScript**. The CDN only delivers the JS file; the browser runs it.
- **Sometimes**: HTML, when it's static (static sites, the shell page of a single-page app).
- **No**: personalized content such as feeds, carts, and most API responses. These go to the origin servers.

**Tags:**
system-design::cdn source::system-design-interview-xu

---

### Content-Hashed Asset Filenames
<!-- anki:1794426132539 -->

**Front:**
How do content-hashed asset filenames (e.g. `app.3f9a2c.js`) solve CDN cache invalidation?

**Back:**
The build tool puts a hash of each file's contents into its name. When the contents change, the filename changes, so the CDN sees a brand-new URL it has never cached.

- **Assets** can be cached for a very long time (e.g. a year), because the content at a given URL never changes.
- **HTML** gets a short TTL, because it's the file that points to the current hashed names. That way new deploys are picked up quickly.

The payoff: you never need to send invalidation requests to the CDN, and users never load a mix of old and new files.

**Tags:**
system-design::cdn source::system-design-interview-xu

---

### Stateless Web Tier
<!-- anki:1794426132593 -->

**Front:**
Why should the web tier be stateless, and what's wrong with using sticky sessions instead? (3 problems with sticky sessions)

**Back:**
If a server keeps session data in its own memory, each user's requests must keep going to that same server. Sticky sessions arrange this, but:
- Load becomes uneven across servers.
- When a server dies or is replaced, all of its users' sessions are lost.
- Autoscaling is awkward. A new server only gets new users, and removing a server means waiting for its sessions to drain.

Stateless approach: move session data to a shared store such as Redis. Then any server can handle any request, so simple load balancing and autoscaling just work. The state still exists; it has moved to a layer built to hold it.

**Tags:**
system-design::scaling source::system-design-interview-xu

---

### Server-Side Sessions vs. JWTs
<!-- anki:1794426132640 -->

**Front:**
What's the core tradeoff between server-side sessions and JWTs for authentication?

**Back:**
- **Server-side session**: the client holds a random, unguessable session ID, and the server looks it up in a store on every request. Every request costs a lookup, but revoking access is trivial: delete the session.
- **JWT**: the client holds a signed token that contains the claims (user ID, expiry). The server only checks the signature, so there's no lookup. But it's **hard to revoke early**: there's nothing on the server to delete, so the token works until it expires.

Sessions suit a single app. JWTs suit setups with many services or an external identity provider, because each service can check tokens with the issuer's public key instead of calling an auth service.

**Tags:**
system-design::auth source::system-design-interview-xu

---

### Access Tokens and Refresh Tokens
<!-- anki:1794426132689 -->

**Front:**
Why are short-lived JWT access tokens usually paired with refresh tokens?

**Back:**
The pairing keeps most of the JWT's speed (no lookup) while making access revocable.

- **Access token**: a JWT that expires quickly (~15 minutes). It's sent with every request and checked by signature only.
- **Refresh token**: long-lived and **stored server-side**. It's used only to get a new access token, and the server checks it against its store each time.

To revoke access, delete the refresh token. In the worst case, a stolen access token keeps working until it expires, which is a short, bounded window.

**Tags:**
system-design::auth source::system-design-interview-xu

---

### Challenges of Multiple Data Centers
<!-- anki:1794426132739 -->

**Front:**
What are the main technical challenges of running a system in multiple data centers? (3 challenges)

**Back:**
- **Routing traffic**: send each user to the nearest healthy data center, usually with geoDNS, and shift traffic elsewhere when one fails.
- **Keeping data in sync**: each data center has its own data stores. Because replication between regions is usually asynchronous, a data center taking over after a failure may be missing recent writes.
- **Testing and deploying**: every location must run the same versions, which in practice requires automated deployment.

The payoff is surviving a full data center outage and lower latency for users around the world.

**Tags:**
system-design::scaling source::system-design-interview-xu

---

### Message Queues for Decoupling
<!-- anki:1794426132788 -->

**Front:**
How does a message queue help a system scale and stay reliable? (3 benefits)

**Back:**
Producers publish messages to a durable queue, and consumers process them asynchronously. The queue **decouples** the two sides, so they can:
- **Scale independently**: if the queue grows, add consumers. The producers don't change.
- **Fail independently**: if the consumers are down, producers keep publishing and the messages wait in the queue.
- **Handle spikes**: the queue buffers bursts, and consumers work through them at their own pace.

Example: when a user uploads a photo, the web server queues image-processing jobs (resizing, thumbnails) and returns right away. Background workers process the jobs, and the number of workers scales with the queue length.

**Tags:**
system-design::messaging source::system-design-interview-xu

---
