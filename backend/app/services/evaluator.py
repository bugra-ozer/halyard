import hashlib

class Evaluator():
    """Evaluate feature flags based on enabled state, target users, and rollout percentage."""

    def __init__(self):
        pass

    def evaluate(
            self,
            flag_key: str,
            enabled: bool,
            rollout_percentage: int = 0,
            target_users: set[str] | None = None,
            user_id: str | None = None
    )->bool: # noqa
        """Determine if a feature flag is active for a given request.

        Args:
            flag_key: Identifier of the feature flag, used for bucketing.
            enabled: Whether the flag is globally enabled.
            rollout_percentage: Percentage (0-100) of users to roll out to.
            target_users: Specific user IDs that always get the flag.
            user_id: ID of the requesting user, used for targeting and bucketing.

        Returns:
            True if the flag is active for this request, otherwise False."""

        guards=self._evaluate_guards(enabled, user_id, target_users, rollout_percentage)
        if guards is not None: return guards

        if rollout_percentage >= 1 or rollout_percentage <=99:
            if isinstance(user_id, str):
                bucket=self._get_user_bucket(flag_key, user_id)
                return bucket<rollout_percentage
        return False

    @staticmethod
    def _evaluate_guards(enabled, user_id, target_users, rollout_percentage:int):
        """Return an immediate decision from guards, or None to continue to bucketing.

        Returns:
            True or False if a guard decides, otherwise None.
        """

        if enabled is False: return False
        if user_id and target_users:
            if user_id in target_users: return True
        if rollout_percentage == 0: return False
        elif rollout_percentage == 100: return True
        elif user_id is None: return False
        return None

    @staticmethod
    def _get_user_bucket(flag_key: str, user_id: str):
        """Map a (flag_key, user_id) pair deterministically to a 0-99 bucket.

        Args:
            flag_key: Identifier of the feature flag.
            user_id: ID of the requesting user.

        Returns:
            Integer bucket in the range 0-99.
        """
        hash_string = flag_key + user_id
        hash_res = int(hashlib.sha256(hash_string.encode()).hexdigest(),16)  # create user_id+flag_key string hash and convert to integer
        bucket = hash_res % 100
        return bucket