import os
import sys
import tempfile

class SingleInstance:
    """
    Ensures that only one instance of the application is running.
    This is achieved by creating and locking a file in the system's temporary directory.
    The lock is released when the application exits.
    """
    def __init__(self, app_name="DefaultApp"):
        self.app_name = app_name
        # Use a consistent lock file path in the temp directory
        self.lockfile = os.path.join(tempfile.gettempdir(), f"{self.app_name}.lock")
        self.fp = None
        self._is_running = self._check_running()

    def _check_running(self):
        """Check if another instance is running by trying to acquire a file lock."""
        try:
            # Open the file in write mode. This will create it if it doesn't exist.
            self.fp = open(self.lockfile, 'w')
            
            # Try to acquire an exclusive lock on the file without blocking.
            if sys.platform == 'win32':
                import msvcrt
                # This will raise an IOError if the lock is already held by another process.
                msvcrt.locking(self.fp.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                # This will raise an IOError if the lock is already held.
                fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            # If we successfully acquired the lock, the app is not running.
            return False
        except (IOError, ImportError):
            # The lock is held by another instance, or we can't import the locking module.
            if self.fp:
                self.fp.close()
            self.fp = None
            return True

    def is_running(self):
        """Return the running status determined at initialization."""
        return self._is_running

    def __del__(self):
        """Release the lock and delete the lock file when the application exits."""
        if self.fp:
            # The lock is automatically released when the file is closed.
            self.fp.close()
            try:
                os.remove(self.lockfile)
            except OSError:
                pass