private void freeAllocatedSpace(java.util.Collection sortedFreeSpaceList)
    {
        if (Tracing.isAnyTracingEnabled() && trace.isEntryEnabled())
            trace.entry(this,
                        cclass,
                        "freeAllocatedSpace",
                        new Object[] { new Integer(sortedFreeSpaceList.size()), new Long(freeSpaceByLength.size()) });

        // Remove from the head of the sorted set until we find the first non-negative
        // address - indicating that the storage was allocated
        java.util.Iterator listIterator = sortedFreeSpaceList.iterator();
        Directory.StoreArea currentArea = null;
        while (listIterator.hasNext()) {
            currentArea = (Directory.StoreArea) listIterator.next();
            if (currentArea.byteAddress > 0)
                break;
        }

        // Did we find at least one to merge?
        if (currentArea != null) {

            // We now have a pointer to the first store area in the sorted list
            // that needs to be merged into the free space map.
            // We iterate through the free space map (which is also in order)
            // merging the entries in, and moving our pointer forwards.
            FreeSpace spaceEntry = freeSpaceByAddressHead;
            FreeSpace previousEntry = null;
            do {
                // If spaceEntry is null then we have reached the end of the list.
                // We handle this case first, because we can avoid null-checks in
                // other branches.
                // The same logic is used to handle the case where we have moved
                // past the point in the address-sorted free space list where this
                // entry would be merged, and did not find any existing entries
                // to merge it with. Merging would have been performed in branches
                // below on an earlier pass round the loop if it was possible (as
                // we would have looked at the entry that is now spaceEntry as        
                // spaceEntry.next in the below branches).
                if (spaceEntry == null || // Tail of list reached
                    spaceEntry.address > currentArea.byteAddress // Moved past insertion point without merge
                ) {
                    // Create a new entry, unless this is a zero-sized entry
                    if (currentArea.length > 0) {
                        FreeSpace newSpaceEntry =
                                        new FreeSpace(currentArea.byteAddress, currentArea.length);

                        // Link it in behind the current entry
                        newSpaceEntry.next = spaceEntry;
                        if (previousEntry != null) {
                            previousEntry.next = newSpaceEntry;
                        }
                        else {
                            // We are the new head
                            freeSpaceByAddressHead = newSpaceEntry;
                        }
                        newSpaceEntry.prev = previousEntry;
                        if (spaceEntry != null) {
                            spaceEntry.prev = newSpaceEntry;
                        }

                        // Add our extended entry into the length-sorted list
                        freeSpaceByLength.add(newSpaceEntry);

                        // Debug freespace list
                        // if (Tracing.isAnyTracingEnabled() && trace.isDebugEnabled()) trace.debug(this, cclass, methodName, "ADD to freespace list");

                        // Keep track of the maximum free space count as a statistic
                        if (gatherStatistics && freeSpaceByLength.size() > maxFreeSpaceCount)
                            maxFreeSpaceCount = freeSpaceByLength.size();

                        // As we've added a new entry before the current on, we should use it next time round
                        spaceEntry = newSpaceEntry;
                        // Previous entry stayed the same - as we've inserted without moving forwards
                    }
                    // Regardless of whether we added an entry, move onto the next store area and
                    // go back round the loop.
                    if (listIterator.hasNext()) {
                        currentArea = (Directory.StoreArea) listIterator.next();
                    }
                    else
                        currentArea = null; // We've run out of entries to merge
                }
                // Can our current store entry be merged with the current free space entry.
                else if (spaceEntry.address + spaceEntry.length == currentArea.byteAddress) {
                    // We can merge this entry with the one before it.
                    // Remove from the length-sorted list and change the size
                    freeSpaceByLength.remove(spaceEntry);
                    spaceEntry.length += currentArea.length;

                    // Can we also merge it with the one after it?
                    FreeSpace nextSpaceEntry = spaceEntry.next;
                    if (nextSpaceEntry != null &&
                        currentArea.byteAddress + currentArea.length == nextSpaceEntry.address) {
                        // Remove the eliminated space entry from the length-sorted list
                        freeSpaceByLength.remove(nextSpaceEntry);

                        // Debug freespace list
                        // if (Tracing.isAnyTracingEnabled() && trace.isDebugEnabled()) trace.debug(this, cclass, methodName, "REMOVE from freespace list");

                        // Make the previous one larger
                        spaceEntry.length += nextSpaceEntry.length;
                        // Remove the next one
                        spaceEntry.next = nextSpaceEntry.next;
                        if (nextSpaceEntry.next != null) {
                            nextSpaceEntry.next.prev = spaceEntry;
                        }
                    }

                    // Add our extended entry into the length-sorted list
                    freeSpaceByLength.add(spaceEntry);

                    // We've merged this store entry now, so move onto the next one
                    // in the sorted list.
                    if (listIterator.hasNext()) {
                        currentArea = (Directory.StoreArea) listIterator.next();
                    }
                    else
                        currentArea = null; // We've run out of entries to merge
                    // Note we do not advance our position in the free space, as the
                    // current entry could also be of interest to the next store item.
                }
                // Can our current store entry be merged with the next free space entry
                // (note that the case where it merges with both is already handled).
                else if (spaceEntry.next != null &&
                         currentArea.byteAddress + currentArea.length == spaceEntry.next.address) {
                    // Remove from the length-sorted list and change the size
                    FreeSpace nextSpaceEntry = spaceEntry.next;
                    freeSpaceByLength.remove(nextSpaceEntry);
                    nextSpaceEntry.address = currentArea.byteAddress;
                    nextSpaceEntry.length += currentArea.length;

                    // Add back into the length-sorted list
                    freeSpaceByLength.add(nextSpaceEntry);

                    // We've merged this store entry now, so move onto the next one
                    // in the sorted list.
                    if (listIterator.hasNext()) {
                        currentArea = (Directory.StoreArea) listIterator.next();
                    }
                    else
                        currentArea = null; // We've run out of entries to merge
                    // Note we do not advance our position in the free space, as the
                    // current entry could also be of interest to the next store item.
                }
                // Otherwise this space entry is not interesting to us, and we
                // can simply move onto the next one.
                else {
                    previousEntry = spaceEntry;
                    spaceEntry = spaceEntry.next;
                }
                // Although looping through the free space map, our condition for
                // breaking the loop is when we've run out of entries to merge.
            } while (currentArea != null);
        }

        if (Tracing.isAnyTracingEnabled() && trace.isEntryEnabled())
            trace.exit(this,
                       cclass,
                       "freeAllocatedSpace",
                       new Object[] { new Long(freeSpaceByLength.size()) });
    }