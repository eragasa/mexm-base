import pytest
from mexm.manager.referencemanager import ReferenceManager

def test__ReferenceManager__reference_paths__no_args():
    ref_manager = ReferenceManager()
    assert isinstance(ref_manager.reference_paths, list)
    assert len(ref_manager.reference_paths) == 1
    assert all([
        isinstance(k, str) for k in ref_manager.reference_paths
    ])

def test__ReferenceManager__db__no_args():
    ref_manager = ReferenceManager()
    assert isinstance(ref_manager.db, dict)
    assert all([
        isinstance(k, str)  for k in ref_manager.db
    ])
    assert all([
        isinstance(v, dict) for k,v in ref_manager.db.items()
    ])

if __name__ == "__main__":
    ref_manager = ReferenceManager()
    print('ReferenceManager().reference_paths:{}'.format(
        ref_manager.reference_paths
    ))
    for article_id, article_info in ref_manager.db.items():
        print(article_id, article_info)
