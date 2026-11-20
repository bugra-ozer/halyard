from enum import StrEnum, auto

# Fixed enum strings for API normalization.

class RuleType(StrEnum):
    """Belongs to Pydantic schema's Rule class."""
    USER_LIST = auto()
    ATTRIBUTE = auto()
    PERCENTAGE = auto()

class Operator(StrEnum):
    """Belongs to Pydantic schema's Rule Create, Update, Response class' conditions attribute."""
    EQUALS = auto()
    NOT_EQUALS = auto()
    IN = auto()
    CONTAINS = auto()

class EvaluationReason(StrEnum):
    """Belongs to Pydantic EvalRequest schema, reason attribute."""
    FLAG_DISABLED = auto()
    RULE_MATCHED = auto()
    PERCENTAGE_ROLLOUT = auto()
    DEFAULT = auto()