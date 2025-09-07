func (c *replicationLagCache) add(r replicationLagRecord) {
	if !r.Up {
		// Tablet is down. Do no longer track it.
		delete(c.entries, r.Key)
		delete(c.ignoredSlowReplicasInARow, r.Key)
		return
	}

	entry, ok := c.entries[r.Key]
	if !ok {
		entry = newReplicationLagHistory(c.historyCapacityPerReplica)
		c.entries[r.Key] = entry
	}

	entry.add(r)
}