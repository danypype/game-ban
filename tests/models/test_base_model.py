from lib.models import BaseModel
from lib.db import Base


def test_base_model():
    """
    Makes sure the definition of the BaseModel class is correct
    """
    assert issubclass(BaseModel, Base)
    assert hasattr(BaseModel, 'created_at')
    assert hasattr(BaseModel, 'updated_at')
