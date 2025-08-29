import os
import sys
import time

# Add path to access agent_orchestrator module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'project', 'scripts'))

from agent_orchestrator import MemoryBuffer


def test_lru_eviction():
    buffer = MemoryBuffer(max_size=2)
    buffer.store('a', 'A')
    time.sleep(0.01)
    buffer.store('b', 'B')
    time.sleep(0.01)
    buffer.retrieve('a')  # Mark 'a' as recently used
    time.sleep(0.01)
    buffer.store('c', 'C')  # Should evict 'b'

    assert buffer.retrieve('a') == 'A'
    assert buffer.retrieve('b') is None
    assert buffer.retrieve('c') == 'C'
